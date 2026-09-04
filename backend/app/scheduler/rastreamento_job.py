import logging

from apscheduler.schedulers.background import BackgroundScheduler

from app.config import settings
from app.database import SessionLocal
from app.integrations.linketrack import LinkeTrackClient
from app.repositories.encomenda_repository import EncomendaRepository
from app.repositories.mensagem_repository import MensagemRepository
from app.repositories.movimentacao_repository import MovimentacaoRepository
from app.services.rastreamento_service import RastreamentoService

logger = logging.getLogger(__name__)


def executar_rastreamento():
    db = SessionLocal()
    try:
        encomenda_repository = EncomendaRepository(db)
        rastreamento_service = RastreamentoService(
            encomenda_repository,
            MovimentacaoRepository(db),
            MensagemRepository(db),
            LinkeTrackClient(),
        )

        for encomenda in encomenda_repository.list_ativas():
            try:
                rastreamento_service.atualizar_encomenda(encomenda)
            except Exception:
                logger.exception("Falha ao atualizar encomenda %s", encomenda.codigo_rastreio)
    finally:
        db.close()


def iniciar_scheduler() -> BackgroundScheduler:
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        executar_rastreamento,
        "interval",
        minutes=settings.TRACKING_INTERVAL_MINUTES,
        id="rastreamento_job",
    )
    scheduler.start()
    return scheduler
