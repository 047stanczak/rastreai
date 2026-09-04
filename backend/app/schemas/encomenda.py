import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class EncomendaCreate(BaseModel):
    codigo_rastreio: str


class EncomendaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    cliente_id: uuid.UUID
    codigo_rastreio: str
    transportadora: Optional[str] = None
    status_atual: Optional[str] = None
    ultima_consulta: Optional[datetime] = None
    ativa: bool
    created_at: datetime
    updated_at: datetime
