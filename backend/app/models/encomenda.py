import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Encomenda(Base):
    __tablename__ = "encomendas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("clientes.id"), nullable=False)
    codigo_rastreio = Column(String(50), nullable=False, index=True)
    transportadora = Column(String(80), nullable=True)
    status_atual = Column(String(120), nullable=True)
    ultima_consulta = Column(DateTime(timezone=True), nullable=True)
    ativa = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    cliente = relationship("Cliente", back_populates="encomendas")
    movimentacoes = relationship(
        "Movimentacao", back_populates="encomenda", cascade="all, delete-orphan"
    )
    mensagens = relationship("Mensagem", back_populates="encomenda", cascade="all, delete-orphan")
