from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    parent_category_id: int | None = None


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ProductBase(BaseModel):
    parent_product_id: str | None = Field(default=None, max_length=100)
    external_id: str = Field(min_length=1, max_length=100)
    title: str = Field(min_length=1, max_length=1000)
    description: str | None = None
    price: Decimal | None = Field(default=None, ge=0)
    brand: str | None = Field(default=None, max_length=255)
    category_id: int | None = None
    features: dict | list | None = None
    images: list | dict | None = None
    rating: Decimal | None = Field(default=None, ge=0, le=5)
    review_count: int = Field(default=0, ge=0)
    is_active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    parent_product_id: str | None = Field(default=None, max_length=100)
    title: str | None = Field(default=None, min_length=1, max_length=1000)
    description: str | None = None
    price: Decimal | None = Field(default=None, ge=0)
    brand: str | None = Field(default=None, max_length=255)
    category_id: int | None = None
    features: dict | list | None = None
    images: list | dict | None = None
    rating: Decimal | None = Field(default=None, ge=0, le=5)
    review_count: int | None = Field(default=None, ge=0)
    is_active: bool | None = None


class ProductResponse(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: object
    updated_at: object


class ProductListResponse(BaseModel):
    items: list[ProductResponse]
    total: int
    page: int
    page_size: int