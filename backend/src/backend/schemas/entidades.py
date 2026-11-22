from datetime import date
from decimal import Decimal
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

class Esquema(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, from_attributes=True)

class FamiliaIn(Esquema):
    responsable: str = Field(min_length=3, max_length=100)
    sector: str = Field(min_length=2, max_length=100)
    direccion: str = Field(min_length=3, max_length=160)
    telefono: str = Field(pattern=r'^\d{9}$')

class FamiliaOut(FamiliaIn):
    id: int

class RecoleccionIn(Esquema):
    familia_id: int = Field(gt=0)
    fecha: date
    estado: Literal['pendiente', 'completada'] = 'pendiente'
    observacion: str = Field(default='', max_length=300)

class RecoleccionOut(RecoleccionIn):
    id: int
    familia_nombre: str
    sector: str

class RegistroIn(Esquema):
    recoleccion_id: int = Field(gt=0)
    material_id: int = Field(gt=0)
    cantidad_kg: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    fecha_registro: date

class RegistroOut(RegistroIn):
    id: int
    material_nombre: str
    familia_nombre: str

class TipoMaterialOut(Esquema):
    id: int
    nombre: str

class UsuarioOut(Esquema):
    id: int
    email: str
    nombre: str
    rol: str

class LoginIn(Esquema):
    email: str = Field(min_length=5, max_length=150)
    password: str = Field(min_length=1)

class TokenOut(Esquema):
    access_token: str
    token_type: str = 'bearer'
    usuario: UsuarioOut

class DashboardOut(Esquema):
    familias: int
    recolecciones_completadas: int
    total_kg: float
    ultimas_recolecciones: list[RecoleccionOut]
