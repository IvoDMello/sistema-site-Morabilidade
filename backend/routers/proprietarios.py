from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth import usuario_atual
from database import get_db
from models.proprietario import Proprietario
from models.usuario import Usuario
from schemas.proprietario import ProprietarioCriar, ProprietarioAtualizar, ProprietarioResposta

router = APIRouter(prefix="/api/v1/proprietarios", tags=["proprietarios"])


@router.get("/", response_model=list[ProprietarioResposta])
def listar(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    _: Usuario = Depends(usuario_atual),
):
    return db.query(Proprietario).offset(skip).limit(limit).all()


@router.get("/{id}", response_model=ProprietarioResposta)
def buscar(id: int, db: Session = Depends(get_db), _: Usuario = Depends(usuario_atual)):
    prop = db.get(Proprietario, id)
    if not prop:
        raise HTTPException(status_code=404, detail="Proprietário não encontrado")
    return prop


@router.post("/", response_model=ProprietarioResposta, status_code=201)
def criar(
    dados: ProprietarioCriar,
    db: Session = Depends(get_db),
    _: Usuario = Depends(usuario_atual),
):
    prop = Proprietario(**dados.model_dump())
    db.add(prop)
    db.commit()
    db.refresh(prop)
    return prop


@router.patch("/{id}", response_model=ProprietarioResposta)
def atualizar(
    id: int,
    dados: ProprietarioAtualizar,
    db: Session = Depends(get_db),
    _: Usuario = Depends(usuario_atual),
):
    prop = db.get(Proprietario, id)
    if not prop:
        raise HTTPException(status_code=404, detail="Proprietário não encontrado")
    for campo, valor in dados.model_dump(exclude_none=True).items():
        setattr(prop, campo, valor)
    db.commit()
    db.refresh(prop)
    return prop


@router.delete("/{id}", status_code=204)
def remover(id: int, db: Session = Depends(get_db), _: Usuario = Depends(usuario_atual)):
    prop = db.get(Proprietario, id)
    if not prop:
        raise HTTPException(status_code=404, detail="Proprietário não encontrado")
    db.delete(prop)
    db.commit()
