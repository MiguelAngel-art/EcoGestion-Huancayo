import os
import tempfile
from pathlib import Path
os.environ['JWT_SECRET'] = 'clave-de-prueba-exclusiva-de-los-tests-123456'

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from backend.db import Base, get_db
from backend.main import app
from backend.models import TipoMaterial, Usuario
from backend.services.seguridad import hash_password

@pytest.fixture
def cliente():
    engine = create_engine('sqlite://', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(engine, expire_on_commit=False)
    with session_factory() as db:
        db.add_all([
            Usuario(email='admin@demo.com', nombre='Admin Demo', rol='admin', password_hash=hash_password('AdminSeguro123!')),
            Usuario(email='operador@demo.com', nombre='Operador Demo', rol='operador', password_hash=hash_password('OperadorSeguro123!')),
            TipoMaterial(nombre='Plástico'), TipoMaterial(nombre='Papel'),
        ])
        db.commit()
    def override():
        with session_factory() as db: yield db
    app.dependency_overrides[get_db] = override
    with TestClient(app) as cliente:
        yield cliente
    app.dependency_overrides.clear()
    engine.dispose()

def headers(c, user='admin@demo.com', password='AdminSeguro123!'):
    res = c.post('/auth/login', json={'email':user,'password':password})
    assert res.status_code == 200, res.text
    return {'Authorization':f"Bearer {res.json()['access_token']}"}

def test_auth_y_crud_integrado(cliente):
    assert cliente.get('/familias').status_code == 401
    assert cliente.post('/auth/login', json={'email':'admin@demo.com','password':'incorrecta'}).status_code == 401
    h = headers(cliente)
    f = cliente.post('/familias', headers=h, json={'responsable':'Ana Torres','sector':'Azapampa','direccion':'Jr. Las Flores 123','telefono':'987654321'})
    assert f.status_code == 201, f.text
    fid = f.json()['id']
    assert len(cliente.get('/familias', headers=h).json()) == 1
    f = cliente.put(f'/familias/{fid}', headers=h, json={'responsable':'Ana Torres A','sector':'Azapampa','direccion':'Jr. Las Flores 124','telefono':'987654321'})
    assert f.status_code == 200
    r = cliente.post('/recolecciones', headers=h, json={'familia_id':fid,'fecha':'2026-11-22','estado':'pendiente','observacion':''})
    assert r.status_code == 201, r.text
    rid = r.json()['id']
    assert cliente.post('/materiales', headers=h, json={'recoleccion_id':rid,'material_id':1,'cantidad_kg':4.5,'fecha_registro':'2026-11-22'}).status_code == 409
    r = cliente.put(f'/recolecciones/{rid}', headers=h, json={'familia_id':fid,'fecha':'2026-11-22','estado':'completada','observacion':'Recogido'})
    assert r.status_code == 200, r.text
    m = cliente.post('/materiales', headers=h, json={'recoleccion_id':rid,'material_id':1,'cantidad_kg':4.5,'fecha_registro':'2026-11-22'})
    assert m.status_code == 201, m.text
    mid = m.json()['id']
    assert cliente.get('/dashboard',headers=h).json()['total_kg'] == 4.5
    assert cliente.get('/dashboard',headers=h).json()['recolecciones_completadas'] == 1
    assert cliente.delete(f'/familias/{fid}',headers=h).status_code == 409
    operador_h = headers(cliente, 'operador@demo.com','OperadorSeguro123!')
    assert cliente.delete(f'/materiales/{mid}',headers=operador_h).status_code == 403
    assert cliente.delete(f'/materiales/{mid}',headers=h).status_code == 204
    assert cliente.delete(f'/recolecciones/{rid}',headers=h).status_code == 204
    assert cliente.delete(f'/familias/{fid}',headers=h).status_code == 204
    assert cliente.get('/dashboard',headers=h).json()['total_kg'] == 0

def test_validaciones(cliente):
    h = headers(cliente)
    assert cliente.post('/familias', headers=h, json={'responsable':'A','sector':'X','direccion':'X','telefono':'abc'}).status_code == 422
    assert cliente.post('/recolecciones', headers=h, json={'familia_id':999,'fecha':'2026-11-22','estado':'pendiente'}).status_code == 404
