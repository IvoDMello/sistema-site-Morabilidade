from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from config import settings
from database import get_db
from models.usuario import Usuario

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/usuarios/token")


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha_plana, senha_hash)


def hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)


def criar_token(dados: dict) -> str:
    payload = dados.copy()
    expira = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload.update({"exp": expira})
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def autenticar_usuario(db: Session, email: str, senha: str):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario or not verificar_senha(senha, usuario.senha_hash):
        return None
    return usuario


async def usuario_atual(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> Usuario:
    credencial_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credencial_exception
    except JWTError:
        raise credencial_exception

    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario is None or not usuario.ativo:
        raise credencial_exception
    return usuario


async def requer_admin(usuario: Usuario = Depends(usuario_atual)) -> Usuario:
    if usuario.perfil != "admin":
        raise HTTPException(status_code=403, detail="Acesso restrito a administradores")
    return usuario
