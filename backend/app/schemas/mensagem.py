import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class MensagemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    cliente_id: uuid.UUID
    encomenda_id: uuid.UUID
    movimentacao_id: uuid.UUID
    tipo: str
    status: str
    conteudo: str
    created_at: datetime
    enviada_em: Optional[datetime] = None
