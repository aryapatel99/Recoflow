from pydantic import BaseModel


class RecommendedProduct(BaseModel):
    product_id: int
    external_id: str
    title: str
    score: float
    strategy: str


class RecommendationResponse(BaseModel):
    user_id: int
    strategy: str
    count: int
    items: list[RecommendedProduct]