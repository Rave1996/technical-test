from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi_pagination import add_pagination
from loguru import logger

from api import routers
from core.middlewares.catcher import CatcherExceptionMiddleware
from core.middlewares.trailing_slash import TrailingSlashMiddleware
from core.settings import settings
from core.utils.validations import validation_pydantic_field
from db.utils import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    logger.success("Start app")
    init_db()
    yield


def create_application() -> FastAPI:
    application = FastAPI(
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
        middleware=[
            Middleware(CatcherExceptionMiddleware),
            Middleware(TrailingSlashMiddleware),
        ],
        redirect_slashes=False,
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(routers.healthcheck_router)
    application.include_router(routers.api_v1_router)
    add_pagination(application)

    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        routes=application.routes,
    )
    application.openapi_schema = openapi_schema

    return application


app = create_application()
validation_pydantic_field(app)
