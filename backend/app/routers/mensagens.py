import uuid
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_cliente_id
from app.repositories.mensagem_repository import MensagemRepository
from app.schemas.mensagem import MensagemResponse
from app.services.mensagem_service import MensagemService

router = APIRouter(prefix="/api/mensagens", tags=["mensagens"])


@router.get("", response_model=List[MensagemResponse])
def listar(
    cliente_id: uuid.UUID = Depends(get_current_cliente_id),
    db: Session = Depends(get_db),
):
    service = MensagemService(MensagemRepository(db))
    return service.listar(cliente_id)
