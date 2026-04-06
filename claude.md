# Projeto: Sistema Imobiliário RJ

## Stack
- Python 3.12, FastAPI, SQLAlchemy 2.0, PostgreSQL
- Frontend: Jinja2 + Tailwind CSS + Alpine.js
- Auth: JWT com python-jose

## Convenções
- Models em português (campo `tipo_imovel`, não `property_type`)
- Todas as rotas da API começam com /api/v1/
- Site público: rotas sem prefixo /api

## Módulos
- Imóveis (cadastro, fotos, características, status)
- Proprietários (PF e PJ)
- Clientes/Leads (CRM básico)
- Usuários internos (admin, corretor)
- Relatórios
- Integração site ↔ sistema (mesmo banco, API compartilhada)