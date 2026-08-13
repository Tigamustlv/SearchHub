from starlette.middleware.base import BaseHTTPMiddleware
from logs.logger import logger


class AuditoriaMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        response = await call_next(request)


        usuario = getattr(
            request.state,
            "usuario",
            None
        )


        if usuario:

            ip = request.client.host

            logger.info(
                f"usuario={usuario.email} | "
                f"nivel={usuario.nivel} | "
                f"ip={ip} | "
                f"{request.method} {request.url.path}"
            )


        return response