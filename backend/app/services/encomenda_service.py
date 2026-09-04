import uuid
from typing import List

from app.models.encomenda import Encomenda
from app.repositories.encomenda_repository import EncomendaRepository
from app.services.rastreamento_service import RastreamentoService


class EncomendaService:
    def __init__(
        self,
        encomenda_repository: EncomendaRepository,
        rastreamento_service: RastreamentoService,
    ):
        self.encomenda_repository = encomenda_repository
        self.rastreamento_service = rastreamento_service

    def criar(self, cliente_id: uuid.UUID, codigo_rastreio: str) -> Encomenda:
        existente = self.encomenda_repository.get_by_codigo_e_cliente(codigo_rastreio, cliente_id)
        if existente:
            raise ValueError("Encomenda já cadastrada para este cliente")

        encomenda = Encomenda(cliente_id=cliente_id, codigo_rastreio=codigo_rastreio)
        encomenda = self.encomenda_repository.create(encomenda)

        self.rastreamento_service.atualizar_encomenda(encomenda)
        return encomenda

    def listar(self, cliente_id: uuid.UUID) -> List[Encomenda]:
        return self.encomenda_repository.list_by_cliente(cliente_id)

    def obter(self, cliente_id: uuid.UUID, encomenda_id: uuid.UUID) -> Encomenda:
        encomenda = self.encomenda_repository.get_by_id(encomenda_id)
        if not encomenda or encomenda.cliente_id != cliente_id:
            raise ValueError("Encomenda não encontrada")
        return encomenda

    def remover(self, cliente_id: uuid.UUID, encomenda_id: uuid.UUID) -> None:
        encomenda = self.obter(cliente_id, encomenda_id)
        self.encomenda_repository.delete(encomenda)
