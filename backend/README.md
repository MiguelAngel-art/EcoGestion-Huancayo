
# EcoGestión Huancayo 🌱

## Backend del sistema de reciclaje

### 1. ¿De qué trata el proyecto?

EcoGestión Huancayo es un proyecto que desarrollamos para el curso de Programación Web.

La idea surgió porque el reciclaje es una actividad importante para cuidar nuestro medio ambiente, pero muchas veces no se lleva un buen registro de las familias que participan, de las recolecciones que se realizan ni de la cantidad de materiales recuperados.

Por eso, desarrollamos una aplicación web que permite organizar esta información de manera sencilla.

El sistema está pensado como una propuesta tecnológica que puede ayudar a mejorar la organización de las actividades de reciclaje en Huancayo.

### 2. Objetivo del proyecto

Nuestro objetivo es desarrollar un sistema web que permita registrar familias, controlar las recolecciones de residuos reciclables y conocer la cantidad de materiales recuperados.

También buscamos demostrar cómo la programación puede utilizarse para ayudar a solucionar problemas de nuestra comunidad.

### 3. Herramientas que utilizamos

Para desarrollar nuestro proyecto utilizamos las siguientes tecnologías:

- **Angular:** para crear las pantallas que utiliza el usuario.
- **Bootstrap:** para mejorar el diseño y adaptar las pantallas a diferentes tamaños.
- **Python y FastAPI:** para desarrollar la parte que procesa la información del sistema.
- **SQL Server Express:** para guardar los datos de manera organizada.
- **Visual Studio Code:** para escribir y trabajar con nuestro código.
- **Git y GitHub:** para guardar y compartir los avances del proyecto.

También utilizamos Angular Signals para actualizar la información de algunas pantallas.

### 4. ¿Qué funciones tiene nuestro sistema?

El proyecto cuenta con los siguientes módulos:

**Inicio de sesión**

Permite ingresar al sistema utilizando un correo electrónico y una contraseña.

**Gestión de familias**

Permite registrar nuevas familias, visualizar su información, modificar sus datos y eliminar registros cuando corresponda.

**Gestión de recolecciones**

Permite registrar las recolecciones realizadas o programadas, asignarlas a una familia y actualizar su estado.

**Gestión de materiales**

Permite registrar materiales como plástico, papel, cartón y vidrio. También se puede indicar cuántos kilogramos se recuperaron en cada recolección.

**Panel de control**

Muestra un resumen con la cantidad de familias registradas, las recolecciones completadas y los kilogramos recuperados.

Los datos del panel se actualizan cuando realizamos cambios en los registros.

### 5. ¿Cómo funciona?

Nuestro sistema está dividido en tres partes principales.

La primera es Angular, donde el usuario puede ingresar y utilizar las diferentes opciones.

La segunda es FastAPI, que recibe las solicitudes, revisa la información y realiza las operaciones correspondientes.

La tercera es SQL Server, donde se almacenan los datos registrados.

Estas tres partes trabajan juntas para que la información que ingresamos en las pantallas se guarde correctamente y pueda consultarse después.

### 6. ¿Qué necesito para ejecutar el proyecto?

Para ejecutar el sistema en una computadora con Windows es necesario tener instalado:

- Python 3.11 o superior.
- Node.js y npm.
- SQL Server Express.
- ODBC Driver 18 for SQL Server.
- Git para descargar el repositorio.

También recomendamos utilizar Visual Studio Code y SQL Server Management Studio.

### 7. Preparar la base de datos

Primero debemos abrir SQL Server Management Studio y conectarnos a SQL Server Express.

Durante el desarrollo utilizamos la instancia:

`.\SQLEXPRESS`

Después debemos crear una base de datos con el nombre:

`EcoGestionHuancayo`

Podemos utilizar esta consulta:

```sql
IF DB_ID(N'EcoGestionHuancayo') IS NULL
BEGIN
    CREATE DATABASE [EcoGestionHuancayo];
END;
```

Al iniciar el backend, el programa crea las tablas necesarias mediante SQLAlchemy y registra los tipos de materiales iniciales.

Es importante que el usuario de Windows tenga permisos para acceder a la base de datos.

