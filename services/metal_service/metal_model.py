from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class MetalModel(BaseModel):
    id: int
    type: str
    name: str
    price: Decimal
    available: bool
    created_at: datetime


class CreateMetalModel(BaseModel):
    type: str
    name: str
    price: Decimal


class UpdateMetalModel(BaseModel):
    type: Optional[str]
    name: Optional[str]
    price: Optional[Decimal]
    available: Optional[bool]


class UpdateMetalShortModel(BaseModel):
    price: Optional[Decimal]
    available: Optional[bool]
