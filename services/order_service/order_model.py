from enum import Enum
from typing import Optional, List, Any
from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal


class Status(str, Enum):
    new = "New"
    processed = "Processed"
    declined = "Declined"


class Unit(str, Enum):
    m = "m"


class OrderModel(BaseModel):
    id: int
    client_name: str
    client_phone: str
    order: Any
    total_sum: Decimal
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
    metal_category: str
    metal_subcategory: str
    amount: Decimal


class UpdateOrder(BaseModel):
    status: Status