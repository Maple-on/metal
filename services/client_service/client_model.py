from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class ClientModel(BaseModel):
    id: int
    username: str
    phone: str
    created_at: datetime


class CreateClientModel(BaseModel):
    username: str
    phone: str


class UpdateClientModel(BaseModel):
    username: Optional[str]
    phone: Optional[str]
