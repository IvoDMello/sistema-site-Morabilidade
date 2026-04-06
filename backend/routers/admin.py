"""
Rotas do painel administrativo — renderizam templates Jinja2.
Autenticação via token JWT armazenado no localStorage (validado no frontend).
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/admin", tags=["admin"])
templates = Jinja2Templates(directory="frontend/templates")


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("admin/login.html", {"request": request})


@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("admin/dashboard.html", {"request": request})


@router.get("/imoveis", response_class=HTMLResponse)
def imoveis_page(request: Request):
    return templates.TemplateResponse("admin/dashboard.html", {"request": request})


@router.get("/proprietarios", response_class=HTMLResponse)
def proprietarios_page(request: Request):
    return templates.TemplateResponse("admin/dashboard.html", {"request": request})


@router.get("/clientes", response_class=HTMLResponse)
def clientes_page(request: Request):
    return templates.TemplateResponse("admin/dashboard.html", {"request": request})


@router.get("/relatorios", response_class=HTMLResponse)
def relatorios_page(request: Request):
    return templates.TemplateResponse("admin/dashboard.html", {"request": request})
