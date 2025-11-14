# ProyectoFinal_Equipo1
Repositorio oficial del proyecto final del equipo 1, curso Desarrollo de Software Empresarial.

Equipo 1500 Equipo #1

Integrantes:      
Yeyson Elber Aguilar Echeverria

David Alexander Borja Abrego

Heriberto Josue Echeverria Cardona 

Marco Antonio Orellana Guardado 

Ludy Amarillis Pineda Lemus 

Jennifer Susana Ruiz Mendez 


-----------------------------------------------------------------------------------------------------------------

Usuarios GitHub:  
yeysonecheverria07

David69-code

HeriJosue123

Marcuz097

LudyAP14

jenniruiz0820

------------------------------------------------------------------------------------------------------------------

PRIMEROS AVANCES DEL PROYECTO 

Fecha: 15 / 10 /  2025

Creacion del proyecto 

Creacion de core 

Migraciones a la base de datos y conexion a ella 

Creacion de tablas en el models 

-------------------------------------------------------------------------------------------------------------------
AVANCES DEL PROYECTO HASTA EL MOMENTO 
Fecha: 22/ 10 / 2025

Core: maneja la autenticación de usuarios, registro e inicio de sesión, así como la asignación de roles (administrador, médico y paciente).

Gestión de Citas: implementa el CRUD de las entidades principales del sistema (Pacientes, Médicos, Especialidades y Citas).

Hasta este punto, se ha logrado:

Configuración completa del entorno Django y base de datos.

Implementación de vistas basadas en clases para las operaciones CRUD.

Formularios dinámicos con ModelForm para facilitar la gestión de datos.

Plantillas HTML integradas con Bootstrap para la interfaz de usuario.

Enrutamiento funcional entre módulos y control básico de acceso por roles.

Próximos pasos:

Mejorar la personalización de la interfaz por tipo de usuario.

Implementar filtros de citas según el rol (paciente o médico).

Agregar validaciones y control de permisos más específicos.


------------------------------------------------------------------------------------------------------------------

NUEVOS AVANCES DEL PROYECTO HASTA EL MOMENTO

Fecha: 31 / 10 / 2025

En esta versión del proyecto se han implementado diversas mejoras y nuevas características que amplían la funcionalidad general del sistema:

🔧 Funcionalidades incorporadas

Gestión avanzada de usuarios:
Se mejoró el control de roles (Administrador, Médico y Paciente), con permisos específicos para cada tipo de usuario.

Módulo de gestión de citas actualizado:
Se optimizó el CRUD de Citas, permitiendo validar fechas y horarios disponibles, así como mostrar los datos relacionados de médicos y pacientes.

Interfaz mejorada:
Se aplicaron estilos adicionales con Bootstrap y plantillas reutilizables para lograr una apariencia más profesional y consistente.

Mensajes de retroalimentación:
Se incorporaron mensajes de éxito y error dinámicos al realizar operaciones CRUD.

Filtros y búsquedas:
Se añadieron filtros por especialidad, médico o paciente para facilitar la administración de las citas.

Navegación y seguridad:
Se mejoró el enrutamiento, la protección de vistas con decoradores @login_required, y la validación de acceso por tipo de usuario.

Conexión estable con base de datos:
Se optimizó la configuración del entorno y los modelos para un mejor rendimiento y estabilidad en consultas.

