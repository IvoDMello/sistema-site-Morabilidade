from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(150))
    email: Mapped[str | None] = mapped_column(String(150), nullable=True, index=True)
    telefone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    cpf: Mapped[str | None] = mapped_column(String(14), unique=True, nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)

    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    leads: Mapped[list["Lead"]] = relationship("Lead", back_populates="cliente")


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    cliente_id: Mapped[int | None] = mapped_column(
        ForeignKey("clientes.id"), nullable=True
    )
    imovel_id: Mapped[int | None] = mapped_column(
        ForeignKey("imoveis.id"), nullable=True
    )
    corretor_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id"), nullable=True
    )

    # Dados do contato (preenchidos quando não há cliente cadastrado)
    nome_contato: Mapped[str | None] = mapped_column(String(150), nullable=True)
    email_contato: Mapped[str | None] = mapped_column(String(150), nullable=True)
    telefone_contato: Mapped[str | None] = mapped_column(String(20), nullable=True)

    mensagem: Mapped[str | None] = mapped_column(Text, nullable=True)
    origem: Mapped[str] = mapped_column(
        Enum("site", "whatsapp", "telefone", "indicacao", "outro", name="origem_lead"),
        default="site",
    )
    status: Mapped[str] = mapped_column(
        Enum("novo", "em_atendimento", "negociando", "fechado", "perdido", name="status_lead"),
        default="novo",
    )
    prioridade: Mapped[int] = mapped_column(Integer, default=2)  # 1=alta 2=media 3=baixa

    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    cliente: Mapped["Cliente"] = relationship("Cliente", back_populates="leads")
