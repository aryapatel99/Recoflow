from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class DeliveryAddress(BaseModel):
    full_name: str = Field(min_length=1, max_length=200)
    line1: str = Field(min_length=1, max_length=200)
    line2: str | None = Field(default=None, max_length=200)
    city: str = Field(min_length=1, max_length=100)
    state: str = Field(min_length=1, max_length=100)
    postal_code: str = Field(min_length=1, max_length=20)
    country: str = Field(default="India", min_length=1, max_length=100)


class OrderItemCreate(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0, le=99)


class OrderCreate(BaseModel):
    items: list[OrderItemCreate] = Field(min_length=1, max_length=100)
    delivery_address: DeliveryAddress
    shipping_method: str = Field(pattern="^(standard|express)$")
    idempotency_key: str = Field(min_length=8, max_length=100)


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    quantity: int
    unit_price: Decimal


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    total_amount: Decimal
    delivery_address: DeliveryAddress
    shipping_method: str
    idempotency_key: str
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemResponse]