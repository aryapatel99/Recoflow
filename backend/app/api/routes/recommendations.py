from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.api.dependencies import (
    get_current_user,
    get_db,
)
from backend.app.models.user import User
from backend.app.schemas.recommendation import (
    RecommendationResponse,
)
from backend.app.services.recommendation_service import (
    RecommendationService,
)


router = APIRouter(
    prefix="/api/v1/recommendations",
    tags=["Recommendations"],
)


@router.get(
    "/popular",
    response_model=RecommendationResponse,
)
def get_popular_recommendations(
    limit: int = Query(
        default=10,
        ge=1,
        le=50,
    ),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return RecommendationService.popular(
        db,
        current_user.id,
        limit,
    )


@router.get(
    "/content-based",
    response_model=RecommendationResponse,
)
def get_content_based_recommendations(
    limit: int = Query(
        default=10,
        ge=1,
        le=50,
    ),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return RecommendationService.content_based(
        db,
        current_user.id,
        limit,
    )