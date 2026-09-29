from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.security import (
    create_access_token,
    generate_verification_token,
    hash_password,
    hash_verification_token,
    verify_password,
    verification_token_expiry,
)
from backend.app.repositories.user_repository import UserRepository
from backend.app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
)


class AuthService:

    @staticmethod
    def register(
        db: Session,
        data: RegisterRequest,
    ):
        email = str(data.email).lower().strip()

        existing_user = UserRepository.get_by_email(
            db,
            email,
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists.",
            )

        password_hash = hash_password(data.password)

        verification_token = generate_verification_token()

        verification_token_hash = hash_verification_token(
            verification_token
        )

        verification_expires_at = verification_token_expiry(
            hours=24
        )

        user = UserRepository.create(
            db,
            email=email,
            full_name=data.full_name,
            password_hash=password_hash,
            verification_token_hash=verification_token_hash,
            verification_expires_at=verification_expires_at,
        )

        return user, verification_token

    @staticmethod
    def verify_email(
        db: Session,
        token: str,
    ):
        token_hash = hash_verification_token(token)

        user = UserRepository.get_by_verification_token_hash(
            db,
            token_hash,
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email verification token.",
            )

        if user.email_verified:
            return user

        if (
            not user.email_verification_expires_at
            or user.email_verification_expires_at
            < datetime.now(timezone.utc)
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email verification token has expired.",
            )

        return UserRepository.mark_email_verified(
            db,
            user,
        )

    @staticmethod
    def login(
        db: Session,
        data: LoginRequest,
    ) -> str:

        email = str(data.email).lower().strip()

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
            data.password,
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

        if not user.email_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Email address has not been verified.",
            )

        return create_access_token(
            str(user.id)
        )

    @staticmethod
    def get_current_user(
        db: Session,
        user_id: str,
    ):
        try:
            parsed_user_id = UUID(user_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials.",
            )

        user = UserRepository.get_by_id(
            db,
            parsed_user_id,
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User no longer exists.",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive.",
            )

        return user