import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_cliente_id
from app.integrations.linketrack import LinkeTrackClient
from app.repositories.encomenda_repository import EncomendaRepository
from app.repositories.mensagem_repository import MensagemRepository
from app.repositories.movimentacao_repository import MovimentacaoRepository
from app.schemas.encomenda import EncomendaCreate, EncomendaResponse
from app.schemas.movimentacao import MovimentacaoResponse
from app.services.encomenda_service import EncomendaService
from app.services.rastreamento_service import RastreamentoService

router = APIRouter(prefix="/api/encomendas", tags=["encomendas"])


def _encomenda_service(db: Session) -> EncomendaService:
    rastreamento_service = RastreamentoService(
        EncomendaRepository(db),
        MovimentacaoRepository(db),
        MensagemRepository(db),
        LinkeTrackClient(),
    )
    return EncomendaService(EncomendaRepository(db), rastreamento_service)


@router.post("", response_model=EncomendaResponse, status_code=status.HTTP_201_CREATED)
def criar(
    payload: EncomendaCreate,
    cliente_id: uuid.UUID = Depends(get_current_cliente_id),
    db: Session = Depends(get_db),
):
    service = _encomenda_service(db)
    try:
        return service.criar(cliente_id, payload.codigo_rastreio)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("", response_model=List[EncomendaResponse])
def listar(
    cliente_id: uuid.UUID = Depends(get_current_cliente_id),
    db: Session = Depends(get_db),
):
    service = _encomenda_service(db)
    return service.listar(cliente_id)


@router.get("/{encomenda_id}", response_model=EncomendaResponse)
def obter(
    encomenda_id: uuid.UUID,
    cliente_id: uuid.UUID = Depends(get_current_cliente_id),
    db: Session = Depends(get_db),
):
    service = _encomenda_service(db)
    try:
        return service.obter(cliente_id, encomenda_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.delete("/{encomenda_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover(
    encomenda_id: uuid.UUID,
    cliente_id: uuid.UUID = Depends(get_current_cliente_id),
    db: Session = Depends(get_db),
):
    service = _encomenda_service(db)
    try:
        service.remover(cliente_id, encomenda_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.get("/{encomenda_id}/movimentacoes", response_model=List[MovimentacaoResponse])
def movimentacoes(
    encomenda_id: uuid.UUID,
    cliente_id: uuid.UUID = Depends(get_current_cliente_id),
    db: Session = Depends(get_db),
):
    service = _encomenda_service(db)
    try:
        service.obter(cliente_id, encomenda_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return MovimentacaoRepository(db).list_by_encomenda(encomenda_id)
