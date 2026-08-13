from typing import Annotated
from fastapi import Depends

from database.local import BancoDeDadosLocal
from database.usuario_repositorio import UsuarioRepositorio

banco_de_dados = BancoDeDadosLocal("usuarios.db")

def obter_banco_de_dados() -> BancoDeDadosLocal:
    return banco_de_dados



def obter_usuario_repositorio( 
        banco_de_dados_local: Annotated[BancoDeDadosLocal, 
                                        Depends(obter_banco_de_dados)]) -> UsuarioRepositorio:
    return UsuarioRepositorio(banco_de_dados_local)
