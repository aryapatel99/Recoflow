from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class WishlistItemCreate(BaseModel):
    product_id: int


class WishlistProduct(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    price: Decimal | None
    images: list | None


class WishlistItemResponse(BaseModel):
    id: int
    product_id: int
    product: WishlistProduct


class WishlistResponse(BaseModel):
    id: int
    items: list[WishlistItemResponse]