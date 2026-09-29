from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.user import User


class UserRepository:

    @staticmethod
    def get_by_id(
        db: Session,
        user_id: UUID,
    ) -> User | None:
        return db.scalar(
            select(User).where(User.id == user_id)
        )

    @staticmethod
    def get_by_email(
        db: Session,
        email: str,
    ) -> User | None:
        return db.scalar(
            select(User).where(
                User.email == email.lower().strip()
            )
        )

    @staticmethod
    def get_by_verification_token_hash(
        db: Session,
        token_hash: str,
    ) -> User | None:
        return db.scalar(
            select(User).where(
                User.email_verification_token_hash == token_hash
            )
        )

    @staticmethod
    def create(
        db: Session,
        *,
        email: str,
        full_name: str,
        password_hash: str,
        verification_token_hash: str,
        verification_expires_at: datetime,
    ) -> User:

        user = User(
            email=email.lower().strip(),
            full_name=full_name.strip(),
            password_hash=password_hash,
            email_verified=False,
            email_verification_token_hash=verification_token_hash,
            email_verification_expires_at=verification_expires_at,
            is_active=True,
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

        user.email_verified = True
        user.email_verification_token_hash = None
        user.email_verification_expires_at = None

        db.commit()
        db.refresh(user)

        return user