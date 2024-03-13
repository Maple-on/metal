from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class MetalModel(BaseModel):
    id: int
    category: str
    subcategory: str
    price: Decimal
    available: bool
    created_at: datetime
    updated_at: datetime


class CreateMetalModel(BaseModel):
    category: str
    subcategory: str
    price: Decimal


class UpdateMetalModel(BaseModel):
    category: Optional[str]
    subcategory: Optional[str]
    price: Optional[Decimal]
    available: Optional[bool]


class UpdateMetalShortModel(BaseModel):
    price: Optional[Decimal]
    available: Optional[bool]
