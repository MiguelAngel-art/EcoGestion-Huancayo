"""JWT, contraseñas Argon2id y roles. El frontend no determina permisos."""
import os
from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.models import Usuario

hasher = PasswordHasher()
bearer = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    return hasher.hash(password)

def verifica_password(password: str, hash_guardado: str) -> bool:
    try:
        return hasher.verify(hash_guardado, password)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False

def crear_token(usuario: Usuario) -> str:
    secret = os.getenv('JWT_SECRET', 'solo_desarrollo_cambiar_antes_de_publicar')
    exp = datetime.now(timezone.utc) + timedelta(minutes=int(os.getenv('JWT_MINUTES', '120')))
    return jwt.encode({'sub': str(usuario.id), 'exp': exp}, secret, algorithm='HS256')

def usuario_actual(
    credenciales: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
    db: Annotated[Session, Depends(get_db)],
) -> Usuario:
    if not credenciales or credenciales.scheme.lower() != 'bearer':
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Debes iniciar sesión')
    try:
        payload = jwt.decode(
            credenciales.credentials,
            os.getenv('JWT_SECRET', 'solo_desarrollo_cambiar_antes_de_publicar'),
            algorithms=['HS256'],
        )
        usuario_id = int(payload['sub'])
    except (jwt.PyJWTError, KeyError, ValueError, TypeError):
        raise HTTPException(401, 'Sesión inválida o vencida')
    usuario = db.get(Usuario, usuario_id)
    if usuario is None or not usuario.activo:
        raise HTTPException(401, 'Usuario no autorizado')
    return usuario

def solo_admin(usuario: Annotated[Usuario, Depends(usuario_actual)]) -> Usuario:
    if usuario.rol != 'admin':
        raise HTTPException(403, 'Esta acción requiere un administrador')
    return usuario
