from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.api.dependencies import (
    get_current_user,
    get_db,
)
from backend.app.models.user import User
from backend.app.schemas.event import (
    BatchEventCreate,
    BatchEventResponse,
    EventCreate,
    EventResponse,
)
from backend.app.services.event_service import EventService


router = APIRouter(
    prefix="/api/v1/events",
    tags=["Events"],
)


@router.post(
    "",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_event(
    payload: EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = EventService(db)

    try:
        event, created = service.create_event(
            payload=payload,
            user_id=current_user.id,
        )

    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    if not created:
        return event

    return event


@router.post(
    "/batch",
    response_model=BatchEventResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_event_batch(
    payload: BatchEventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = EventService(db)

    try:
        events = service.create_batch(
            payload=payload,
            user_id=current_user.id,
        )

    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    return BatchEventResponse(
        events=events,
        accepted=len(events),
    )


@router.get(
    "/me",
    response_model=list[EventResponse],
)
def list_my_events(
    limit: int = Query(
        default=50,
        ge=1,
        le=200,
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = EventService(db)

    return service.list_my_events(
        user_id=current_user.id,
        limit=limit,
    )