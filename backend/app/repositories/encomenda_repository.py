import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.encomenda import Encomenda


class EncomendaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, encomenda: Encomenda) -> Encomenda:
        self.db.add(encomenda)
        self.db.commit()
        self.db.refresh(encomenda)
        return encomenda

    def get_by_id(self, encomenda_id: uuid.UUID) -> Optional[Encomenda]:
        return self.db.query(Encomenda).filter(Encomenda.id == encomenda_id).first()

    def get_by_codigo_e_cliente(
        self, codigo_rastreio: str, cliente_id: uuid.UUID
    ) -> Optional[Encomenda]:
        return (
            self.db.query(Encomenda)
            .filter(
                Encomenda.codigo_rastreio == codigo_rastreio,
                Encomenda.cliente_id == cliente_id,
            )
            .first()
        )

    def list_by_cliente(self, cliente_id: uuid.UUID) -> List[Encomenda]:
        return self.db.query(Encomenda).filter(Encomenda.cliente_id == cliente_id).all()

    def list_ativas(self) -> List[Encomenda]:
        return self.db.query(Encomenda).filter(Encomenda.ativa.is_(True)).all()

    def delete(self, encomenda: Encomenda) -> None:
        self.db.delete(encomenda)
        self.db.commit()

    def save(self, encomenda: Encomenda) -> Encomenda:
        self.db.add(encomenda)
        self.db.commit()
        self.db.refresh(encomenda)
        return encomenda
