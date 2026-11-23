
"""Conexion de EcoGestion Huancayo con SQL Server."""

import os
from pathlib import Path
from collections.abc import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# Cargar variables del archivo .env
ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(ENV_PATH)

DB_ENGINE = os.getenv("DB_ENGINE", "").lower().strip()

if DB_ENGINE == "sqlserver":

    servidor = os.getenv("DB_SERVER", r".\SQLEXPRESS")
    base_datos = os.getenv("DB_NAME", "EcoGestionHuancayo")
    controlador = os.getenv(
        "DB_ODBC_DRIVER",
        "ODBC Driver 18 for SQL Server"
    )

    # Autenticacion de Windows
    conexion_odbc = (
        f"DRIVER={{{controlador}}};"
        f"SERVER={servidor};"
        f"DATABASE={base_datos};"
        "Trusted_Connection=yes;"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )

    url = URL.create(
        "mssql+pyodbc",
        query={"odbc_connect": conexion_odbc}
    )

    engine = create_engine(
        url,
        pool_pre_ping=True
    )

else:
    raise RuntimeError(
        "Configura DB_ENGINE=sqlserver en backend/.env"
    )

# Sesiones de la base de datos
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session
