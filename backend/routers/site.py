"""
Rotas do site público — renderizam templates Jinja2.
Nenhuma autenticação necessária.
"""
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from models.cliente import Lead
from models.imovel import Imovel
from schemas.cliente import LeadCriar

router = APIRouter(tags=["site"])
templates = Jinja2Templates(directory="frontend/templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    destaques = (
        db.query(Imovel)
        .filter(Imovel.destaque == True, Imovel.ativo == True)
        .limit(6)
        .all()
    )
    return templates.TemplateResponse(
        "site/index.html", {"request": request, "destaques": destaques}
    )


@router.get("/imoveis", response_class=HTMLResponse)
def lista_imoveis(
    request: Request,
    tipo: str | None = Query(None),
    finalidade: str | None = Query(None),
    bairro: str | None = Query(None),
    quartos: int | None = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(Imovel).filter(Imovel.ativo == True)
    if tipo:
        q = q.filter(Imovel.tipo_imovel == tipo)
    if finalidade:
        q = q.filter(Imovel.finalidade == finalidade)
    if bairro:
        q = q.filter(Imovel.bairro.ilike(f"%{bairro}%"))
    if quartos:
        q = q.filter(Imovel.quartos >= quartos)
    imoveis = q.all()
    return templates.TemplateResponse(
        "site/imoveis.html",
        {"request": request, "imoveis": imoveis, "filtros": request.query_params},
    )


@router.get("/imoveis/{slug}", response_class=HTMLResponse)
def detalhe_imovel(slug: str, request: Request, db: Session = Depends(get_db)):
    imovel = db.query(Imovel).filter(Imovel.slug == slug, Imovel.ativo == True).first()
    if not imovel:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado")
    return templates.TemplateResponse(
        "site/imovel_detalhe.html", {"request": request, "imovel": imovel}
    )


@router.post("/contato", status_code=201)
async def contato(dados: LeadCriar, db: Session = Depends(get_db)):
    lead = Lead(**dados.model_dump())
    db.add(lead)
    db.commit()
    return {"mensagem": "Mensagem recebida! Entraremos em contato em breve."}
