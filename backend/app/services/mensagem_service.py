import uuid
from typing import List

from app.models.mensagem import Mensagem
from app.repositories.mensagem_repository import MensagemRepository


class MensagemService:
    def __init__(self, mensagem_repository: MensagemRepository):
        self.mensagem_repository = mensagem_repository

    def listar(self, cliente_id: uuid.UUID) -> List[Mensagem]:
        return self.mensagem_repository.list_by_cliente(cliente_id)
