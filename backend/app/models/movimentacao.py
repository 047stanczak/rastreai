import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Movimentacao(Base):
    __tablename__ = "movimentacoes"
    __table_args__ = (
        UniqueConstraint("encomenda_id", "dedup_hash", name="uq_movimentacao_dedup"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    encomenda_id = Column(UUID(as_uuid=True), ForeignKey("encomendas.id"), nullable=False)
    status = Column(String(120), nullable=False)
    descricao = Column(String(255), nullable=True)
    local = Column(String(120), nullable=True)
    data_evento = Column(DateTime(timezone=True), nullable=True)
    dedup_hash = Column(String(64), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    encomenda = relationship("Encomenda", back_populates="movimentacoes")
    mensagem = relationship("Mensagem", back_populates="movimentacao", uselist=False)
