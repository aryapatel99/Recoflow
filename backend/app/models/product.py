from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    parent_category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    parent = relationship(
        "Category",
        remote_side=[id],
        back_populates="children",
    )

    children = relationship(
        "Category",
        back_populates="parent",
    )

    products = relationship(
        "Product",
        back_populates="category",
    )


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    parent_product_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
    )

    external_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    price: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )

    brand: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True,
    )

    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    features: Mapped[list | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    images: Mapped[list | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    rating: Mapped[Decimal | None] = mapped_column(
        Numeric(3, 2),
        nullable=True,
    )

    review_count: Mapped[int] = mapped_column(
        default=0,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    category = relationship(
        "Category",
        back_populates="products",
    )

    events = relationship(
        "UserEvent",
        back_populates="product",
    )

    cart_items = relationship(
        "CartItem",
        back_populates="product",
    )

    wishlist_items = relationship(
        "WishlistItem",
        back_populates="product",
    )

    order_items = relationship(
        "OrderItem",
        back_populates="product",
    )

    recommendation_items = relationship(
        "RecommendationItem",
        back_populates="product",
    )

    recommendation_impressions = relationship(
        "RecommendationImpression",
        back_populates="product",
    )

    __table_args__ = (
        UniqueConstraint(
            "external_id",
            name="products_external_id_key",
        ),
        Index(
            "ix_products_external_id",
            "external_id",
        ),
    )