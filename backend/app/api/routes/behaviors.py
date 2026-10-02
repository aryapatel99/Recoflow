from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.api.dependencies import get_current_user, get_db
from backend.app.models.user import User
from backend.app.schemas.behavior import UserBehaviorResponse
from backend.app.services.behavior_service import BehaviorService


router = APIRouter(
    prefix="/api/v1/behaviors",
    tags=["Behavior"],
)


@router.get(
    "/me",
    response_model=UserBehaviorResponse,
)
def get_my_behavior(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return BehaviorService.get_user_behavior(
        db,
        current_user.id,
    )