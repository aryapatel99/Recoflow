from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.api.dependencies import get_current_user, get_db
from backend.app.schemas.product import (
    CategoryCreate,
    CategoryResponse,
    ProductCreate,
    ProductListResponse,
    ProductResponse,
    ProductUpdate,
)
from backend.app.services.product_service import ProductService


router = APIRouter(
    prefix="/api/v1/products",
    tags=["Products"],
)


@router.get(
    "",
    response_model=ProductListResponse,
)
def list_products(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    search: str | None = Query(default=None),
    category_id: int | None = Query(default=None, ge=1),
    brand: str | None = Query(default=None),
    active_only: bool = Query(default=True),
    db: Session = Depends(get_db),
):
    service = ProductService(db)

    products, total = service.list_products(
        page=page,
        page_size=page_size,
        search=search,
        category_id=category_id,
        brand=brand,
        active_only=active_only,
    )

    return ProductListResponse(
        items=products,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    service = ProductService(db)

    product = service.get_product(product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return product


@router.get(
    "/external/{external_id}",
    response_model=ProductResponse,
)
def get_product_by_external_id(
    external_id: str,
    db: Session = Depends(get_db),
):
    service = ProductService(db)

    product = service.get_product_by_external_id(
        external_id
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return product


@router.get(
    "/categories/all",
    response_model=list[CategoryResponse],
)
def list_categories(
    db: Session = Depends(get_db),
):
    service = ProductService(db)

    return service.list_categories()


@router.post(
    "/categories",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    payload: CategoryCreate,
    _current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ProductService(db)

    try:
        return service.create_category(payload)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    payload: ProductCreate,
    _current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ProductService(db)

    try:
        return service.create_product(payload)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.patch(
    "/{product_id}",
    response_model=ProductResponse,
)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    _current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ProductService(db)

    try:
        product = service.update_product(
            product_id,
            payload,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return product