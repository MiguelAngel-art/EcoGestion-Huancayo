from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.models import Familia, Usuario
from backend.schemas.entidades import FamiliaIn, FamiliaOut
from backend.repositories import crud
from backend.services import gestion
from backend.services.seguridad import solo_admin, usuario_actual

router = APIRouter(prefix='/familias', tags=['Familias'])
Db = Annotated[Session, Depends(get_db)]
Acceso = Annotated[Usuario, Depends(usuario_actual)]
Admin = Annotated[Usuario, Depends(solo_admin)]

@router.get('', response_model=list[FamiliaOut])
def listar(db: Db, _usuario: Acceso):
    return crud.listar(db, Familia)

@router.get('/{id}', response_model=FamiliaOut)
def obtener(id: int, db: Db, _usuario: Acceso):
    return gestion.requerido(db, Familia, id)

@router.post('', response_model=FamiliaOut, status_code=status.HTTP_201_CREATED)
def crear(datos: FamiliaIn, db: Db, _usuario: Acceso):
    return gestion.guardar_seguro(db, Familia(**datos.model_dump()))

@router.put('/{id}', response_model=FamiliaOut)
def actualizar(id: int, datos: FamiliaIn, db: Db, _usuario: Acceso):
    familia = gestion.requerido(db, Familia, id)
    for k, v in datos.model_dump().items(): setattr(familia, k, v)
    return gestion.guardar_seguro(db, familia)

@router.delete('/{id}', status_code=204)
def eliminar(id: int, db: Db, _admin: Admin):
    familia = gestion.requerido(db, Familia, id)
    gestion.verificar_familia_sin_recolecciones(db, id)
    gestion.eliminar_seguro(db, familia)
