from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.api.dependencies import get_current_user, get_db
from backend.app.schemas.cart import CartItemUpsert, CartResponse
from backend.app.services.cart_service import CartService

router = APIRouter(prefix="/api/v1/cart", tags=["Cart"])


@router.get("", response_model=CartResponse)
def get_cart(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return CartService(db).get(current_user.id)


@router.post("/items", response_model=CartResponse)
def upsert_cart_item(payload: CartItemUpsert, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return CartService(db).upsert(current_user.id, payload.product_id, payload.quantity)


@router.delete("/items/{product_id}", response_model=CartResponse)
def remove_cart_item(product_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return CartService(db).remove(current_user.id, product_id)


@router.delete("", response_model=CartResponse)
def clear_cart(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return CartService(db).clear(current_user.id)