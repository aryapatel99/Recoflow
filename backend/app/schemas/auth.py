from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    full_name: str = Field(min_length=2, max_length=120)


class RegisterResponse(BaseModel):
    user_id: UUID
    email: EmailStr
    full_name: str
    email_verified: bool
    message: str
    verification_token: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
    full_name: str
    email_verified: bool
    is_active: bool
    created_at: datetime


class VerifyEmailResponse(BaseModel):
    user_id: UUID
    email: EmailStr
    email_verified: bool
    message: str