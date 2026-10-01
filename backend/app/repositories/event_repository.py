from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.event import SessionModel, UserEvent


class EventRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_event_by_event_id(
        self,
        event_id: str,
    ) -> UserEvent | None:

        statement = select(UserEvent).where(
            UserEvent.event_id == event_id
        )

        return self.db.execute(
            statement
        ).scalar_one_or_none()

    def get_session(
        self,
        session_id: str,
    ) -> SessionModel | None:

        statement = select(SessionModel).where(
            SessionModel.session_id == session_id
        )

        return self.db.execute(
            statement
        ).scalar_one_or_none()

    def create_session(
        self,
        session_id: str,
        user_id: int,
        started_at: datetime,
    ) -> SessionModel:

        session = SessionModel(
            session_id=session_id,
            user_id=user_id,
            started_at=started_at,
        )

        self.db.add(session)
        self.db.flush()

        return session

    def create_event(
        self,
        event_data: dict,
    ) -> UserEvent:

        event = UserEvent(**event_data)

        self.db.add(event)
        self.db.flush()

        return event

    def list_user_events(
        self,
        user_id: int,
        limit: int = 50,
    ) -> list[UserEvent]:

        statement = (
            select(UserEvent)
            .where(UserEvent.user_id == user_id)
            .order_by(UserEvent.occurred_at.desc())
            .limit(limit)
        )

        return list(
            self.db.execute(statement).scalars().all()
        )