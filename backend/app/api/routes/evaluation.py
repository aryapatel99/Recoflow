from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.api.dependencies import get_current_user, get_db
from backend.app.schemas.evaluation import EvaluationResponse
from backend.app.services.evaluation_service import EvaluationService

router = APIRouter(
    prefix="/api/v1/evaluation",
    tags=["Evaluation"],
)


@router.get(
    "/recommendations",
    response_model=EvaluationResponse,
)
def evaluate_recommendations(
    k: int = Query(
        default=10,
        ge=1,
        le=50,
    ),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return EvaluationService.evaluate(
        db=db,
        k=k,
    )