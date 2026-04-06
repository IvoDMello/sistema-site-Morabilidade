from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from auth import usuario_atual
from database import get_db
from models.cliente import Cliente, Lead
from models.usuario import Usuario
from schemas.cliente import (
    ClienteCriar, ClienteResposta,
    LeadCriar, LeadAtualizar, LeadResposta,
)

router = APIRouter(prefix="/api/v1/clientes", tags=["clientes"])


# ── Clientes ──────────────────────────────────────────────────────────────────

@router.get("/", response_model=list[ClienteResposta])
def listar_clientes(
    skip: int = 0,
    limit: int = 50,
    nome: str | None = Query(None),
    db: Session = Depends(get_db),
    _: Usuario = Depends(usuario_atual),
):
    q = db.query(Cliente)
    if nome:
        q = q.filter(Cliente.nome.ilike(f"%{nome}%"))
    return q.offset(skip).limit(limit).all()


@router.get("/{id}", response_model=ClienteResposta)
def buscar_cliente(id: int, db: Session = Depends(get_db), _: Usuario = Depends(usuario_atual)):
    cliente = db.get(Cliente, id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente


@router.post("/", response_model=ClienteResposta, status_code=201)
def criar_cliente(
    dados: ClienteCriar,
    db: Session = Depends(get_db),
    _: Usuario = Depends(usuario_atual),
):
    cliente = Cliente(**dados.model_dump())
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


# ── Leads ─────────────────────────────────────────────────────────────────────

@router.get("/leads/", response_model=list[LeadResposta])
def listar_leads(
    skip: int = 0,
    limit: int = 50,
    status: str | None = Query(None),
    corretor_id: int | None = Query(None),
    db: Session = Depends(get_db),
    _: Usuario = Depends(usuario_atual),
):
    q = db.query(Lead)
    if status:
        q = q.filter(Lead.status == status)
    if corretor_id:
        q = q.filter(Lead.corretor_id == corretor_id)
    return q.order_by(Lead.criado_em.desc()).offset(skip).limit(limit).all()


@router.post("/leads/", response_model=LeadResposta, status_code=201)
def criar_lead(dados: LeadCriar, db: Session = Depends(get_db)):
    lead = Lead(**dados.model_dump())
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead


@router.patch("/leads/{id}", response_model=LeadResposta)
def atualizar_lead(
    id: int,
    dados: LeadAtualizar,
    db: Session = Depends(get_db),
    _: Usuario = Depends(usuario_atual),
):
    lead = db.get(Lead, id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead não encontrado")
    for campo, valor in dados.model_dump(exclude_none=True).items():
        setattr(lead, campo, valor)
    db.commit()
    db.refresh(lead)
    return lead
