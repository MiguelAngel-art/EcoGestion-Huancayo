"""Capa que conoce SQLAlchemy; no contiene validaciones de reglas de negocio."""
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend import models

def listar(db: Session, modelo):
    return db.scalars(select(modelo).order_by(modelo.id.desc())).all()

def obtener(db: Session, modelo, ident: int):
    return db.get(modelo, ident)

def guardar(db: Session, objeto):
    db.add(objeto)
    db.commit()
    db.refresh(objeto)
    return objeto

def eliminar(db: Session, objeto):
    db.delete(objeto)
    db.commit()

def existe_dependencia(db: Session, modelo, filtro) -> bool:
    return db.scalar(select(modelo.id).where(filtro).limit(1)) is not None
