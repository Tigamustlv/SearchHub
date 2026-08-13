from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from rotas.dependencias import (
    UsuarioRepositorio,
    obter_usuario_repositorio
)

from autorizacao import verificar_nivel


router = APIRouter()


templates = Jinja2Templates(
    directory="templates"
)



@router.get("/admin")
async def painel_admin(
    request: Request,
    usuario_repositorio: Annotated[
        UsuarioRepositorio,
        Depends(obter_usuario_repositorio)
    ]
):


    acesso = verificar_nivel(
        request,
        ["admin"]
    )


    if acesso:
        return acesso



    usuarios = await usuario_repositorio.listar_usuarios()



    # ==========================
    # CARREGAR LOG DO SISTEMA
    # ==========================

    caminho_log = Path("logs/sistema.log")


    if caminho_log.exists():

        with open(
            caminho_log,
            "r",
            encoding="utf-8"
        ) as arquivo:

            logs = arquivo.readlines()


    else:

        logs = [
            "Arquivo sistema.log não encontrado."
        ]



    logs = logs[-100:]



    return templates.TemplateResponse(

        request=request,

        name="admin.html",

        context={

            "usuarios": usuarios,

            "logs": logs

        }

    )





@router.post("/admin/aprovar/{usuario_id}")
async def aprovar_usuario(

    usuario_id: int,

    request: Request,

    usuario_repositorio: Annotated[
        UsuarioRepositorio,
        Depends(obter_usuario_repositorio)
    ]

):


    acesso = verificar_nivel(
        request,
        ["admin"]
    )


    if acesso:
        return acesso



    await usuario_repositorio.alterar_nivel(

        usuario_id,

        "operacional"

    )


    return RedirectResponse(

        "/admin",

        status_code=303

    )





@router.post("/admin/remover-sessao/{usuario_id}")
async def remover_sessao(

    usuario_id:int,

    request:Request,

    usuario_repositorio: Annotated[
        UsuarioRepositorio,
        Depends(obter_usuario_repositorio)
    ]

):


    acesso = verificar_nivel(
        request,
        ["admin"]
    )


    if acesso:
        return acesso



    await usuario_repositorio.remover_sessao_usuario(
        usuario_id
    )


    return RedirectResponse(
        "/admin",
        status_code=303
    )