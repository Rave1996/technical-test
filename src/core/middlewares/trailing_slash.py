from urllib.parse import urlencode, urlunparse

from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware


class TrailingSlashMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path.endswith("/") and request.query_params:
            new_path = request.url.path[:-1]
            new_url = urlunparse(
                (
                    request.url.scheme,
                    request.url.netloc,
                    new_path,
                    "",
                    urlencode(request.query_params._dict),  # noqa: SLF001
                    "",
                )
            )
            return RedirectResponse(url=new_url, status_code=308)

        elif request.url.path.endswith("/"):  # noqa: RET505
            new_path = request.url.path[:-1]
            return RedirectResponse(url=new_path, status_code=308)

        return await call_next(request)
