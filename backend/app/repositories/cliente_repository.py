import uuid
from typing import Optional

from sqlalchemy.orm import Session

from app.models.cliente import Cliente


class ClienteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> Optional[Cliente]:
        return self.db.query(Cliente).filter(Cliente.email == email).first()

    def get_by_id(self, cliente_id: uuid.UUID) -> Optional[Cliente]:
        return self.db.query(Cliente).filter(Cliente.id == cliente_id).first()

    def create(self, cliente: Cliente) -> Cliente:
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente
