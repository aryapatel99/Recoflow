from datetime import datetime
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
    def get_by_verification_token_hash(
        db: Session,
        token_hash: str,
    ) -> User | None:
        statement = select(User).where(
            User.email_verification_token_hash == token_hash
        )
        return db.execute(statement).scalar_one_or_none()

    @staticmethod
    def create(
        db: Session,
        *,
        email: str,
        first_name: str | None,
        last_name: str | None,
        password_hash: str,
        verification_token_hash: str,
        verification_expires_at: datetime,
    ) -> User:
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password_hash=password_hash,
            is_email_verified=False,
            is_active=True,
            email_verification_token_hash=verification_token_hash,
            email_verification_expires_at=verification_expires_at,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def mark_email_verified(
        db: Session,
        user: User,
    ) -> User:
        user.is_email_verified = True
        user.email_verification_token_hash = None
        user.email_verification_expires_at = None

        db.commit()
        db.refresh(user)

        return user