from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr


class ProprietarioBase(BaseModel):
    tipo: Literal["pf", "pj"] = "pf"
    nome: str
    cpf: str | None = None
    cnpj: str | None = None
    razao_social: str | None = None
    email: EmailStr | None = None
    telefone: str | None = None
    celular: str | None = None
    cep: str | None = None
    logradouro: str | None = None
    numero: str | None = None
    complemento: str | None = None
    bairro: str | None = None
    cidade: str | None = None
    estado: str | None = None
    observacoes: str | None = None


class ProprietarioCriar(ProprietarioBase):
    pass


class ProprietarioAtualizar(ProprietarioBase):
    nome: str | None = None


class ProprietarioResposta(ProprietarioBase):
    id: int
    criado_em: datetime

    model_config = {"from_attributes": True}
