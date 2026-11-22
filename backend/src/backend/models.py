"""Modelo relacional en 3FN: las familias, materiales, usuarios y recolecciones tienen claves propias."""
from datetime import date
from decimal import Decimal
from sqlalchemy import Boolean, CheckConstraint, Date, ForeignKey, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.db import Base

class Usuario(Base):
    __tablename__ = 'usuarios'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    rol: Mapped[str] = mapped_column(String(12), nullable=False)  # admin | operador
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    __table_args__ = (CheckConstraint("rol IN ('admin', 'operador')", name='ck_usuarios_rol'),)

class Familia(Base):
    __tablename__ = 'familias'
    id: Mapped[int] = mapped_column(primary_key=True)
    responsable: Mapped[str] = mapped_column(String(100), nullable=False)
    sector: Mapped[str] = mapped_column(String(100), nullable=False)
    direccion: Mapped[str] = mapped_column(String(160), nullable=False)
    telefono: Mapped[str] = mapped_column(String(15), nullable=False)
    recolecciones: Mapped[list['Recoleccion']] = relationship(back_populates='familia')

class Recoleccion(Base):
    __tablename__ = 'recolecciones'
    id: Mapped[int] = mapped_column(primary_key=True)
    familia_id: Mapped[int] = mapped_column(ForeignKey('familias.id', ondelete='RESTRICT'), nullable=False, index=True)
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    estado: Mapped[str] = mapped_column(String(16), nullable=False, default='pendiente')
    observacion: Mapped[str] = mapped_column(String(300), nullable=False, default='')
    familia: Mapped[Familia] = relationship(back_populates='recolecciones')
    registros: Mapped[list['RegistroMaterial']] = relationship(back_populates='recoleccion')
    __table_args__ = (CheckConstraint("estado IN ('pendiente', 'completada')", name='ck_recolecciones_estado'),)

class TipoMaterial(Base):
    __tablename__ = 'tipos_material'
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

class RegistroMaterial(Base):
    __tablename__ = 'registros_material'
    id: Mapped[int] = mapped_column(primary_key=True)
    recoleccion_id: Mapped[int] = mapped_column(ForeignKey('recolecciones.id', ondelete='RESTRICT'), nullable=False, index=True)
    material_id: Mapped[int] = mapped_column(ForeignKey('tipos_material.id', ondelete='RESTRICT'), nullable=False)
    cantidad_kg: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    fecha_registro: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)
    recoleccion: Mapped[Recoleccion] = relationship(back_populates='registros')
    material: Mapped[TipoMaterial] = relationship()
    __table_args__ = (
        CheckConstraint('cantidad_kg > 0', name='ck_material_cantidad_positiva'),
        UniqueConstraint('recoleccion_id','material_id',name='uq_material_recoleccion'),
    )
