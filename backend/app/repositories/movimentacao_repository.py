import uuid
from typing import List

from sqlalchemy.orm import Session

from app.models.movimentacao import Movimentacao


class MovimentacaoRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_by_encomenda(self, encomenda_id: uuid.UUID) -> List[Movimentacao]:
        return (
            self.db.query(Movimentacao)
            .filter(Movimentacao.encomenda_id == encomenda_id)
            .order_by(Movimentacao.data_evento.asc())
            .all()
        )

    def get_hashes_existentes(self, encomenda_id: uuid.UUID) -> set:
        rows = (
            self.db.query(Movimentacao.dedup_hash)
            .filter(Movimentacao.encomenda_id == encomenda_id)
            .all()
        )
        return {r[0] for r in rows}

    def create(self, movimentacao: Movimentacao) -> Movimentacao:
        self.db.add(movimentacao)
        self.db.commit()
        self.db.refresh(movimentacao)
        return movimentacao
