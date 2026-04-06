import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database import Base, engine
from routers import admin, clientes, imoveis, proprietarios, relatorios, site, usuarios

# Garante que o diretório de uploads existe (mesmo com volume montado)
os.makedirs("/app/uploads/imoveis", exist_ok=True)

# Cria as tabelas automaticamente (em produção, usar Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema Imobiliário RJ",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Arquivos estáticos
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
app.mount("/uploads", StaticFiles(directory="/app/uploads"), name="uploads")

# Routers da API (sistema interno)
app.include_router(usuarios.router)
app.include_router(imoveis.router)
app.include_router(proprietarios.router)
app.include_router(clientes.router)
app.include_router(relatorios.router)

# Painel administrativo
app.include_router(admin.router)

# Routers do site público (sem prefixo)
app.include_router(site.router)
