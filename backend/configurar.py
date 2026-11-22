"""Configuración local inicial: genera un secreto JWT único y crea .env."""
from pathlib import Path
import secrets

raiz = Path(__file__).resolve().parent
destino = raiz / '.env'
if destino.exists():
    print('El archivo .env ya existe. No se modificó.')
else:
    ejemplo = (raiz / '.env.example').read_text(encoding='utf-8')
    ejemplo = ejemplo.replace('REEMPLAZAR_POR_UN_SECRETO_ALEATORIO_LARGO', secrets.token_urlsafe(48))
    destino.write_text(ejemplo, encoding='utf-8')
    print('Configuración local .env creada (con clave secreta aleatoria).')
