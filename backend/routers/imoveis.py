import os
import shutil
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from slugify import slugify
from sqlalchemy.orm import Session

from auth import usuario_atual
from config import settings
from database import get_db
from models.imovel import FotoImovel, Imovel
from models.usuario import Usuario
from schemas.imovel import ImovelCriar, ImovelAtualizar, ImovelListagem, ImovelResposta

router = APIRouter(prefix="/api/v1/imoveis", tags=["imoveis"])


def _gerar_codigo(db: Session) -> str:
    total = db.query(Imovel).count()
    return f"IMV{total + 1:05d}"


def _gerar_slug(titulo: str, codigo: str) -> str:
    return slugify(f"{titulo}-{codigo}")


@router.get("/", response_model=list[ImovelListagem])
def listar(
    skip: int = 0,
    limit: int = 20,
    tipo: str | None = Query(None),
    finalidade: str | None = Query(None),
    bairro: str | None = Query(None),
    status: str | None = Query(None),
    destaque: bool | None = Query(None),
    db: Session = Depends(get_db),
    _: Usuario = Depends(usuario_atual),
):
    q = db.query(Imovel)
    if tipo:
        q = q.filter(Imovel.tipo_imovel == tipo)
    if finalidade:
        q = q.filter(Imovel.finalidade == finalidade)
    if bairro:
        q = q.filter(Imovel.bairro.ilike(f"%{bairro}%"))
    if status:
        q = q.filter(Imovel.status == status)
    if destaque is not None:
        q = q.filter(Imovel.destaque == destaque)
    return q.offset(skip).limit(limit).all()


@router.get("/{id}", response_model=ImovelResposta)
def buscar(id: int, db: Session = Depends(get_db), _: Usuario = Depends(usuario_atual)):
    imovel = db.get(Imovel, id)
    if not imovel:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado")
    return imovel


@router.post("/", response_model=ImovelResposta, status_code=201)
def criar(
    dados: ImovelCriar,
    db: Session = Depends(get_db),
    _: Usuario = Depends(usuario_atual),
):
    codigo = _gerar_codigo(db)
    slug = _gerar_slug(dados.titulo, codigo)
    imovel = Imovel(**dados.model_dump(), codigo=codigo, slug=slug)
    db.add(imovel)
    db.commit()
    db.refresh(imovel)
    return imovel


@router.patch("/{id}", response_model=ImovelResposta)
def atualizar(
    id: int,
    dados: ImovelAtualizar,
    db: Session = Depends(get_db),
    _: Usuario = Depends(usuario_atual),
):
    imovel = db.get(Imovel, id)
    if not imovel:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado")
    for campo, valor in dados.model_dump(exclude_none=True).items():
        setattr(imovel, campo, valor)
    db.commit()
    db.refresh(imovel)
    return imovel


@router.delete("/{id}", status_code=204)
def remover(id: int, db: Session = Depends(get_db), _: Usuario = Depends(usuario_atual)):
    imovel = db.get(Imovel, id)
    if not imovel:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado")
    db.delete(imovel)
    db.commit()


@router.post("/{id}/fotos", status_code=201)
async def upload_foto(
    id: int,
    arquivo: UploadFile = File(...),
    capa: bool = False,
    db: Session = Depends(get_db),
    _: Usuario = Depends(usuario_atual),
):
    imovel = db.get(Imovel, id)
    if not imovel:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado")

    pasta = os.path.join(settings.UPLOAD_DIR, "imoveis", str(id))
    os.makedirs(pasta, exist_ok=True)
    nome_arquivo = f"{uuid.uuid4().hex}{os.path.splitext(arquivo.filename)[1]}"
    caminho = os.path.join(pasta, nome_arquivo)
    with open(caminho, "wb") as f:
        shutil.copyfileobj(arquivo.file, f)

    if capa:
        db.query(FotoImovel).filter(FotoImovel.imovel_id == id).update({"capa": False})

    foto = FotoImovel(
        imovel_id=id,
        caminho=f"/uploads/imoveis/{id}/{nome_arquivo}",
        capa=capa,
        ordem=db.query(FotoImovel).filter(FotoImovel.imovel_id == id).count(),
    )
    db.add(foto)
    db.commit()
    return {"id": foto.id, "caminho": foto.caminho}


@router.delete("/{id}/fotos/{foto_id}", status_code=204)
def remover_foto(
    id: int,
    foto_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(usuario_atual),
):
    foto = db.query(FotoImovel).filter(FotoImovel.id == foto_id, FotoImovel.imovel_id == id).first()
    if not foto:
        raise HTTPException(status_code=404, detail="Foto não encontrada")
    if os.path.exists(foto.caminho.lstrip("/")):
        os.remove(foto.caminho.lstrip("/"))
    db.delete(foto)
    db.commit()
