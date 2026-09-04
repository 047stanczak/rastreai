from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, clientes, encomendas, mensagens
from app.scheduler.rastreamento_job import iniciar_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = iniciar_scheduler()
    yield
    scheduler.shutdown()


app = FastAPI(title="RastreiaAi", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(clientes.router)
app.include_router(encomendas.router)
app.include_router(mensagens.router)


@app.get("/")
def health():
    return {"status": "ok"}
