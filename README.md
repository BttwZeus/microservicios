Proyecto de Microservicios
Nombre: Zeus Aguirre

Carrera: Ingeniería de Software (6to Semestre)

Materia: Diseno y Arquitectura de Software

Fecha: Abril 2026

Introducción
En esta tarea pasamos una aplicación que estaba en un solo bloque (monolito) a un esquema de microservicios usando Docker. La idea era ver cómo separar las tareas pesadas para que el sistema no se trabe cuando muchos usuarios intentan registrarse al mismo tiempo.

El Problema con el Monolito
Cuando probé el monolito con el comando ab de Apache, los tiempos de respuesta estaban por los 730-740ms. Esto pasaba porque el servidor tenía que guardar al usuario en la base de datos y al mismo tiempo procesar una "notificación pesada". Si una parte fallaba o tardaba, toda la página se quedaba cargando.

Mi Arquitectura
Separé el código en dos carpetas: servicio_a y servicio_b.

Servicio A: Es el que ve el usuario. Recibe el nombre y el correo, lo guarda en la tabla usuarios_aguirre de RDS y luego le avisa al Servicio B por una petición HTTP interna.

Servicio B: Este corre por detrás. Recibe el aviso del Servicio A y guarda un log en la tabla logs_procesamiento. Simula ser un proceso que tarda, pero como es un microservicio aparte, no detiene al primero.

Base de Datos (AWS RDS)
Usé MariaDB en AWS. Creé una base de datos llamada db_aguirre con estas dos tablas:

usuarios_aguirre: Para los registros principales.

logs_procesamiento: Para los eventos del Servicio B.

Pruebas de Resiliencia
Lo mejor de este diseño es que si apago el Servicio B, el Servicio A sigue funcionando. El usuario puede registrarse y le sale un mensaje de que el sistema de notificaciones está en mantenimiento, pero su registro sí se guarda. Esto en el monolito hubiera mandado un error 500 y no dejaría hacer nada.

Cómo correrlo
Para levantar todo el proyecto usé:

Bash
sudo docker-compose up --build -d
Y para revisar que los dos contenedores estén arriba:

Bash
sudo docker ps
Conclusión
Lo más difícil fue configurar el docker-compose.yml y las reglas de red en AWS, pero al final funcionó. Los microservicios son mejores para aplicaciones que necesitan estar siempre activas, aunque el código se vuelve un poco más complejo de conectar.
