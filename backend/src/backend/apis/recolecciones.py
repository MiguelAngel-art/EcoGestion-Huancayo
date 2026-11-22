from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.models import Recoleccion, Familia, Usuario, RegistroMaterial
from backend.repositories import crud
from backend.schemas.entidades import RecoleccionIn, RecoleccionOut
from backend.services import gestion
from backend.services.seguridad import solo_admin, usuario_actual

router = APIRouter(prefix='/recolecciones', tags=['Recolecciones'])
Db = Annotated[Session, Depends(get_db)]
Acceso = Annotated[Usuario, Depends(usuario_actual)]
Admin = Annotated[Usuario, Depends(solo_admin)]

@router.get('', response_model=list[RecoleccionOut])
def listar(db: Db, _usuario: Acceso):
    return [gestion.respuesta_recoleccion(r) for r in crud.listar(db, Recoleccion)]

@router.get('/{id}', response_model=RecoleccionOut)
def obtener(id: int, db: Db, _usuario: Acceso):
    return gestion.respuesta_recoleccion(gestion.requerido(db, Recoleccion, id))

@router.post('', response_model=RecoleccionOut, status_code=status.HTTP_201_CREATED)
def crear(datos: RecoleccionIn, db: Db, _usuario: Acceso):
    gestion.requerido(db, Familia, datos.familia_id)
    obj = gestion.guardar_seguro(db, Recoleccion(**datos.model_dump()))
    return gestion.respuesta_recoleccion(obj)

@router.put('/{id}', response_model=RecoleccionOut)
def actualizar(id: int, datos: RecoleccionIn, db: Db, _usuario: Acceso):
    obj = gestion.requerido(db, Recoleccion, id)
    gestion.requerido(db, Familia, datos.familia_id)
    gestion.verificar_estado(db, id, datos.estado)
    # Evitar reasignar materiales existentes a otra familia/recolección sin revisión
    if datos.familia_id != obj.familia_id and crud.existe_dependencia(db, RegistroMaterial, RegistroMaterial.recoleccion_id == id):
        from fastapi import HTTPException
        raise HTTPException(409, 'No puedes cambiar la familia de una recolección que ya registra materiales')
    for k, v in datos.model_dump().items(): setattr(obj, k, v)
    gestion.guardar_seguro(db, obj)
    return gestion.respuesta_recoleccion(obj)

@router.delete('/{id}', status_code=204)
def eliminar(id: int, db: Db, _admin: Admin):
    obj = gestion.requerido(db, Recoleccion, id)
    gestion.verificar_recoleccion_sin_materiales(db, id)
    gestion.eliminar_seguro(db, obj)
