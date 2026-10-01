from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from backend.app.api.dependencies import get_current_user, get_db
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
        email=data.email,
        full_name=data.full_name,
        password=data.password,
    )

    return RegisterResponse(
    message="Registration successful. Verify your email before logging in.",
    email=user.email,
    email_verified=user.is_email_verified,
    verification_token=verification_token,
)


@router.get(
    "/verify-email",
    response_model=VerifyEmailResponse,
)
def verify_email(
    token: str = Query(...),
    db: Session = Depends(get_db),
):
    user = AuthService.verify_email(
        db,
        token=token,
    )

    return VerifyEmailResponse(
        message="Email verified successfully.",
        email=user.email,
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
        email=data.email,
        password=data.password,
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user=Depends(get_current_user),
):
    return current_user