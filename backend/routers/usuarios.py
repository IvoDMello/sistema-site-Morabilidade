from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth import autenticar_usuario, criar_token, hash_senha, requer_admin, usuario_atual
from database import get_db
from models.usuario import Usuario
from schemas.usuario import Token, UsuarioCriar, UsuarioResposta, UsuarioAtualizar

router = APIRouter(prefix="/api/v1/usuarios", tags=["usuarios"])


@router.post("/token", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = autenticar_usuario(db, form.username, form.password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
        )
    token = criar_token({"sub": usuario.email})
    return {"access_token": token}


@router.post("/setup", response_model=UsuarioResposta, status_code=201)
def setup_admin(dados: UsuarioCriar, db: Session = Depends(get_db)):
    """Cria o primeiro admin. Só funciona enquanto não houver nenhum usuário."""
    if db.query(Usuario).count() > 0:
        raise HTTPException(status_code=403, detail="Setup já realizado")
    usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=hash_senha(dados.senha),
        perfil="admin",
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.post("/", response_model=UsuarioResposta, status_code=201)
def criar_usuario(
    dados: UsuarioCriar,
    db: Session = Depends(get_db),
    _: Usuario = Depends(requer_admin),
):
    if db.query(Usuario).filter(Usuario.email == dados.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=hash_senha(dados.senha),
        perfil=dados.perfil,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.get("/me", response_model=UsuarioResposta)
def meu_perfil(atual: Usuario = Depends(usuario_atual)):
    return atual


@router.get("/", response_model=list[UsuarioResposta])
def listar_usuarios(
    db: Session = Depends(get_db),
    _: Usuario = Depends(requer_admin),
):
    return db.query(Usuario).all()


@router.patch("/{id}", response_model=UsuarioResposta)
def atualizar_usuario(
    id: int,
    dados: UsuarioAtualizar,
    db: Session = Depends(get_db),
    _: Usuario = Depends(requer_admin),
):
    usuario = db.get(Usuario, id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    for campo, valor in dados.model_dump(exclude_none=True).items():
        setattr(usuario, campo, valor)
    db.commit()
    db.refresh(usuario)
    return usuario
