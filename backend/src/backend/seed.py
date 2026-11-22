"""Crear usuarios de demo desde consola, sin publicar contraseñas en Git."""
from getpass import getpass
from sqlalchemy import select
from backend.db import Base, SessionLocal, engine
from backend.models import Usuario
from backend.services.seguridad import hash_password

def main():
    Base.metadata.create_all(engine)
    print('Crear un usuario para EcoGestión Huancayo')
    email = input('Correo: ').strip().lower()
    nombre = input('Nombre: ').strip()
    rol = input('Rol (admin/operador) [admin]: ').strip().lower() or 'admin'
    password = getpass('Contraseña (mínimo 10 caracteres): ')
    if '@' not in email or len(nombre) < 3 or rol not in ('admin', 'operador') or len(password) < 10:
        raise SystemExit('Datos inválidos. Revisa correo, nombre, rol y contraseña.')
    with SessionLocal() as db:
        if db.scalar(select(Usuario).where(Usuario.email == email)):
            raise SystemExit('Ese correo ya está registrado.')
        db.add(Usuario(email=email, nombre=nombre, rol=rol, password_hash=hash_password(password)))
        db.commit()
    print('Usuario creado. Puedes iniciar sesión desde http://localhost:4200')

if __name__ == '__main__':
    main()
