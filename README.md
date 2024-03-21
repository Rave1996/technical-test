# Python Backend Developer MID

Este es un proyecto que utiliza FastAPI como framework web y PostgreSQL como base de datos, todo en contenedores Docker.
Proporciona una estructura básica para comenzar a desarrollar una aplicación web con Python.

## Requisitos previos
- Docker: Instalación de Docker
- Docker Compose: Instalación de Docker Compose


## Instrucciones de instalación

Crea un archivo `.env` en el directorio raíz del proyecto y configura las variables de entorno necesarias.
Puedes copiar el archivo .env.example y modificarlo según tus necesidades:

```bash
cp .env.example .env
```

Tienes un comandos de Makefile que te pueden ser de ayuda:

```
Usage: make <target>

app          Run app with docker
clean        Remove all temporary files like pycache
help         show the help
install      Install and setup project dependencies
lint         Run linters
start        Init development server
test         Run all the tests with docker
update_libs  update libs + generate new lockfile & requirements
virtualenv   Create a virtual environment.
```

es decir, que si quieres levantar el proyecto con docker, solo debes ejecutar el comando

```bash
make app
```

Esto iniciará los contenedores de FastAPI y PostgreSQL en segundo plano.


### Accede a FastAPI en tu navegador:
- FastAPI: http://localhost:8000
- Documentación Swagger de FastAPI: http://localhost:8000/docs
- Documentación ReDoc de FastAPI: http://localhost:8000/redoc

## Estructura del proyecto

```
.
├── Makefile
├── README.md
├── docker-compose.yml
├── envs.sh
├── poetry.lock
├── pyproject.toml
└── src
    ├── __init__.py
    ├── api
    │   ├── __init__.py
    │   ├── healthcheck
    │   │   ├── __init__.py
    │   │   ├── endpoints.py
    │   │   ├── schemas.py
    │   │   └── tests
    │   │       ├── __init__.py
    │   │       └── test_endpoints.py
    │   ├── routers.py
    │   └── v1
    │       ├── __init__.py
    │       ├── costumers
    │       │   ├── __init__.py
    │       │   ├── endpoints.py
    │       │   └── tests
    │       │       └── __init__.py
    │       └── loans
    │           ├── __init__.py
    │           ├── endpoints.py
    │           └── tests
    │               └── __init__.py
    ├── core
    │   ├── __init__.py
    │   ├── middlewares
    │   │   ├── __init__.py
    │   │   ├── catcher.py
    │   │   └── trailing_slash.py
    │   ├── settings
    │   │   ├── __init__.py
    │   │   └── base.py
    │   └── utils
    │       ├── __init__.py
    │       ├── datetime.py
    │       ├── exceptions.py
    │       ├── responses.py
    │       └── validations.py
    ├── db
    │   ├── __init__.py
    │   ├── models
    │   │   ├── __init__.py
    │   │   ├── base.py
    │   │   └── models.py
    │   ├── session.py
    │   └── utils.py
    ├── main.py
    └── tests
        ├── __init__.py
        └── unit
```

`19 directories, 42 files`


- `src/`: Es el directorio principal que contiene todo el código de la aplicación.
- `api/`: Contiene los módulos relacionados con la API de la aplicación.
- `core/`: Contiene los módulos centrales de la aplicación, como configuraciones y utilidades.
- `db/`: Contiene los módulos relacionados con la base de datos, incluyendo la definición de modelos y configuración de sesiones.
- `tests/`: Es el directorio para las pruebas de la aplicación.
- `Makefile`: Archivo para definir comandos y tareas comunes.
- `README.md`: Documentación del proyecto.
- `docker-compose.yml`: Archivo de configuración para ejecutar la aplicación con Docker Compose.
- `poetry.lock y pyproject.toml`: Archivos generados por Poetry para manejar las dependencias del proyecto.
