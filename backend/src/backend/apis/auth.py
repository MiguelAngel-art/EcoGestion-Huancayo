from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.models import Usuario
from backend.schemas.entidades import LoginIn, TokenOut, UsuarioOut
from backend.services.seguridad import usuario_actual, verifica_password, crear_token

router = APIRouter(prefix='/auth', tags=['Acceso'])

@router.post('/login', response_model=TokenOut)
def login(datos: LoginIn, db: Annotated[Session, Depends(get_db)]):
    usuario = db.scalar(select(Usuario).where(Usuario.email == datos.email.lower()))
    if not usuario or not usuario.activo or not verifica_password(datos.password, usuario.password_hash):
        raise HTTPException(401, 'Correo o contraseña incorrectos')
    return {'access_token': crear_token(usuario), 'usuario': usuario}

@router.get('/me', response_model=UsuarioOut)
def me(usuario: Annotated[Usuario, Depends(usuario_actual)]):
    return usuario
