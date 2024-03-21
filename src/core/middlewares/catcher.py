from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware

from core.utils.exceptions import ObjectNotFound
from core.utils.responses import EnvelopeResponse


class CatcherExceptionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except HTTPException as http_exception:
            return JSONResponse(
                status_code=http_exception.status_code,
                content={
                    "error": "Client Error",
                    "message": str(http_exception.detail),
                },
            )
        except ObjectNotFound as object_no_found:
            response = EnvelopeResponse(errors=object_no_found.args, body=None)
            logger.exception(response)
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=dict(response))
        except ValidationError as errors:
            response = EnvelopeResponse(errors=[error.get("msg") for error in errors.errors()])
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=dict(response),
            )
        except Exception as error:
            logger.error("-" * 80)
            logger.info(error)
            logger.error("-" * 80)
            response = EnvelopeResponse(errors=error.args, body=None)
            logger.exception(response)
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=dict(response))
