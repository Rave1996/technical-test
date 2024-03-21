# Prueba técnica para Python Backend Developer MID

Desarrolla un módulo para una entidad financiera que ofrece préstamos en línea. Este módulo gestionará clientes y préstamos, permitiendo crear, editar, visualizar y eliminar registros a través de endpoints. Los datos se almacenarán en una base de datos.


## Requerimientos del sistema:
- Tener instalado docker, python 3
- Un IDE de desarrollo


## Requerimientos funcionales:
1. Creación de endpoints `(API REST)` para la gestión de los `clientes`:
  - Se debe desarrollar una API REST que permita realizar operaciones CRUD (Crear, Leer, Actualizar y Eliminar) sobre los datos de los clientes.
  - Los endpoints a implementar son:
    - `Create`: Permite crear un nuevo cliente en la base de datos.
    - `List`: Devuelve una lista de todos los clients existentes.
    - `Retrieve`: Obtiene los detalles de un cliente específico.
    - `Update`: Actualiza la información de un cliente existente.
    - `Delete`: Elimina un cliente de la base de datos.
2. Creación de los endpoints `(API REST)` para la gestión de los `préstamos` a un cliente.
  - Se debe desarrollar una API REST que permita realizar operaciones CRUD (Crear, Leer, Actualizar y Eliminar) sobre los datos de los clientes.
  - Los endpoints a implementar son:
    - `Create`: Permite crear un nuevo préstamo para un cliente, en la base de datos.
    - `List`: Devuelve una lista de todos los préstamo existentes.
    - `Retrieve`: Obtiene los detalles de un préstamo específico.
    - `Update`: Actualiza la información de un préstamo existente.
    - `Delete`: Elimina un préstamo de la base de datos.
3. Pruebas Unitarias:
   - Se deben escribir pruebas unitarias para garantizar el correcto funcionamiento de los endpoints de la API.
   - Se utilizarán frameworks de pruebas como `unittest` o `pytest` para crear y ejecutar las pruebas.

## Requerimientos Opcionales:
1. Mejorar los endpoints de tipo List
   - Implementar filtrado en la búsqueda
   - Implementar paginación
2. Documentar el Código
3. Crear una collection en postman (o alguna herramienta similar) de los endpoints creados
4. Factory para insertar datos de prueba en los modelos de tu sistema
5. Autenticación y Autorización: Implementar un sistema de autenticación (por ejemplo, utilizando tokens JWT) para controlar el acceso a la API.
   - Esto puede incluir roles de usuario diferentes, como administrador y usuario regular, con diferentes niveles de acceso.
   - Endpoint para hacer login y obtener el token

## Entregables
1. URL del repositorio público en github, gitlab, o el de tu preferencia
2. Diagrama de Entidad-Relación


## <span style="color: #dc3545;">Importante</span>
Tiempo para completar el ejercicio
- Se dispone de un plazo máximo de 3 días para completar el ejercicio y enviar la respuesta.
- Si no se logra finalizar dentro del tiempo establecido, no te preocupes, no hay ningún problema; por favor envíanos tu progreso. Lo importante es intentarlo.

Además, comprendemos que la agenda puede ser exigente:
- Si consideras que cuentas con las habilidades y aptitudes necesarias, también es aceptable presentarte sin haber completado el ejercicio previo. Solo avísanos para estar al tanto e ir al siguiente paso.

Si tienes alguna duda del ejercicio escríbenos a los correos:
- marlenlc@getfairplay.com
- luisph@getfairplay.com
