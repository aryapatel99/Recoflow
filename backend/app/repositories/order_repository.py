from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from backend.app.models.order import Order


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id_for_user(self, order_id: int, user_id: int) -> Order | None:
        statement = (
            select(Order)
            .options(joinedload(Order.items))
            .where(Order.id == order_id, Order.user_id == user_id)
        )
        return self.db.execute(statement).unique().scalar_one_or_none()

    def get_by_idempotency_key(self, key: str, user_id: int) -> Order | None:
        statement = (
            select(Order)
            .options(joinedload(Order.items))
            .where(Order.idempotency_key == key, Order.user_id == user_id)
        )
        return self.db.execute(statement).unique().scalar_one_or_none()

    def list_for_user(self, user_id: int) -> list[Order]:
        statement = (
            select(Order)
            .options(joinedload(Order.items))
            .where(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
        )
        return list(self.db.execute(statement).unique().scalars().all())
