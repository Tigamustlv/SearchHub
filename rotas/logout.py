from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

from rotas.dependencias import (
    UsuarioRepositorio,
    obter_usuario_repositorio
)

from logs.auditoria import registrar



router = APIRouter(
    prefix="/logout"
)



@router.get("/")
async def logout(

    request: Request,

    usuario_repositorio: Annotated[
        UsuarioRepositorio,
        Depends(obter_usuario_repositorio)
    ]

):


    token = request.cookies.get(
        "session_token"
    )



    if token:


        usuario = await usuario_repositorio.buscar_usuario_por_token(
            token
        )



        if usuario:


            # SALVA DATA/HORA DO LOGOUT
            await usuario_repositorio.registrar_logout(
                usuario.id_
            )



            registrar(
                request,
                "LOGOUT",
                f"email={usuario.email}",
                usuario=usuario
            )



        # REMOVE A SESSÃO ATIVA
        await usuario_repositorio.remover_sessao(
            token
        )



    response = RedirectResponse(
        url="/login/",
        status_code=303
    )



    response.delete_cookie(
        key="session_token"
    )


    response.delete_cookie(
        key="nivel"
    )



    return response