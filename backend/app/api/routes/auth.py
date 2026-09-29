from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from backend.app.api.dependencies import (
    get_current_user,
    get_db,
)
from backend.app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
    UserResponse,
    VerifyEmailResponse,
)
from backend.app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db),
):
    user, verification_token = AuthService.register(
        db,
        data,
    )

    return RegisterResponse(
        user_id=user.id,
        email=user.email,
        full_name=user.full_name,
        email_verified=user.email_verified,
        message=(
            "Registration successful. "
            "Verify your email before logging in."
        ),
        verification_token=(
            verification_token
            if user.email_verified is False
            else None
        ),
    )


@router.get(
    "/verify-email",
    response_model=VerifyEmailResponse,
)
def verify_email(
    token: str = Query(
        min_length=20,
        max_length=200,
    ),
    db: Session = Depends(get_db),
):
    user = AuthService.verify_email(
        db,
        token,
    )

    return VerifyEmailResponse(
        user_id=user.id,
        email=user.email,
        email_verified=user.email_verified,
        message="Email address verified successfully.",
    )


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    access_token = AuthService.login(
        db,
        data,
    )

    from backend.app.core.config import settings

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.access_token_expire_minutes * 60,
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user=Depends(get_current_user),
):
    return current_user