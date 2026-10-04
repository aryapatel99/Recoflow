from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base


class SessionModel(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    session_id: Mapped[str] = mapped_column(
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

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    ended_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    user = relationship(
        "User",
    )

    events = relationship(
        "UserEvent",
        back_populates="session",
    )

    __table_args__ = (
        UniqueConstraint(
            "session_id",
            name="sessions_session_id_key",
        ),
        Index(
            "ix_sessions_session_id",
            "session_id",
        ),
    )


class UserEvent(Base):
    __tablename__ = "user_events"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    event_id: Mapped[str] = mapped_column(
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

    session_id: Mapped[str | None] = mapped_column(
        ForeignKey(
            "sessions.session_id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    event_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    product_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "products.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    event_metadata: Mapped[dict | None] = mapped_column(
        "metadata",
        JSONB,
        nullable=True,
    )

    user = relationship(
        "User",
        back_populates="events",
    )

    session = relationship(
        "SessionModel",
        back_populates="events",
        foreign_keys=[session_id],
    )

    product = relationship(
        "Product",
        back_populates="events",
    )

    __table_args__ = (
        UniqueConstraint(
            "event_id",
            name="user_events_event_id_key",
        ),
        Index(
            "ix_user_events_event_id",
            "event_id",
        ),
        Index(
            "ix_user_events_user_occurred_at",
            "user_id",
            "occurred_at",
        ),
        Index(
            "ix_user_events_product_event_type",
            "product_id",
            "event_type",
        ),
    )