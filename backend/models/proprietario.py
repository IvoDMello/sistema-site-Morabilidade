from datetime import datetime

from sqlalchemy import DateTime, Enum, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Proprietario(Base):
    __tablename__ = "proprietarios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tipo: Mapped[str] = mapped_column(
        Enum("pf", "pj", name="tipo_proprietario"), default="pf"
    )
    nome: Mapped[str] = mapped_column(String(150))
    # PF
    cpf: Mapped[str | None] = mapped_column(String(14), unique=True, nullable=True)
    # PJ
    cnpj: Mapped[str | None] = mapped_column(String(18), unique=True, nullable=True)
    razao_social: Mapped[str | None] = mapped_column(String(150), nullable=True)
    # Contato
    email: Mapped[str | None] = mapped_column(String(150), nullable=True)
    telefone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    celular: Mapped[str | None] = mapped_column(String(20), nullable=True)
    # Endereço
    cep: Mapped[str | None] = mapped_column(String(9), nullable=True)
    logradouro: Mapped[str | None] = mapped_column(String(200), nullable=True)
    numero: Mapped[str | None] = mapped_column(String(10), nullable=True)
    complemento: Mapped[str | None] = mapped_column(String(50), nullable=True)
    bairro: Mapped[str | None] = mapped_column(String(100), nullable=True)
    cidade: Mapped[str | None] = mapped_column(String(100), nullable=True)
    estado: Mapped[str | None] = mapped_column(String(2), nullable=True)

    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)

    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    imoveis: Mapped[list["Imovel"]] = relationship("Imovel", back_populates="proprietario")
