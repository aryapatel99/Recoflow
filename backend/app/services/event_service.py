from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.app.repositories.event_repository import EventRepository
from backend.app.repositories.product_repository import ProductRepository
from backend.app.schemas.event import (
    BatchEventCreate,
    EventCreate,
)


class EventService:
    def __init__(self, db: Session):
        self.db = db
        self.events = EventRepository(db)
        self.products = ProductRepository(db)

    def _validate_product(
        self,
        product_id: int | None,
    ):
        if product_id is None:
            return None

        product = self.products.get_product(product_id)

        if product is None:
            raise ValueError(
                "Product does not exist"
            )

        if not product.is_active:
            raise ValueError(
                "Product is inactive"
            )

        return product

    def _get_or_create_session(
        self,
        session_id: str | None,
        user_id: int,
        occurred_at: datetime,
    ):
        if session_id:
            session = self.events.get_session(
                session_id
            )

            if session is None:
                raise ValueError(
                    "Session does not exist"
                )

            if session.user_id != user_id:
                raise PermissionError(
                    "Session does not belong to authenticated user"
                )

            return session

        generated_session_id = (
            f"session_{uuid4().hex}"
        )

        return self.events.create_session(
            session_id=generated_session_id,
            user_id=user_id,
            started_at=occurred_at,
        )

    def create_event(
        self,
        payload: EventCreate,
        user_id: int,
        commit: bool = True,
    ):
        existing = self.events.get_event_by_event_id(
            payload.event_id
        )

        if existing is not None:
            if existing.user_id != user_id:
                raise PermissionError(
                    "Event ID already belongs to another user"
                )

            return existing, False

        occurred_at = (
            payload.occurred_at
            or datetime.now(timezone.utc)
        )

        if occurred_at.tzinfo is None:
            occurred_at = occurred_at.replace(
                tzinfo=timezone.utc
            )

        now = datetime.now(timezone.utc)

        if occurred_at > now:
            raise ValueError(
                "occurred_at cannot be in the future"
            )

        self._validate_product(
            payload.product_id
        )

        session = self._get_or_create_session(
            session_id=payload.session_id,
            user_id=user_id,
            occurred_at=occurred_at,
        )

        event_data = {
            "event_id": payload.event_id,
            "user_id": user_id,
            "session_id": session.session_id,
            "event_type": payload.event_type,
            "product_id": payload.product_id,
            "occurred_at": occurred_at,
            "received_at": now,
            "event_metadata": payload.metadata,
        }

        try:
            event = self.events.create_event(
                event_data
            )

            if commit:
                self.db.commit()
            self.db.refresh(event)

            return event, True

        except IntegrityError:
            self.db.rollback()

            existing = self.events.get_event_by_event_id(
                payload.event_id
            )

            if existing is not None:
                return existing, False

            raise ValueError(
                "Event could not be created"
            )

    def create_batch(
        self,
        payload: BatchEventCreate,
        user_id: int,
    ):
        results = []

        for event_payload in payload.events:
            event, created = self.create_event(
                event_payload,
                user_id,
            )

            results.append(event)

        return results

    def list_my_events(
        self,
        user_id: int,
        limit: int,
    ):
        return self.events.list_user_events(
            user_id=user_id,
            limit=limit,
        )