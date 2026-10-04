from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.user import User


class UserRepository:

    @staticmethod
    def get_by_id(
        db: Session,
        user_id: int,
    ) -> User | None:
        return db.get(User, user_id)

    @staticmethod
    def get_by_email(
        db: Session,
        email: str,
    ) -> User | None:
        statement = select(User).where(User.email == email)
        return db.execute(statement).scalar_one_or_none()

    @staticmethod
    def create(
        db: Session,
        *,
        email: str,
        first_name: str | None,
        last_name: str | None,
        password_hash: str,
    ) -> User:
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password_hash=password_hash,
            is_email_verified=True,
            is_active=True,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user
