from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.models import RegistroMaterial, TipoMaterial, Usuario
from backend.repositories import crud
from backend.schemas.entidades import RegistroIn, RegistroOut, TipoMaterialOut
from backend.services import gestion
from backend.services.seguridad import solo_admin, usuario_actual

router = APIRouter(tags=['Materiales'])
Db = Annotated[Session, Depends(get_db)]
Acceso = Annotated[Usuario, Depends(usuario_actual)]
Admin = Annotated[Usuario, Depends(solo_admin)]

@router.get('/tipos-material', response_model=list[TipoMaterialOut])
def tipos(db: Db, _usuario: Acceso):
    return sorted(crud.listar(db, TipoMaterial), key=lambda x: x.nombre)

@router.get('/materiales', response_model=list[RegistroOut])
def listar(db: Db, _usuario: Acceso):
    return [gestion.respuesta_registro(r) for r in crud.listar(db, RegistroMaterial)]

@router.get('/materiales/{id}', response_model=RegistroOut)
def obtener(id: int, db: Db, _usuario: Acceso):
    return gestion.respuesta_registro(gestion.requerido(db, RegistroMaterial, id))

@router.post('/materiales', response_model=RegistroOut, status_code=status.HTTP_201_CREATED)
def crear(datos: RegistroIn, db: Db, _usuario: Acceso):
    gestion.verificar_registro(db, datos.recoleccion_id, datos.material_id)
    obj = gestion.guardar_seguro(db, RegistroMaterial(**datos.model_dump()))
    return gestion.respuesta_registro(obj)

@router.put('/materiales/{id}', response_model=RegistroOut)
def actualizar(id: int, datos: RegistroIn, db: Db, _usuario: Acceso):
    obj = gestion.requerido(db, RegistroMaterial, id)
    gestion.verificar_registro(db, datos.recoleccion_id, datos.material_id, excluir_id=id)
    for k, v in datos.model_dump().items(): setattr(obj, k, v)
    gestion.guardar_seguro(db, obj)
    return gestion.respuesta_registro(obj)

@router.delete('/materiales/{id}', status_code=204)
def eliminar(id: int, db: Db, _admin: Admin):
    gestion.eliminar_seguro(db, gestion.requerido(db, RegistroMaterial, id))
