import uuid

from app.models.cliente import Cliente
from app.repositories.cliente_repository import ClienteRepository


class ClienteService:
    def __init__(self, cliente_repository: ClienteRepository):
        self.cliente_repository = cliente_repository

    def obter_atual(self, cliente_id: uuid.UUID) -> Cliente:
        cliente = self.cliente_repository.get_by_id(cliente_id)
        if not cliente:
            raise ValueError("Cliente não encontrado")
        return cliente
