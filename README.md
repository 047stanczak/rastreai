# RastreiaAi

Sistema de monitoramento de encomendas: o cliente cadastra um código de rastreio, o backend consulta periodicamente a transportadora (via Link&Track) e notifica o cliente quando surge uma movimentação nova — sem duplicar histórico.

## Arquitetura

```
Usuário → Frontend (React) → Backend (FastAPI) → PostgreSQL
                                    ↑
                              Scheduler (APScheduler)
                                    ↓
                              Link&Track API
```

Camadas do backend: `routers` (HTTP) → `services` (regras de negócio) → `repositories` (acesso a dados) → `models` (SQLAlchemy). A comunicação com a transportadora fica isolada em `integrations/linketrack.py`.

## Tecnologias

- **Backend**: Python 3.12, FastAPI, SQLAlchemy, Alembic, PostgreSQL, JWT, bcrypt, APScheduler, pytest
- **Frontend**: React, Vite, TypeScript, React Router
- **Infra**: Docker Compose (backend, frontend, postgres)

## Estrutura

```
rastreiaai/
├── backend/       # API REST
├── frontend/      # SPA React
├── infra/         # documentação de infraestrutura
├── .env.example
└── docker-compose.yml
```

## Como executar

```bash
cp .env.example .env
docker compose up --build
```

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Swagger: http://localhost:8000/docs

O backend roda as migrations do Alembic automaticamente ao subir.

## Variáveis de ambiente

Ver `.env.example` na raiz. Principais:

| Variável | Descrição |
|---|---|
| `DATABASE_URL` | string de conexão do backend com o PostgreSQL |
| `JWT_SECRET` | chave de assinatura dos tokens JWT |
| `JWT_EXPIRE_MINUTES` | validade do token |
| `LINKE_TRACK_TOKEN` | chave da API de rastreamento (Bearer) |
| `TRACKING_INTERVAL_MINUTES` | intervalo do job de rastreamento automático |
| `VITE_API_URL` | URL do backend consumida pelo frontend |

## Rodar migrations manualmente (fora do Docker)

```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
```

## Rodar testes

```bash
cd backend
pip install -r requirements.txt
export DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rastreiaai
pytest
```

Os testes usam um banco separado (`rastreiaai_test`), criado automaticamente a partir de `DATABASE_URL` (sufixo `_test`). Crie-o manualmente antes de rodar caso não exista:

```bash
createdb rastreiaai_test
```

## API

```
POST   /api/auth/register
POST   /api/auth/login

GET    /api/clientes/me

POST   /api/encomendas
GET    /api/encomendas
GET    /api/encomendas/{id}
DELETE /api/encomendas/{id}
GET    /api/encomendas/{id}/movimentacoes

GET    /api/mensagens
```

Todos os endpoints exceto `/api/auth/*` exigem `Authorization: Bearer <token>`.

## Regra de negócio central

A cada consulta à Link&Track, apenas eventos ainda não persistidos (identificados por um hash de deduplicação sobre código de rastreio + status + descrição + local + data) são salvos como novas `Movimentacao`. Cada movimentação nova gera exatamente uma `Mensagem`.
