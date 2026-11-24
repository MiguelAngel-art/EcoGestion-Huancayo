
# Manual de Usuario
## EcoGestión Huancayo 🌱

**Curso:** Programación Web  
**Año:** 2026

### 1. Presentación

EcoGestión Huancayo es una aplicación web que desarrollamos para facilitar el registro de familias que participan en actividades de reciclaje, organizar las recolecciones y conocer la cantidad de materiales recuperados.

Este manual explica cómo utilizar las funciones principales del sistema.

### 2. Ingreso al sistema

Para utilizar la aplicación, primero debemos tener el backend y el frontend funcionando.

Abrimos el navegador e ingresamos a:

http://localhost:4200

En la pantalla de inicio de sesión escribimos nuestro correo y contraseña.

Si los datos son correctos, ingresaremos al panel de control. Si son incorrectos, aparecerá un mensaje de error.

### 3. Panel de control

Al ingresar al sistema encontramos el Dashboard o panel de control.

En esta pantalla podemos observar:

- Cantidad de familias registradas.
- Número de recolecciones completadas.
- Total de kilogramos de materiales recuperados.

También encontramos botones para ingresar a los módulos de Familias, Recolecciones y Materiales.

El botón "Actualizar datos" permite consultar nuevamente las estadísticas.

### 4. Gestión de familias

Para administrar las familias:

1. Ingresamos al módulo "Familias".
2. Seleccionamos la opción para registrar una nueva familia.
3. Completamos los datos solicitados.
4. Guardamos la información.

La familia aparecerá en la lista de registros.

Si necesitamos corregir algún dato, utilizamos el botón "Editar".

También podemos eliminar una familia cuando el sistema lo permita. Si tiene recolecciones relacionadas, debemos respetar las restricciones de la base de datos.

### 5. Gestión de recolecciones

En este módulo podemos registrar las actividades de recolección.

Para agregar una:

1. Entramos a "Recolecciones".
2. Seleccionamos la opción de nuevo registro.
3. Elegimos una familia registrada.
4. Indicamos la fecha.
5. Seleccionamos el estado de la recolección.
6. Agregamos una observación cuando corresponda.
7. Guardamos la información.

También podemos editar o eliminar registros cuando esté permitido.

### 6. Gestión de materiales

En este módulo registramos los materiales reciclables asociados a una recolección completada.

Para registrar un material:

1. Entramos a "Materiales".
2. Presionamos "Nuevo material".
3. Seleccionamos una recolección completada.
4. Elegimos el tipo de material.
5. Ingresamos la cantidad en kilogramos.
6. Indicamos la fecha del registro.
7. Guardamos.

El sistema permite trabajar con plástico, papel, cartón y vidrio.

También podemos editar cantidades o eliminar un registro.

Los cambios realizados se reflejan en las estadísticas del Dashboard cuando actualizamos los datos.

### 7. Actualización de estadísticas

Después de registrar o modificar materiales:

1. Regresamos al Dashboard.
2. Presionamos "Actualizar datos".
3. Revisamos la cantidad total de kilogramos recuperados.

De esta manera podemos comprobar que el sistema está utilizando los registros guardados en la base de datos.

### 8. Diseño de las pantallas

La aplicación fue desarrollada utilizando Angular y Bootstrap.

Probamos la distribución de los elementos con las herramientas del navegador, reduciendo el ancho de la pantalla para comprobar que las tarjetas y los botones se reorganizaran.

### 9. Cerrar sesión

Cuando terminamos de utilizar el sistema, presionamos el botón "Cerrar sesión".

Esto nos devuelve a la pantalla de inicio de sesión.

### 10. Recomendaciones

- No compartir las contraseñas de acceso.
- Registrar información correcta.
- Revisar los datos antes de guardarlos.
- Evitar eliminar registros importantes.
- Cerrar sesión al terminar de utilizar el sistema.

### 11. Conclusión

EcoGestión Huancayo nos permite organizar la información de familias, recolecciones y materiales reciclables desde una sola aplicación.

Mediante sus diferentes módulos podemos registrar, consultar, modificar y eliminar información, además de visualizar estadísticas relacionadas con el reciclaje.

Este proyecto demuestra cómo podemos aplicar lo aprendido en Programación Web para desarrollar una propuesta que contribuya al cuidado del medio ambiente.
