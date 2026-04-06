from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr


class ClienteBase(BaseModel):
    nome: str
    email: EmailStr | None = None
    telefone: str | None = None
    cpf: str | None = None
    observacoes: str | None = None


class ClienteCriar(ClienteBase):
    pass


class ClienteResposta(ClienteBase):
    id: int
    criado_em: datetime

    model_config = {"from_attributes": True}


class LeadBase(BaseModel):
    cliente_id: int | None = None
    imovel_id: int | None = None
    corretor_id: int | None = None
    nome_contato: str | None = None
    email_contato: EmailStr | None = None
    telefone_contato: str | None = None
    mensagem: str | None = None
    origem: Literal["site", "whatsapp", "telefone", "indicacao", "outro"] = "site"
    status: Literal["novo", "em_atendimento", "negociando", "fechado", "perdido"] = "novo"
    prioridade: int = 2


class LeadCriar(LeadBase):
    pass


class LeadAtualizar(BaseModel):
    corretor_id: int | None = None
    status: Literal["novo", "em_atendimento", "negociando", "fechado", "perdido"] | None = None
    prioridade: int | None = None


class LeadResposta(LeadBase):
    id: int
    criado_em: datetime
    atualizado_em: datetime

    model_config = {"from_attributes": True}
