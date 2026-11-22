"""Punto de entrada: uvicorn backend.main:app --app-dir src --reload"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from backend.db import Base, SessionLocal, engine
from backend.models import TipoMaterial
from backend.apis import auth, familias, recolecciones, materiales, dashboard

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Para proyectos escolares sirve create_all; en producción usar migraciones Alembic.
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        for nombre in ('Plástico', 'Papel', 'Cartón', 'Vidrio'):
            if db.scalar(select(TipoMaterial).where(TipoMaterial.nombre == nombre)) is None:
                db.add(TipoMaterial(nombre=nombre))
        db.commit()
    yield

app = FastAPI(title='EcoGestión Huancayo - API', version='1.0.0', lifespan=lifespan)
origins = os.getenv('CORS_ORIGINS', 'http://localhost:4200,http://127.0.0.1:4200').split(',')
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=False, allow_methods=['GET','POST','PUT','DELETE'], allow_headers=['Authorization','Content-Type'])

app.include_router(auth.router)
app.include_router(familias.router)
app.include_router(recolecciones.router)
app.include_router(materiales.router)
app.include_router(dashboard.router)

@app.get('/health', tags=['Estado'])
def health():
    return {'estado': 'ok', 'sistema': 'EcoGestión Huancayo'}
