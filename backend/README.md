# EcoGestión Huancayo — Backend FastAPI

Primer bloque del proyecto de Programación Web: **API funcional para familias, recolecciones, materiales, acceso y dashboard**.

## Empezar en Windows (VS Code + PowerShell)

1. Instala **Python 3.11 o superior** y VS Code. Al instalar Python, activa «Add Python to PATH» y comprueba `py --version`.
2. Descomprime `EcoGestion_Backend_Paso1.zip`. Abre en VS Code la **carpeta `backend`** del ZIP (Archivo → Abrir carpeta).
3. En la terminal de VS Code escribe ` .\iniciar_backend.bat ` o haz doble clic en ese archivo dentro de la carpeta.
4. La primera ejecución crea `.venv`, instala paquetes y genera `.env` automáticamente. **No cierres esa terminal**.
5. Abre http://127.0.0.1:8000/health y confirma `{"estado":"ok"}`.
6. Abre http://127.0.0.1:8000/docs para ver y probar todas las rutas HTTP.
7. En **otra terminal**, desde la carpeta `backend`, ejecuta `.\crear_usuario.bat`; introduce tu correo, nombre, rol `admin` y una contraseña segura de **10 caracteres o más**. La contraseña no se ve mientras escribes.
8. En `/docs`, prueba **POST `/auth/login`** con tu correo y contraseña. Copia `access_token`.
9. Pulsa el botón **Authorize** arriba en Swagger e introduce el token en el campo del esquema HTTP Bearer. Si pide prefijo, usa `Bearer TU_TOKEN` (según el cuadro que muestre). Ya puedes probar POST `/familias` y los demás endpoints.

Para apagar el servidor presiona `Ctrl+C` en la terminal. Para reiniciarlo basta con volver a ejecutar `.\iniciar_backend.bat`.

### Si prefieres escribir comandos en PowerShell

Ubicado dentro de `backend`:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe configurar.py
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --app-dir src --reload
```

Para crear el usuario en otra terminal:

```powershell
$env:PYTHONPATH = (Resolve-Path .\src).Path
.\.venv\Scripts\python.exe -m backend.seed
```

### URLs de trabajo

| Servicio | Dirección |
| --- | --- |
| Backend | http://127.0.0.1:8000 |
| Estado | http://127.0.0.1:8000/health |
| Documentación interactiva | http://127.0.0.1:8000/docs |
| Frontend Angular (más adelante) | http://localhost:4200 |

El backend **no abre una página visual**: `/docs` es su interfaz de prueba. La página con botones y pantallas será el frontend Angular.

## Estructura explicada para la sustentación

```
backend/
├── src/backend/
│   ├── main.py                    # Arranca FastAPI, habilita CORS y registra rutas
│   ├── db.py                      # Configura la sesión de base de datos
│   ├── models.py                  # Tablas, relaciones y restricciones (3FN)
│   ├── apis/                      # Rutas HTTP por módulo
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   ├── familias.py
│   │   ├── recolecciones.py
│   │   └── materiales.py
│   ├── schemas/entidades.py       # Validación de entradas y salidas con Pydantic
│   ├── services/                  # Reglas de negocio, seguridad, autenticación JWT
│   ├── repositories/crud.py       # Acceso a datos mediante SQLAlchemy
│   └── seed.py                    # Crear usuarios para demostraciones
├── tests/test_flujo.py           # Pruebas automáticas integradas de la API
├── requirements.txt
├── .env.example                   # Plantilla SQLite de desarrollo
├── .env.postgres.example          # Plantilla PostgreSQL para integración final
├── configurar.py                  # Genera la clave local de forma segura
├── iniciar_backend.bat           # Iniciar en Windows
├── crear_usuario.bat             # Crear usuarios de prueba
└── probar_backend.bat            # Ejecutar las pruebas
```

### Flujo de una operación

**Angular → API de FastAPI → Service (reglas) → Repository (SQLAlchemy) → Base de datos → JSON → Angular**.

### Reglas incluidas

- Login con hash **Argon2**, token **JWT**, autorización por roles (administrador/operador).
- CRUD de familias, recolecciones y registros de materiales (listar, consultar, crear, editar, borrar).
- Validación de teléfonos, fechas, valores positivos y estados permitidos con **Pydantic**.
- Integridad referencial: no se borra una familia con recolecciones ni una recolección con materiales asociados.
- Solo se registran kilos de materiales en recolecciones **completadas**.
- Dashboard con conteo de familias, recolecciones completadas y kilos acumulados.
- Peticiones parametrizadas por SQLAlchemy para evitar concatenar SQL inseguro.
- CORS restringido a frontend de desarrollo en 4200.

## Base de datos: SQLite para empezar; PostgreSQL para el entregable

La primera ejecución utiliza el archivo local `ecogestion.db` (**SQLite**). Esto permite tener el backend en localhost sin instalar todavía PostgreSQL, y **los registros persisten cuando se reinicia el servidor**. El modelo relacional ya tiene tablas normalizadas y claves foráneas.

**Antes de la entrega final**, cambia a PostgreSQL. Si instalas Docker Desktop:

1. Instala Docker Desktop y, desde la carpeta `backend`, ejecuta `docker compose up -d db` (el archivo `docker-compose.yml` está incluido).
2. Detén el backend.
3. Cambia en `.env` **solo la línea** `DATABASE_URL` por el valor de `.env.postgres.example`. El servicio Docker incluido crea la base y el usuario de desarrollo.
4. Vuelve a levantar el backend. Se crearán las tablas en PostgreSQL (no se migran automáticamente los datos de SQLite).
5. Recrea el usuario de demostración con `crear_usuario.bat`.

**Nota**: SQLite permite validar el flujo y la normalización, pero no sustituye una prueba real de la conexión a PostgreSQL. El proyecto de clase utiliza `create_all`; en proyectos de producción se prefieren migraciones de esquema.

## Probar las funciones

En la terminal, ejecuta `.\probar_backend.bat` o:

```powershell
$env:PYTHONPATH = (Resolve-Path .\src).Path
.\.venv\Scripts\python.exe -m pytest -q
```

Los tests comprueban login, 401 sin token, CRUD, actualización, restricciones de borrado, estadísticas del dashboard y permisos de roles.

## Seguridad, Git y datos de entrevistas

- **No subas a GitHub el archivo `.env`**, la base de datos local ni contraseñas. `.gitignore` ya las excluye.
- Nunca uses el DNI, número de teléfono o dirección real de entrevistados sin su consentimiento.
- Usa datos inventados para la demostración y conserva evidencias reales de entrevistas autorizadas para el informe.
- Mantén `.env` como secreto local; antes de desplegar públicamente activa HTTPS, credenciales robustas y migraciones.
- Para la rúbrica conserva commits por integrante, ramas descriptivas y Pull Requests con revisiones.
