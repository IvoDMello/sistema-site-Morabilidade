from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Imovel(Base):
    __tablename__ = "imoveis"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    codigo: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    titulo: Mapped[str] = mapped_column(String(200))
    slug: Mapped[str] = mapped_column(String(220), unique=True, index=True)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)

    tipo_imovel: Mapped[str] = mapped_column(
        Enum(
            "apartamento", "casa", "terreno", "sala_comercial",
            "galpao", "cobertura", "flat", "studio",
            name="tipo_imovel",
        )
    )
    finalidade: Mapped[str] = mapped_column(
        Enum("venda", "aluguel", "temporada", name="finalidade_imovel")
    )
    status: Mapped[str] = mapped_column(
        Enum("disponivel", "reservado", "vendido", "alugado", name="status_imovel"),
        default="disponivel",
    )

    # Localização
    cep: Mapped[str | None] = mapped_column(String(9), nullable=True)
    logradouro: Mapped[str | None] = mapped_column(String(200), nullable=True)
    numero: Mapped[str | None] = mapped_column(String(10), nullable=True)
    complemento: Mapped[str | None] = mapped_column(String(50), nullable=True)
    bairro: Mapped[str] = mapped_column(String(100))
    cidade: Mapped[str] = mapped_column(String(100), default="Rio de Janeiro")
    estado: Mapped[str] = mapped_column(String(2), default="RJ")
    mostrar_endereco: Mapped[bool] = mapped_column(Boolean, default=True)

    # Valores
    preco: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    preco_condominio: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    preco_iptu: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)

    # Características
    area_total: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    area_util: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    quartos: Mapped[int | None] = mapped_column(Integer, nullable=True)
    suites: Mapped[int | None] = mapped_column(Integer, nullable=True)
    banheiros: Mapped[int | None] = mapped_column(Integer, nullable=True)
    vagas_garagem: Mapped[int | None] = mapped_column(Integer, nullable=True)
    andar: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_andares: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Diferenciais (booleanos)
    aceita_permuta: Mapped[bool] = mapped_column(Boolean, default=False)
    aceita_financiamento: Mapped[bool] = mapped_column(Boolean, default=False)
    destaque: Mapped[bool] = mapped_column(Boolean, default=False)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)

    # FK
    proprietario_id: Mapped[int | None] = mapped_column(
        ForeignKey("proprietarios.id"), nullable=True
    )
    corretor_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id"), nullable=True
    )

    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    proprietario: Mapped["Proprietario"] = relationship("Proprietario", back_populates="imoveis")
    fotos: Mapped[list["FotoImovel"]] = relationship(
        "FotoImovel", back_populates="imovel", cascade="all, delete-orphan"
    )


class FotoImovel(Base):
    __tablename__ = "fotos_imovel"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    imovel_id: Mapped[int] = mapped_column(ForeignKey("imoveis.id"))
    caminho: Mapped[str] = mapped_column(String(300))
    legenda: Mapped[str | None] = mapped_column(String(150), nullable=True)
    ordem: Mapped[int] = mapped_column(Integer, default=0)
    capa: Mapped[bool] = mapped_column(Boolean, default=False)

    imovel: Mapped["Imovel"] = relationship("Imovel", back_populates="fotos")
