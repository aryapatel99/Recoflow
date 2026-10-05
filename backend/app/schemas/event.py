from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


ALLOWED_EVENT_TYPES = {
    "product_view",
    "product_click",
    "search",
    "add_to_cart",
    "purchase",
    "wishlist_add",
    "recommendation_impression",
    "recommendation_click",
}


class EventCreate(BaseModel):
    event_id: str = Field(
        min_length=1,
        max_length=100,
    )

    session_id: str | None = Field(
        default=None,
        max_length=100,
    )

    event_type: str = Field(
        min_length=1,
        max_length=50,
    )

    product_id: int | None = None

    occurred_at: datetime | None = None

    metadata: dict[str, Any] | None = None

    @field_validator("event_type")
    @classmethod
    def validate_event_type(cls, value: str) -> str:
        if value not in ALLOWED_EVENT_TYPES:
            raise ValueError(
                f"Unsupported event_type: {value}"
            )

        return value


class EventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    event_id: str
    user_id: int
    session_id: str | None
    event_type: str
    product_id: int | None
    occurred_at: datetime
    received_at: datetime
    metadata: dict[str, Any] | None = Field(
        default=None,
        validation_alias="event_metadata",
    )


class BatchEventCreate(BaseModel):
    events: list[EventCreate] = Field(
        min_length=1,
        max_length=100,
    )


class BatchEventResponse(BaseModel):
    events: list[EventResponse]
    accepted: int