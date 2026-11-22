"""Reglas de negocio: integridad, estados, dependencias y cálculo de estadísticas."""
from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from backend import models
from backend.repositories import crud
from backend.schemas.entidades import RecoleccionOut, RegistroOut


def requerido(db: Session, modelo, ident: int):
    objeto = crud.obtener(db, modelo, ident)
    if objeto is None:
        raise HTTPException(404, 'Registro no encontrado')
    return objeto


def respuesta_recoleccion(r: models.Recoleccion) -> dict:
    return {
        'id': r.id, 'familia_id': r.familia_id, 'fecha': r.fecha,
        'estado': r.estado, 'observacion': r.observacion,
        'familia_nombre': r.familia.responsable, 'sector': r.familia.sector,
    }


def respuesta_registro(r: models.RegistroMaterial) -> dict:
    return {
        'id': r.id, 'recoleccion_id': r.recoleccion_id,
        'material_id': r.material_id, 'cantidad_kg': r.cantidad_kg,
        'fecha_registro': r.fecha_registro,
        'material_nombre': r.material.nombre,
        'familia_nombre': r.recoleccion.familia.responsable,
    }


def verificar_familia_sin_recolecciones(db: Session, id: int) -> None:
    if crud.existe_dependencia(db, models.Recoleccion, models.Recoleccion.familia_id == id):
        raise HTTPException(409, 'No se puede eliminar una familia con recolecciones asociadas')


def verificar_recoleccion_sin_materiales(db: Session, id: int) -> None:
    if crud.existe_dependencia(db, models.RegistroMaterial, models.RegistroMaterial.recoleccion_id == id):
        raise HTTPException(409, 'No se puede eliminar una recolección con materiales registrados')


def verificar_registro(db: Session, recoleccion_id: int, material_id: int, excluir_id: int | None = None):
    recoleccion = requerido(db, models.Recoleccion, recoleccion_id)
    requerido(db, models.TipoMaterial, material_id)
    if recoleccion.estado != 'completada':
        raise HTTPException(409, 'Solo puedes registrar materiales de una recolección completada')
    query = select(models.RegistroMaterial.id).where(
        models.RegistroMaterial.recoleccion_id == recoleccion_id,
        models.RegistroMaterial.material_id == material_id,
    )
    if excluir_id is not None:
        query = query.where(models.RegistroMaterial.id != excluir_id)
    if db.scalar(query.limit(1)) is not None:
        raise HTTPException(409, 'Ese material ya está registrado en la recolección')


def verificar_estado(db: Session, recoleccion_id: int, nuevo_estado: str):
    if nuevo_estado == 'pendiente' and crud.existe_dependencia(
        db, models.RegistroMaterial, models.RegistroMaterial.recoleccion_id == recoleccion_id
    ):
        raise HTTPException(409, 'La recolección tiene materiales; no puede volver a pendiente')


def guardar_seguro(db: Session, objeto):
    try:
        return crud.guardar(db, objeto)
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, 'Conflicto de integridad o registro duplicado')


def eliminar_seguro(db: Session, objeto):
    try:
        crud.eliminar(db, objeto)
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, 'El registro tiene relaciones y no se puede eliminar')


def resumen(db: Session) -> dict:
    familias = db.scalar(select(func.count(models.Familia.id))) or 0
    terminadas = db.scalar(select(func.count(models.Recoleccion.id)).where(models.Recoleccion.estado == 'completada')) or 0
    kilos = db.scalar(select(func.coalesce(func.sum(models.RegistroMaterial.cantidad_kg), 0)))
    ultimas = db.scalars(select(models.Recoleccion).order_by(models.Recoleccion.fecha.desc(), models.Recoleccion.id.desc()).limit(5)).all()
    return {
        'familias': familias,
        'recolecciones_completadas': terminadas,
        'total_kg': float(kilos or 0),
        'ultimas_recolecciones': [respuesta_recoleccion(r) for r in ultimas],
    }
