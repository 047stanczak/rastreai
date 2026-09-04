import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Mensagem(Base):
    __tablename__ = "mensagens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("clientes.id"), nullable=False)
    encomenda_id = Column(UUID(as_uuid=True), ForeignKey("encomendas.id"), nullable=False)
    movimentacao_id = Column(
        UUID(as_uuid=True), ForeignKey("movimentacoes.id"), nullable=False, unique=True
    )
    tipo = Column(String(30), default="SISTEMA", nullable=False)
    status = Column(String(30), default="ENVIADA", nullable=False)
    conteudo = Column(String(500), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    enviada_em = Column(DateTime(timezone=True), nullable=True)

    cliente = relationship("Cliente", back_populates="mensagens")
    encomenda = relationship("Encomenda", back_populates="mensagens")
    movimentacao = relationship("Movimentacao", back_populates="mensagem")
