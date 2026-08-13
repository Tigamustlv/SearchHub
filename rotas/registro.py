from typing import Annotated

from fastapi import APIRouter, Form, Depends, HTTPException
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates


from rotas.dependencias import UsuarioRepositorio, obter_usuario_repositorio
from modelos.usuario import UsuarioCriarAtualizar


router = APIRouter(
    prefix="/registro"
)


templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def pagina_registro(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="registro.html",
        context={}
    )


@router.post("/")
async def registrar_usuario(
    usuario_repositorio: Annotated[UsuarioRepositorio, Depends(obter_usuario_repositorio)],
    request: Request,
    nome = Form(...),
    email = Form(...), 
    senha = Form(...),
    confirma_senha = Form(...),
):
    
    data = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "confirma_senha": confirma_senha,
    }

    if not all([email, senha, nome, confirma_senha]):
        return templates.TemplateResponse("registro.html", {
            "request": request,
            "error": "Campos obrigatórios faltantes",
            **data
        })


    usuario_existente = await usuario_repositorio.buscar_usuario_por_email(email)

    if usuario_existente:
        return templates.TemplateResponse(
            "registro.html",
            {
                "request": request,
                "error": "Usuário inválido!",
                **data
            }
        )


    usuario_criar = UsuarioCriarAtualizar(
        nome=nome,
        email=email,
        senha=senha,
        nivel="pendente"
    )

    usuario = await usuario_repositorio.criar_usuario(usuario_criar)

    if usuario:
        response = RedirectResponse(url="/login", status_code=303)
        return response
