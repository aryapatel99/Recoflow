from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from backend.app.models.user import User
from backend.app.repositories.user_repository import UserRepository


class AuthService:
    @staticmethod
    def register(
        db: Session,
        *,
        email: str,
        full_name: str,
        password: str,
    ) -> User:
        email = email.strip().lower()

        existing_user = UserRepository.get_by_email(
            db,
            email,
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists.",
            )

        name_parts = full_name.strip().split(maxsplit=1)

        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else None

        password_hash = hash_password(password)

        user = UserRepository.create(
            db,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password_hash=password_hash,
        )
        return user

    @staticmethod
    def login(
        db: Session,
        *,
        email: str,
        password: str,
    ) -> str:

        user = UserRepository.get_by_email(
            db,
            email,
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive.",
            )

        access_token = create_access_token(str(user.id))

        return access_token

    @staticmethod
    def get_current_user(
        db: Session,
        *,
        token: str,
    ) -> User:

        subject = decode_access_token(token)

        if not subject:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token.",
                headers={
                    "WWW-Authenticate": "Bearer"
                },
            )

        try:
            user_id = int(subject)
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token.",
                headers={
                    "WWW-Authenticate": "Bearer"
                },
            )

        user = UserRepository.get_by_id(
            db,
            user_id,
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User no longer exists.",
                headers={
                    "WWW-Authenticate": "Bearer"
                },
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive.",
            )

        return user