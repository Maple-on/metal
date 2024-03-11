from enum import Enum
from typing import Optional, List, Any
from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal


class Status(str, Enum):
    new = "New"
    processed = "Processed"


class Unit(str, Enum):
    m = "m"


class OrderModel(BaseModel):
    id: int
    client_name: str
    client_phone: str
    metal_type: str
    metal_name: str
    metal_price: Decimal
    amount: Decimal
    unit: Unit
    status: Status
    created_at: datetime
    updated_at: datetime


class CreateOrder(BaseModel):
    client_id: int
    metal_id: int
    amount: Decimal
    metal_price: Decimal


class CreateBaseOrder(BaseModel):
    client_id: int
    metal_id: int
    amount: Decimal


class UpdateOrder(BaseModel):
    amount: Decimal
    unit: Unit
    status: Status