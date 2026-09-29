from fastapi import APIRouter, Depends

from backend.app.api.dependencies import get_current_user
from backend.app.schemas.auth import UserResponse


router = APIRouter(
    prefix="/auth-test",
    tags=["Authentication Test"],
)


@router.get(
    "/protected",
    response_model=UserResponse,
)
def protected_route(
    current_user=Depends(get_current_user),
):
    return current_user