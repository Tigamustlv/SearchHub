from logs.logger import logger


def registrar(request, acao, detalhes="", usuario=None):

    # Se não foi informado, tenta pegar do middleware
    if usuario is None:
        usuario = getattr(
            request.state,
            "usuario",
            None
        )


    if usuario:

        logger.info(
            f"usuario={usuario.email} | "
            f"nivel={usuario.nivel} | "
            f"acao={acao} | "
            f"{detalhes}"
        )

    else:

        ip = request.client.host

        logger.info(
            f"usuario=NAO_IDENTIFICADO | "
            f"ip={ip} | "
            f"acao={acao} | "
            f"{detalhes}"
        )