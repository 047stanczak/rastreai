import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_cliente_id
from app.repositories.cliente_repository import ClienteRepository
from app.schemas.cliente import ClienteResponse
from app.services.cliente_service import ClienteService

router = APIRouter(prefix="/api/clientes", tags=["clientes"])


@router.get("/me", response_model=ClienteResponse)
def me(
    cliente_id: uuid.UUID = Depends(get_current_cliente_id),
    db: Session = Depends(get_db),
):
    service = ClienteService(ClienteRepository(db))
    return service.obter_atual(cliente_id)
