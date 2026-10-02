from collections import Counter

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.event import UserEvent
from backend.app.models.product import Product


class RecommendationRepository:

    @staticmethod
    def get_active_products(
        db: Session,
    ) -> list[Product]:
        statement = (
            select(Product)
            .where(Product.is_active.is_(True))
            .order_by(Product.id)
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def get_user_events(
        db: Session,
        user_id: int,
    ) -> list[UserEvent]:
        statement = select(UserEvent).where(
            UserEvent.user_id == user_id
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def get_global_event_counts(
        db: Session,
    ) -> Counter:
        statement = select(UserEvent)

        events = db.scalars(statement).all()

        counts = Counter()

        for event in events:
            if event.product_id is not None:
                counts[event.product_id] += 1

        return counts