### 8. ¿Cómo iniciar el backend?

Primero descargamos el proyecto desde GitHub:

```powershell
git clone https://github.com/MiguelAngel-art/EcoGestion-Huancayo.git
```

Luego ingresamos a la carpeta del backend:

```powershell
cd EcoGestion-Huancayo
cd backend
```

Ejecutamos:

```powershell
.\iniciar_backend.bat
```

Este archivo ayuda a preparar Python, instalar las dependencias necesarias y ejecutar FastAPI.

La primera vez también genera un archivo de configuración local llamado `.env`.

Si SQL Server está configurado correctamente, podemos abrir:

http://127.0.0.1:8000/docs

En esa dirección encontraremos las diferentes funciones de nuestra API.

También podemos comprobar que el servidor funciona ingresando a:

http://127.0.0.1:8000/health

### 9. Crear un usuario

Para ingresar al sistema primero necesitamos registrar un usuario.

Abrimos otra terminal dentro de la carpeta `backend` y ejecutamos:

```powershell
.\crear_usuario.bat
```

El programa nos pedirá:

- Correo electrónico.
- Nombre.
- Rol de usuario.
- Contraseña.

La contraseña debe tener como mínimo 10 caracteres.

Después de registrar al usuario, podremos iniciar sesión desde Angular.

### 10. ¿Cómo iniciar Angular?

Abrimos otra terminal y entramos a la carpeta `frontend` del proyecto.

Instalamos los paquetes necesarios:

```powershell
npm.cmd install
```

Después iniciamos Angular:

```powershell
npx.cmd ng serve --configuration development --prebundle=false --no-hmr
```

Finalmente, abrimos en el navegador:

http://localhost:4200

Desde allí podremos iniciar sesión y utilizar los módulos del sistema.

Para que todo funcione correctamente, SQL Server y FastAPI deben estar ejecutándose.

### 11. Seguridad del sistema

Durante el desarrollo también tuvimos en cuenta la seguridad de la información.

Por ejemplo, el ingreso se realiza con correo y contraseña, y el backend utiliza tokens para verificar las solicitudes de los usuarios.

Las contraseñas se almacenan mediante hashes y no directamente como texto.

Además, utilizamos un archivo `.env` para guardar información de configuración que no debe publicarse en GitHub.

Estas medidas forman parte de la seguridad básica del proyecto académico.

### 12. Pruebas que realizamos

Durante el desarrollo fuimos comprobando que las principales funciones trabajaran correctamente.

Probamos el inicio de sesión y verificamos que las contraseñas incorrectas fueran rechazadas.

También registramos, modificamos y eliminamos familias, recolecciones y materiales.

Una de las pruebas fue registrar diferentes materiales reciclables y verificar que el Dashboard mostrara correctamente el total de kilogramos.

Asimismo, comprobamos que, al reducir el tamaño de la pantalla desde las herramientas del navegador, los elementos se reorganizaran.

Los datos utilizados en estas pruebas son ejemplos para demostrar el funcionamiento del sistema.

### 13. Importancia de nuestro proyecto

Consideramos que EcoGestión Huancayo es una propuesta útil porque muestra cómo la tecnología puede ayudar a organizar actividades relacionadas con el cuidado del medio ambiente.

Aunque actualmente es un proyecto académico, puede servir como base para desarrollar una herramienta que se utilice en programas de reciclaje de nuestra comunidad.

También nos permitió poner en práctica lo aprendido durante el curso, trabajando con diferentes herramientas de programación y una base de datos real.

### 14. Conclusión

Con el desarrollo de EcoGestión Huancayo logramos crear una aplicación web que permite administrar familias, recolecciones y materiales reciclables.

Aprendimos a conectar Angular con FastAPI y SQL Server, además de implementar formularios, operaciones CRUD, autenticación y estadísticas.

Este proyecto nos ayudó a comprender mejor cómo desarrollar un sistema web y cómo aplicar nuestros conocimientos para proponer soluciones a problemas de nuestro entorno.

---

**Proyecto académico: EcoGestión Huancayo**

**Asignatura: Programación Web**

**Año: 2026**
