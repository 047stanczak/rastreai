import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


class ClienteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nome: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime
