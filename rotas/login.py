from typing import Annotated

from fastapi import APIRouter, Form, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from rotas.dependencias import (
    UsuarioRepositorio,
    obter_usuario_repositorio
)

from logs.auditoria import registrar



router = APIRouter(
    prefix="/login"
)



templates = Jinja2Templates(
    directory="templates"
)



@router.get("/", response_class=HTMLResponse)
async def pagina_login(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )





@router.post("/")
async def login(

    usuario_repositorio: Annotated[
        UsuarioRepositorio,
        Depends(obter_usuario_repositorio)
    ],

    request: Request,

    email=Form(...),

    senha=Form(...),

):


    registrar(
        request,
        "ACESSO_LOGIN"
    )



    usuario = await usuario_repositorio.buscar_usuario_por_cred(
        email,
        senha
    )



    if usuario:



        if usuario.nivel == "pendente" or not usuario.nivel:


            registrar(
                request,
                "LOGIN_BLOQUEADO",
                f"email={usuario.email} motivo=nivel_pendente"
            )


            return templates.TemplateResponse(
                request=request,
                name="login.html",
                context={
                    "email": email,
                    "error": "Usuário aguardando aprovação"
                }
            )




        # REGISTRA DATA E IP DO LOGIN
        await usuario_repositorio.registrar_login(
            usuario.id_,
            request.client.host
        )



        token = await usuario_repositorio.criar_sessao(
            usuario.id_
        )



        registrar(
            request,
            "LOGIN",
            f"email={usuario.email}",
            usuario=usuario
        )



        response = RedirectResponse(
            url="/menu",
            status_code=303
        )



        response.set_cookie(
            key="session_token",
            value=token,
            httponly=True
        )


        return response





    registrar(
        request,
        "LOGIN_FALHA",
        f"email_tentado={email}"
    )



    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "email": email,
            "error": "Credenciais invalidas"
        }
    )