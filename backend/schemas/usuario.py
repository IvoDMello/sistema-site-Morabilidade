from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr


class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    perfil: Literal["admin", "corretor"] = "corretor"


class UsuarioCriar(UsuarioBase):
    senha: str


class UsuarioAtualizar(BaseModel):
    nome: str | None = None
    perfil: Literal["admin", "corretor"] | None = None
    ativo: bool | None = None


class UsuarioResposta(UsuarioBase):
    id: int
    ativo: bool
    criado_em: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
