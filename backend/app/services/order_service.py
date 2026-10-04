from decimal import Decimal
from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.cart import Cart
from backend.app.models.order import Order, OrderItem
from backend.app.models.product import Product
from backend.app.repositories.order_repository import OrderRepository
from backend.app.schemas.event import EventCreate
from backend.app.schemas.order import OrderCreate
from backend.app.services.event_service import EventService


class OrderService:
    def __init__(self, db: Session):
        self.db = db
        self.orders = OrderRepository(db)

    def create_order(self, payload: OrderCreate, user_id: int) -> Order:
        existing = self.orders.get_by_idempotency_key(
            payload.idempotency_key, user_id
        )
        if existing:
            return existing

        product_ids = [item.product_id for item in payload.items]
        if len(product_ids) != len(set(product_ids)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cart contains a duplicate product.",
            )

        products = {
            product.id: product
            for product in self.db.execute(
                select(Product).where(
                    Product.id.in_(product_ids),
                    Product.is_active.is_(True),
                )
            ).scalars()
        }

        if len(products) != len(product_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="One or more cart products are unavailable.",
            )

        if any(products[item.product_id].price is None for item in payload.items):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="One or more cart products has no price.",
            )

        total = sum(
            (
                products[item.product_id].price * item.quantity
                for item in payload.items
            ),
            Decimal("0.00"),
        )
        order = Order(
            user_id=user_id,
            status="placed",
            total_amount=total,
            delivery_address=payload.delivery_address.model_dump(),
            shipping_method=payload.shipping_method,
            idempotency_key=payload.idempotency_key,
        )
        order.items = [
            OrderItem(
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=products[item.product_id].price,
            )
            for item in payload.items
        ]
        self.db.add(order)
        self.db.flush()

        EventService(self.db).create_event(
            EventCreate(
                event_id=f"purchase-order-{order.id}-{uuid4().hex}",
                event_type="purchase",
                metadata={
                    "order_id": order.id,
                    "total_amount": str(total),
                },
            ),
            user_id=user_id,
            commit=False,
        )

        active_cart = self.db.execute(
            select(Cart).where(
                Cart.user_id == user_id,
                Cart.status == "active",
            )
        ).scalar_one_or_none()
        if active_cart:
            active_cart.items.clear()
            active_cart.status = "completed"

        self.db.commit()
        self.db.refresh(order)
        return order

    def list_orders(self, user_id: int) -> list[Order]:
        return self.orders.list_for_user(user_id)

    def get_order(self, order_id: int, user_id: int) -> Order:
        order = self.orders.get_by_id_for_user(order_id, user_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found.",
            )
        return order
