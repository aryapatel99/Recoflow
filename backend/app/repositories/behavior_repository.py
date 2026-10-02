from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.event import UserEvent


class BehaviorRepository:

    @staticmethod
    def get_user_events(
        db: Session,
        user_id: int,
    ) -> list[UserEvent]:
        statement = (
            select(UserEvent)
            .where(UserEvent.user_id == user_id)
            .order_by(UserEvent.occurred_at.desc())
        )

        return list(db.scalars(statement).all())