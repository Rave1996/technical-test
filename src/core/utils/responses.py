from typing import Any

from fastapi import Query
from fastapi_pagination import Params
from pydantic import BaseModel

from core.settings import settings


class PaginationParams(Params):
    size: int = Query(None, ge=1, le=500, description="Page size")


class EnvelopeResponse(BaseModel):
    errors: Any = None
    body: Any = None


def default_pagination_params(
    page: int = Query(1, ge=1, alias="page", description="Page number"),
    size: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=500, alias="page_size", description="Page size"),
) -> PaginationParams:
    return PaginationParams(page=page, size=size)
