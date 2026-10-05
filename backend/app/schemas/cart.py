from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CartItemUpsert(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0, le=99)


class CartProduct(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    price: Decimal | None
    images: list | None


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    product: CartProduct


class CartResponse(BaseModel):
    id: int
    status: str
    items: list[CartItemResponse]