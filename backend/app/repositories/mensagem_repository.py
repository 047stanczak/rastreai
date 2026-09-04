import uuid
from typing import List

from sqlalchemy.orm import Session

from app.models.mensagem import Mensagem


class MensagemRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, mensagem: Mensagem) -> Mensagem:
        self.db.add(mensagem)
        self.db.commit()
        self.db.refresh(mensagem)
        return mensagem

    def list_by_cliente(self, cliente_id: uuid.UUID) -> List[Mensagem]:
        return (
            self.db.query(Mensagem)
            .filter(Mensagem.cliente_id == cliente_id)
            .order_by(Mensagem.created_at.desc())
            .all()
        )
