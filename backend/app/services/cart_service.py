from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from backend.app.models.cart import Cart, CartItem
from backend.app.models.product import Product


class CartService:
    def __init__(self, db: Session):
        self.db = db

    def _cart(self, user_id: int) -> Cart:
        cart = self.db.execute(
            select(Cart).where(Cart.user_id == user_id, Cart.status == "active")
            .options(joinedload(Cart.items).joinedload(CartItem.product))
        ).unique().scalar_one_or_none()
        if cart is None:
            cart = Cart(user_id=user_id, status="active")
            self.db.add(cart)
            self.db.commit()
            self.db.refresh(cart)
        return cart

    def get(self, user_id: int) -> Cart:
        return self._cart(user_id)

    def upsert(self, user_id: int, product_id: int, quantity: int) -> Cart:
        product = self.db.get(Product, product_id)
        if product is None or not product.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product is unavailable.")
        cart = self._cart(user_id)
        item = next((item for item in cart.items if item.product_id == product_id), None)
        if item:
            item.quantity = quantity
        else:
            cart.items.append(CartItem(product_id=product_id, quantity=quantity, product=product))
        self.db.commit()
        return self._cart(user_id)

    def remove(self, user_id: int, product_id: int) -> Cart:
        cart = self._cart(user_id)
        cart.items = [item for item in cart.items if item.product_id != product_id]
        self.db.commit()
        return self._cart(user_id)

    def clear(self, user_id: int) -> Cart:
        cart = self._cart(user_id)
        cart.items.clear()
        self.db.commit()
        return self._cart(user_id)