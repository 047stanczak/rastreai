import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class MovimentacaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    encomenda_id: uuid.UUID
    status: str
    descricao: Optional[str] = None
    local: Optional[str] = None
    data_evento: Optional[datetime] = None
    created_at: datetime
