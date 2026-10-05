from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from backend.app.models.product import Product
from backend.app.models.wishlist import Wishlist, WishlistItem


class WishlistService:
    def __init__(self, db: Session):
        self.db = db

    def _wishlist(self, user_id: int) -> Wishlist:
        wishlist = self.db.execute(
            select(Wishlist).where(Wishlist.user_id == user_id)
            .options(joinedload(Wishlist.items).joinedload(WishlistItem.product))
        ).unique().scalar_one_or_none()
        if wishlist is None:
            wishlist = Wishlist(user_id=user_id)
            self.db.add(wishlist)
            self.db.commit()
            self.db.refresh(wishlist)
        return wishlist

    def get(self, user_id: int) -> Wishlist:
        return self._wishlist(user_id)

    def add(self, user_id: int, product_id: int) -> Wishlist:
        product = self.db.get(Product, product_id)
        if product is None or not product.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product is unavailable.")
        wishlist = self._wishlist(user_id)
        if not any(item.product_id == product_id for item in wishlist.items):
            wishlist.items.append(WishlistItem(product_id=product_id, product=product))
            self.db.commit()
        return self._wishlist(user_id)

    def remove(self, user_id: int, product_id: int) -> Wishlist:
        wishlist = self._wishlist(user_id)
        wishlist.items = [item for item in wishlist.items if item.product_id != product_id]
        self.db.commit()
        return self._wishlist(user_id)