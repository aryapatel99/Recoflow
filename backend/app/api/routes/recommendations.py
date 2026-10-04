from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.api.dependencies import (
    get_current_user,
    get_db,
)
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
    "/collaborative",
    response_model=RecommendationResponse,
)
def collaborative_recommendations(
    limit: int = Query(
        default=10,
        ge=1,
        le=50,
    ),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return RecommendationService.collaborative(
        db=db,
        user_id=int(current_user.id),
        limit=limit,
    )


@router.get(
    "/hybrid",
    response_model=RecommendationResponse,
)
def hybrid_recommendations(
    limit: int = Query(
        default=10,
        ge=1,
        le=50,
    ),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return RecommendationService.hybrid(
        db=db,
        user_id=int(current_user.id),
        limit=limit,
    )