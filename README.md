
# 🌱 EcoGestión Huancayo

## Sistema Web de Gestión de Reciclaje

Proyecto académico desarrollado para la asignatura de **Programación Web**, orientado a contribuir a la gestión del reciclaje y al cuidado del medio ambiente en la ciudad de Huancayo, Perú.

El sistema permite registrar familias participantes, gestionar recolecciones, controlar los materiales reciclables recuperados y visualizar estadísticas mediante un panel de control.

---

## 1. Problemática social

La gestión inadecuada de residuos sólidos representa un desafío ambiental para las comunidades urbanas.

EcoGestión Huancayo propone una herramienta digital para organizar la información relacionada con actividades de reciclaje, facilitar el seguimiento de las recolecciones y promover una gestión responsable de los residuos.

## 2. Objetivo general

Desarrollar una aplicación web que facilite el registro y seguimiento de actividades de reciclaje mediante tecnologías modernas, contribuyendo a una gestión organizada y sostenible de residuos reciclables.

## 3. Tecnologías utilizadas

### Frontend
- Angular 22
- TypeScript
- HTML5 y SCSS
- Bootstrap 5
- Angular Signals
- Angular Router
- HttpClient

### Backend
- Python
- FastAPI
- API REST
- SQLAlchemy
- Autenticación JWT

### Base de datos
- Microsoft SQL Server Express
- Modelo de datos relacional

### Herramientas
- Visual Studio Code
- Git
- GitHub
- Swagger UI

## 4. Funcionalidades implementadas

### Autenticación
- Inicio de sesión con correo y contraseña.
- Validación de credenciales desde el backend.
- Protección de rutas del frontend.
- Cierre de sesión.

### Gestión de familias
- Registrar familias.
- Consultar familias.
- Editar información.
- Eliminar registros.

### Gestión de recolecciones
- Registrar recolecciones.
- Consultar recolecciones.
- Actualizar datos y estados.
- Eliminar registros.

### Gestión de materiales
- Registrar materiales reciclables.
- Asociar materiales con recolecciones.
- Registrar cantidades en kilogramos.
- Consultar, editar y eliminar registros.

### Dashboard
- Visualización de familias registradas.
- Conteo de recolecciones completadas.
- Cálculo del total de kilogramos recuperados.
- Actualización de estadísticas desde el backend.

## 5. Uso de Angular Signals

La aplicación implementa programación reactiva mediante Angular Signals.

Se utilizan:

- `signal()` para almacenar estados y datos.
- `.set()` para actualizar valores.
- `computed()` para obtener información derivada.
- Lectura de Signals en las plantillas HTML.

Por ejemplo, el módulo de Materiales obtiene automáticamente las recolecciones completadas mediante una señal calculada.

Esta implementación permite mantener la interfaz sincronizada con los cambios de estado.

## 6. Arquitectura del sistema

La solución utiliza una arquitectura cliente-servidor organizada por responsabilidades:

**Frontend Angular**
- Interfaz de usuario.
- Formularios y tablas.
- Navegación.
- Gestión del estado.
- Consumo de la API REST.

**Backend FastAPI**
- Recepción y procesamiento de peticiones.
- Validación de datos.
- Autenticación.
- Lógica de negocio.
- Acceso a la base de datos.

**SQL Server**
- Almacenamiento de usuarios.
- Almacenamiento de familias.
- Registro de recolecciones.
- Registro de materiales.

Flujo general:

Usuario → Angular → API FastAPI → SQL Server

## 7. Estructura del repositorio

```text
EcoGestion-Huancayo/
|
|-- backend/
|   |-- src/
|   |-- crear_usuario.bat
|   |-- iniciar_backend.bat
|
|-- frontend/
|   |-- src/
|   |   |-- app/
|   |   |   |-- guards/
|   |   |   |-- pages/
|   |   |       |-- login/
|   |   |       |-- dashboard/
|   |   |       |-- familias/
|   |   |       |-- recolecciones/
|   |   |       |-- materiales/
|   |-- package.json
|   |-- angular.json
|
|-- .gitignore
|-- README.md
```

