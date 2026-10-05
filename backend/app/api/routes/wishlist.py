from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.api.dependencies import get_current_user, get_db
from backend.app.schemas.wishlist import WishlistItemCreate, WishlistResponse
from backend.app.services.wishlist_service import WishlistService

router = APIRouter(prefix="/api/v1/wishlist", tags=["Wishlist"])


@router.get("", response_model=WishlistResponse)
def get_wishlist(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return WishlistService(db).get(current_user.id)


@router.post("/items", response_model=WishlistResponse)
def add_wishlist_item(payload: WishlistItemCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return WishlistService(db).add(current_user.id, payload.product_id)


@router.delete("/items/{product_id}", response_model=WishlistResponse)
def remove_wishlist_item(product_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return WishlistService(db).remove(current_user.id, product_id)