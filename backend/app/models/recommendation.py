from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    request_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    strategy: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    context: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    model_version: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )

    user = relationship(
        "User",
        back_populates="recommendations",
    )

    items = relationship(
        "RecommendationItem",
        back_populates="recommendation",
        cascade="all, delete-orphan",
    )

    impressions = relationship(
        "RecommendationImpression",
        back_populates="recommendation",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint(
            "request_id",
            name="recommendations_request_id_key",
        ),
        Index(
            "ix_recommendations_request_id",
            "request_id",
        ),
    )


class RecommendationItem(Base):
    __tablename__ = "recommendation_items"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    recommendation_id: Mapped[int] = mapped_column(
        ForeignKey(
            "recommendations.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey(
            "products.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    score: Mapped[Decimal] = mapped_column(
        Numeric(12, 8),
        nullable=False,
    )

    position: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    recommendation = relationship(
        "Recommendation",
        back_populates="items",
    )

    product = relationship(
        "Product",
        back_populates="recommendation_items",
    )


class RecommendationImpression(Base):
    __tablename__ = "recommendation_impressions"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    recommendation_id: Mapped[int] = mapped_column(
        ForeignKey(
            "recommendations.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey(
            "products.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    position: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    shown_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    clicked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    recommendation = relationship(
        "Recommendation",
        back_populates="impressions",
    )

    product = relationship(
        "Product",
        back_populates="recommendation_impressions",
    )


class ModelMetadata(Base):
    __tablename__ = "model_metadata"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    model_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    model_version: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    strategy: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    dataset_version: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    artifact_location: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    training_timestamp: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="created",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )