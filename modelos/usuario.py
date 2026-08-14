from pydantic import BaseModel
from decimal import Decimal, InvalidOperation
from datetime import date, datetime
from pydantic import BaseModel

class Usuario(BaseModel):
    id_: int
    nome: str
    email: str
    senha: str | None = None
    nivel: str = "operacional"


class UsuarioCriarAtualizar(BaseModel):
    nome: str
    email: str
    senha: str | None = None
    nivel: str = "operacional"


from datetime import date
from decimal import Decimal
from pydantic import BaseModel


class ParcelaResponse(BaseModel):
    seu_numero: str | None
    vencimento: date | None
    valor_nominal: Decimal | None
    valor_aquisicao: Decimal | None
    data_liquidacao: date | None


class ParcelasResponse(BaseModel):
    ccb: str
    total: int
    data: list[ParcelaResponse]