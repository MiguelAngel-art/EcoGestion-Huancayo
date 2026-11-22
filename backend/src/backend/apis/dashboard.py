from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.models import Usuario
from backend.schemas.entidades import DashboardOut
from backend.services.gestion import resumen
from backend.services.seguridad import usuario_actual

router = APIRouter(prefix='/dashboard', tags=['Dashboard'])

@router.get('', response_model=DashboardOut)
def obtener(db: Annotated[Session, Depends(get_db)], _usuario: Annotated[Usuario, Depends(usuario_actual)]):
    return resumen(db)
