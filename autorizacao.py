from fastapi import Request
from fastapi.responses import RedirectResponse


def verificar_nivel(request: Request, niveis: list[str]):

    usuario = getattr(request.state, "usuario", None)

    if not usuario:
        return RedirectResponse("/", status_code=303)

    if usuario.nivel not in niveis:
        return RedirectResponse("/menu", status_code=303)

    return None