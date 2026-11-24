# EcoGestión Huancayo

## Sistema Web de Gestión de Reciclaje

EcoGestión Huancayo es un proyecto desarrollado para el curso de Programación Web. Su finalidad es ayudar a organizar las actividades de reciclaje en la ciudad de Huancayo, Perú.

El sistema permite registrar familias, gestionar recolecciones, registrar materiales reciclables y consultar estadísticas mediante un panel de control.

## 1. Problemática

En Huancayo, la gestión de residuos sólidos es un problema que afecta al medio ambiente. Por ello, este proyecto propone un sistema web que permita organizar y llevar un mejor control de las actividades de reciclaje.

## 2. Objetivo

Desarrollar una aplicación web que facilite el registro de familias, recolecciones y materiales reciclables, utilizando herramientas de programación web y una base de datos.

## 3. Tecnologías utilizadas

**Frontend:**
- Angular 22
- TypeScript
- HTML5
- SCSS
- Bootstrap 5

**Backend:**
- Python
- FastAPI
- SQLAlchemy
- API REST
- JWT para autenticación

**Base de datos:**
- SQL Server Express

**Herramientas:**
- Visual Studio Code
- Git y GitHub
- Swagger UI

## 4. Funcionalidades del sistema

**Inicio de sesión**
- Ingresar con correo y contraseña.
- Validar los datos del usuario.
- Cerrar sesión.

**Gestión de familias**
- Registrar familias.
- Mostrar familias registradas.
- Editar y eliminar registros.

**Gestión de recolecciones**
- Registrar nuevas recolecciones.
- Consultar las recolecciones.
- Cambiar su estado a pendiente o completada.
- Editar y eliminar registros.

**Gestión de materiales**
- Registrar materiales reciclables.
- Seleccionar una recolección completada.
- Registrar la cantidad en kilogramos.
- Consultar, editar y eliminar registros.

**Panel de control**
- Mostrar el número de familias registradas.
- Mostrar las recolecciones completadas.
- Mostrar el total de kilogramos recuperados.

## 5. Funcionamiento del sistema

El proyecto está dividido en tres partes:

- **Angular:** muestra las páginas, formularios y tablas.
- **FastAPI:** recibe las solicitudes y procesa la información.
- **SQL Server:** almacena los datos del sistema.

La comunicación funciona de la siguiente manera:

**Usuario → Angular → FastAPI → SQL Server**

También se utilizan Angular Signals para actualizar los datos que aparecen en pantalla.

## 6. Estructura del proyecto

```text
EcoGestion-Huancayo/
|
|-- backend/
|   |-- src/
|   |-- iniciar_backend.bat
|   |-- crear_usuario.bat
|
|-- frontend/
|   |-- public/
|   |-- src/
|       |-- app/
|           |-- guards/
|           |-- pages/
|               |-- login/
|               |-- dashboard/
|               |-- familias/
|               |-- recolecciones/
|               |-- materiales/
|
|-- .gitignore
|-- README.md
```

## 7. Instalación y ejecución

Para ejecutar el proyecto se necesita:

- Python
- Node.js y npm
- SQL Server Express
- Controlador ODBC para SQL Server

**Paso 1. Clonar el repositorio**

```powershell
git clone https://github.com/MiguelAngel-art/EcoGestion-Huancayo.git
cd EcoGestion-Huancayo
```

**Paso 2. Configurar el backend**

Configurar la conexión con SQL Server y las variables necesarias en el archivo `.env`.

Ingresar a la carpeta del backend y ejecutar:

```powershell
cd backend
.\iniciar_backend.bat
```

La API estará disponible en:

http://127.0.0.1:8000/docs

**Paso 3. Crear un usuario**

Desde la carpeta `backend`, ejecutar:

```powershell
.\crear_usuario.bat
```

**Paso 4. Ejecutar el frontend**

Abrir otra terminal desde la carpeta principal del proyecto:

```powershell
cd frontend
npm.cmd install
npx.cmd ng serve --configuration development --prebundle=false --no-hmr
```

Abrir en el navegador:

http://localhost:4200

Para que el sistema funcione correctamente, SQL Server y el backend deben estar ejecutándose.

## 8. Seguridad

El sistema utiliza autenticación con JWT y contraseñas almacenadas mediante hashes.

Los datos de configuración y las claves privadas se mantienen en archivos de entorno que no deben publicarse en GitHub.

## 9. Pruebas realizadas

Durante el desarrollo se realizaron pruebas de:

- Inicio y cierre de sesión.
- Registro, edición y eliminación de familias.
- Registro, edición y eliminación de recolecciones.
- Registro, edición y eliminación de materiales.
- Actualización de estadísticas.
- Navegación entre las diferentes páginas.

Se utilizaron datos de prueba para comprobar el funcionamiento del sistema.

## 10. Conclusión

EcoGestión Huancayo es una aplicación web que permite organizar información relacionada con el reciclaje. Con este proyecto se aplicaron conocimientos de Angular, Python, FastAPI y SQL Server.

El sistema cumple con las funciones principales propuestas y puede seguir mejorándose para su uso en actividades reales de reciclaje.

---

**Proyecto académico — Programación Web, 2026**