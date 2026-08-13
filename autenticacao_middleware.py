from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

from database.local import BancoDeDadosLocal
from database.usuario_repositorio import UsuarioRepositorio


banco = BancoDeDadosLocal("usuarios.db")


class AuthenticationToken(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        path = request.url.path

        if (
            path == "/"
            or path.startswith("/login")
            or path.startswith("/registro")
            or path.startswith("/static")
        ):
            return await call_next(request)


        token = request.cookies.get("session_token")


        if not token:
            return RedirectResponse("/", status_code=303)


        repositorio = UsuarioRepositorio(banco)

        usuario = await repositorio.buscar_usuario_por_token(token)


        if not usuario:
            return RedirectResponse("/", status_code=303)


        request.state.usuario = usuario


        return await call_next(request)