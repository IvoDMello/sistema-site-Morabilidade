from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from auth import usuario_atual
from database import get_db
from models.cliente import Lead
from models.imovel import Imovel
from models.usuario import Usuario

router = APIRouter(prefix="/api/v1/relatorios", tags=["relatorios"])


@router.get("/resumo")
def resumo_geral(
    db: Session = Depends(get_db),
    _: Usuario = Depends(usuario_atual),
):
    total_imoveis = db.query(func.count(Imovel.id)).scalar()
    por_status = (
        db.query(Imovel.status, func.count(Imovel.id))
        .group_by(Imovel.status)
        .all()
    )
    total_leads = db.query(func.count(Lead.id)).scalar()
    leads_novos = db.query(func.count(Lead.id)).filter(Lead.status == "novo").scalar()

    return {
        "imoveis": {
            "total": total_imoveis,
            "por_status": {s: c for s, c in por_status},
        },
        "leads": {
            "total": total_leads,
            "novos": leads_novos,
        },
    }


@router.get("/imoveis-por-tipo")
def imoveis_por_tipo(
    db: Session = Depends(get_db),
    _: Usuario = Depends(usuario_atual),
):
    resultado = (
        db.query(Imovel.tipo_imovel, func.count(Imovel.id))
        .group_by(Imovel.tipo_imovel)
        .all()
    )
    return {tipo: total for tipo, total in resultado}


@router.get("/leads-por-origem")
def leads_por_origem(
    db: Session = Depends(get_db),
    _: Usuario = Depends(usuario_atual),
):
    resultado = (
        db.query(Lead.origem, func.count(Lead.id))
        .group_by(Lead.origem)
        .all()
    )
    return {origem: total for origem, total in resultado}
