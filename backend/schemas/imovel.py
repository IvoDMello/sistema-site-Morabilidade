from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class FotoResposta(BaseModel):
    id: int
    caminho: str
    legenda: str | None = None
    ordem: int
    capa: bool

    model_config = {"from_attributes": True}


class ImovelBase(BaseModel):
    titulo: str
    descricao: str | None = None
    tipo_imovel: Literal[
        "apartamento", "casa", "terreno", "sala_comercial",
        "galpao", "cobertura", "flat", "studio"
    ]
    finalidade: Literal["venda", "aluguel", "temporada"]
    status: Literal["disponivel", "reservado", "vendido", "alugado"] = "disponivel"
    cep: str | None = None
    logradouro: str | None = None
    numero: str | None = None
    complemento: str | None = None
    bairro: str
    cidade: str = "Rio de Janeiro"
    estado: str = "RJ"
    mostrar_endereco: bool = True
    preco: float | None = None
    preco_condominio: float | None = None
    preco_iptu: float | None = None
    area_total: float | None = None
    area_util: float | None = None
    quartos: int | None = None
    suites: int | None = None
    banheiros: int | None = None
    vagas_garagem: int | None = None
    andar: int | None = None
    total_andares: int | None = None
    aceita_permuta: bool = False
    aceita_financiamento: bool = False
    destaque: bool = False
    proprietario_id: int | None = None
    corretor_id: int | None = None


class ImovelCriar(ImovelBase):
    pass


class ImovelAtualizar(ImovelBase):
    titulo: str | None = None
    tipo_imovel: str | None = None
    finalidade: str | None = None
    bairro: str | None = None


class ImovelResposta(ImovelBase):
    id: int
    codigo: str
    slug: str
    ativo: bool
    fotos: list[FotoResposta] = []
    criado_em: datetime
    atualizado_em: datetime

    model_config = {"from_attributes": True}


class ImovelListagem(BaseModel):
    id: int
    codigo: str
    titulo: str
    slug: str
    tipo_imovel: str
    finalidade: str
    status: str
    bairro: str
    cidade: str
    preco: float | None
    quartos: int | None
    area_util: float | None
    destaque: bool
    foto_capa: str | None = None

    model_config = {"from_attributes": True}