## 8. Requisitos para ejecutar el proyecto

- Windows.
- Python y las dependencias del backend.
- Node.js y npm.
- SQL Server Express.
- Controlador ODBC compatible con SQL Server.
- Git, para clonar el repositorio.

## 9. Instalación y ejecución

### 9.1. Clonar el repositorio

```powershell
git clone https://github.com/MiguelAngel-art/EcoGestion-Huancayo.git
cd EcoGestion-Huancayo
```

### 9.2. Configurar el backend

Entrar a la carpeta:

```powershell
cd backend
```

Configurar la conexión local a SQL Server Express y las variables de entorno del backend.

Entre las variables utilizadas se encuentran:

- `DB_ENGINE`
- `DB_SERVER`
- `DB_NAME`
- `DB_ODBC_DRIVER`
- `JWT_SECRET`
- `JWT_MINUTES`
- `CORS_ORIGINS`

El archivo `.env` contiene configuración local y **no se publica en GitHub**.

Ejecutar el iniciador del backend:

```powershell
.\iniciar_backend.bat
```

Una vez iniciado, la API estará disponible en:

http://127.0.0.1:8000

Documentación interactiva:

http://127.0.0.1:8000/docs

### 9.3. Crear un usuario

El proyecto cuenta con una herramienta de consola para registrar usuarios:

```powershell
.\crear_usuario.bat
```

Se debe introducir un correo, nombre, rol y contraseña.

Las contraseñas no deben incluirse en el código ni en el repositorio.

### 9.4. Instalar y ejecutar el frontend

Abrir otra terminal en la carpeta principal del proyecto:

```powershell
cd frontend
npm.cmd install
npx.cmd ng serve --configuration development --prebundle=false --no-hmr
```

Abrir en el navegador:

http://localhost:4200

El frontend requiere que el backend y SQL Server estén correctamente configurados y ejecutándose.

## 10. Seguridad

El proyecto incorpora autenticación mediante JWT y almacenamiento de contraseñas como hashes.

También considera:

- Protección de rutas.
- Validación de datos.
- Separación entre frontend y backend.
- Uso de variables de entorno.
- Exclusión de claves privadas del repositorio.

Las verificaciones de seguridad deben complementarse con pruebas del backend antes de un despliegue público.

## 11. Diseño responsive

La interfaz utiliza Bootstrap para adaptar la distribución de formularios, tablas, botones y tarjetas a diferentes tamaños de pantalla.

Se realizaron comprobaciones visuales mediante las herramientas de desarrollo del navegador.

## 12. Pruebas funcionales

Durante el desarrollo se comprobaron las siguientes operaciones:

- Inicio de sesión.
- Rechazo de credenciales incorrectas.
- CRUD de familias.
- CRUD de recolecciones.
- CRUD de materiales.
- Actualización de estadísticas del Dashboard.
- Navegación entre módulos.
- Reorganización responsive de elementos.

Los registros empleados durante estas pruebas son datos demostrativos y no representan resultados ambientales medidos en la comunidad.

## 13. Impacto social esperado

EcoGestión Huancayo busca contribuir a:

- Organizar las actividades de reciclaje.
- Facilitar el seguimiento de familias participantes.
- Registrar las cantidades de materiales recuperados.
- Mejorar la disponibilidad de información.
- Fomentar prácticas ambientales responsables.

El impacto real del sistema requerirá validación con usuarios y seguimiento de indicadores durante su aplicación.

## 14. Responsabilidad profesional

El proyecto reconoce la importancia de desarrollar soluciones tecnológicas que beneficien a la comunidad, respeten la privacidad de los usuarios y promuevan el uso responsable de la información.

La aplicación constituye una propuesta tecnológica académica con potencial para su ampliación y mejora.

## 15. Estado del proyecto

Versión académica funcional.

Módulos principales implementados:
- Login.
- Dashboard.
- Familias.
- Recolecciones.
- Materiales.

Tecnologías principales: Angular, FastAPI y SQL Server.

---

**EcoGestión Huancayo — Programación Web, 2026**
