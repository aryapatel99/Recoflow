from pydantic import BaseModel


class EvaluationResponse(BaseModel):
    users_evaluated: int
    k: int
    precision_at_k: float
    recall_at_k: float
    ndcg_at_k: float
    coverage: float
    diversity: float