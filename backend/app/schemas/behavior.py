from datetime import datetime

from pydantic import BaseModel


class BehaviorEventSummary(BaseModel):
    event_type: str
    count: int
    weight: float


class ProductBehaviorSummary(BaseModel):
    product_id: int
    score: float
    interaction_count: int
    last_interaction_at: datetime | None


class UserBehaviorResponse(BaseModel):
    user_id: int
    total_events: int
    unique_products: int
    event_breakdown: list[BehaviorEventSummary]
    top_products: list[ProductBehaviorSummary]