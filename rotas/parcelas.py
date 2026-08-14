from fastapi import APIRouter, Request, HTTPException
from datetime import date, datetime
from decimal import Decimal, InvalidOperation

import mariadb

from modelos.usuario import (
    ParcelaResponse,
    ParcelasResponse
)

from database.mariadb import obter_conexao

from logs.logger import logger


router = APIRouter()


def converter_decimal(valor):

    if valor is None:
        return None

    if isinstance(valor, Decimal):
        return valor

    valor = str(valor).strip()

    if not valor:
        return None

    valor = (
        valor
        .replace("R$", "")
        .replace("r$", "")
        .replace(" ", "")
    )

    if not valor:
        return None

    try:

        if "." in valor and "," in valor:

            valor = valor.replace(".", "")
            valor = valor.replace(",", ".")

        elif "," in valor:

            valor = valor.replace(",", ".")


        return Decimal(valor)

    except (InvalidOperation, ValueError):

        return None


def converter_data(valor):

    if valor is None:
        return None

    if isinstance(valor, datetime):
        return valor.date()

    if isinstance(valor, date):
        return valor

    valor = str(valor).strip()

    if not valor:
        return None

    # Normaliza espaços
    valor = " ".join(valor.split())

    # Tenta ISO diretamente
    try:

        valor_iso = valor.replace("Z", "+00:00")

        return datetime.fromisoformat(
            valor_iso
        ).date()

    except ValueError:
        pass

    formatos = [

        # 2026-01-15
        "%Y-%m-%d",

        # 2026-01-15 00:00:00
        "%Y-%m-%d %H:%M:%S",

        # 2026-01-15 00:00:00.000
        "%Y-%m-%d %H:%M:%S.%f",

        # 15/01/2026
        "%d/%m/%Y",

        # 15/01/2026 00:00:00
        "%d/%m/%Y %H:%M:%S",

        # 15/01/2026 00:00:00.000
        "%d/%m/%Y %H:%M:%S.%f",

        # 15-01-2026
        "%d-%m-%Y",

        # 15-01-2026 00:00:00
        "%d-%m-%Y %H:%M:%S",

        # 2026/01/15
        "%Y/%m/%d",

        # 2026/01/15 00:00:00
        "%Y/%m/%d %H:%M:%S",

        # 15.01.2026
        "%d.%m.%Y",

        # 15.01.2026 00:00:00
        "%d.%m.%Y %H:%M:%S",
    ]

    for formato in formatos:

        try:

            return datetime.strptime(
                valor,
                formato
            ).date()

        except ValueError:

            continue

    return None


@router.get(
    "/parcelas",
    response_model=ParcelasResponse
)
def buscar_parcelas(
    ccb: str,
    request: Request
):

    ccb = ccb.strip()

    if not ccb:

        raise HTTPException(
            status_code=400,
            detail="CCB não informado"
        )

    con = None
    cursor = None

    try:

        con = obter_conexao()

        cursor = con.cursor()

        cursor.execute(
            """
            SELECT
                `Seu NÃºmero`,
                `Vencimento`,
                `Valor Nominal`,
                `Valor de AquisiÃ§Ã£o`,
                `Data LiquidaÃ§Ã£o`
            FROM searchhub.parcelas
            WHERE `CCB` = ?
            ORDER BY `Vencimento`
            """,
            (ccb,)
        )

        rows = cursor.fetchall()

    except mariadb.Error as e:

        logger.exception(
            f"usuario={request.state.usuario.email} | "
            f"ERRO_BUSCA_PARCELAS | "
            f"ccb={ccb} | "
            f"erro={str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail="Erro ao consultar fluxo de parcelas"
        )

    finally:

        if cursor is not None:
            cursor.close()

        if con is not None:
            con.close()

    data = []

    for row in rows:

        data.append(
            ParcelaResponse(

                seu_numero=(
                    str(row[0]).strip()
                    if row[0] is not None
                    else None
                ),

                vencimento=converter_data(
                    row[1]
                ),

                valor_nominal=converter_decimal(
                    row[2]
                ),

                valor_aquisicao=converter_decimal(
                    row[3]
                ),

                data_liquidacao=converter_data(
                    row[4]
                )
            )
        )

    logger.info(
        f"usuario={request.state.usuario.email} | "
        f"FLUXO_PARCELAS | "
        f"ccb={ccb} | "
        f"total_parcelas={len(data)}"
    )

    return ParcelasResponse(
        ccb=ccb,
        total=len(data),
        data=data
    )