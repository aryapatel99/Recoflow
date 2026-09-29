from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base


class SessionModel(Base):
    __tablename__ = "sessions"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    session_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    user_id: Mapped[UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
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

    user = relationship(
        "User",
    )

    events = relationship(
        "UserEvent",
        back_populates="session",
        primaryjoin="SessionModel.session_id == UserEvent.session_id",
        foreign_keys="UserEvent.session_id",
    )


class UserEvent(Base):
    __tablename__ = "user_events"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    event_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    parent_asin: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        index=True,
    )

    asin: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        index=True,
    )

    session_id: Mapped[str | None] = mapped_column(
        String(100),
        ForeignKey("sessions.session_id"),
        nullable=True,
    )

    search_query: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    event_metadata: Mapped[dict | None] = mapped_column(
        "metadata",
        JSONB,
        nullable=True,
    )

    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        index=True,
    )

    user = relationship(
        "User",
        back_populates="events",
    )

    session = relationship(
        "SessionModel",
        back_populates="events",
        primaryjoin="SessionModel.session_id == UserEvent.session_id",
        foreign_keys=[session_id],
    )