from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.app.repositories.product_repository import ProductRepository
from backend.app.schemas.product import (
    CategoryCreate,
    ProductCreate,
    ProductUpdate,
)


class ProductService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ProductRepository(db)

    def list_products(
        self,
        page: int,
        page_size: int,
        search: str | None,
        category_id: int | None,
        brand: str | None,
        active_only: bool,
    ):
        return self.repository.list_products(
            page=page,
            page_size=page_size,
            search=search,
            category_id=category_id,
            brand=brand,
            active_only=active_only,
        )

    def get_product(self, product_id: int):
        return self.repository.get_product(product_id)

    def get_product_by_external_id(self, external_id: str):
        return self.repository.get_product_by_external_id(
            external_id
        )

    def list_categories(self):
        return self.repository.list_categories()

    def create_category(
        self,
        category_data: CategoryCreate,
    ):
        existing = self.repository.get_category_by_name(
            category_data.name
        )

        if existing:
            raise ValueError("Category already exists")

        try:
            category = self.repository.create_category(
                name=category_data.name,
                parent_category_id=category_data.parent_category_id,
            )

            self.db.commit()
            self.db.refresh(category)

            return category

        except IntegrityError:
            self.db.rollback()
            raise ValueError(
                "Category could not be created"
            )

    def create_product(
        self,
        product_data: ProductCreate,
    ):
        existing = self.repository.get_product_by_external_id(
            product_data.external_id
        )

        if existing:
            raise ValueError(
                "Product with this external_id already exists"
            )

        if product_data.category_id is not None:
            category = self.repository.get_category(
                product_data.category_id
            )

            if category is None:
                raise ValueError(
                    "Category does not exist"
                )

        try:
            product = self.repository.create_product(
                product_data.model_dump()
            )

            self.db.commit()
            self.db.refresh(product)

            return product

        except IntegrityError:
            self.db.rollback()
            raise ValueError(
                "Product could not be created"
            )

    def update_product(
        self,
        product_id: int,
        product_data: ProductUpdate,
    ):
        product = self.repository.get_product(product_id)

        if product is None:
            return None

        update_data = product_data.model_dump(
            exclude_unset=True
        )

        if "category_id" in update_data:
            category_id = update_data["category_id"]

            if category_id is not None:
                category = self.repository.get_category(
                    category_id
                )

                if category is None:
                    raise ValueError(
                        "Category does not exist"
                    )

        try:
            product = self.repository.update_product(
                product,
                update_data,
            )

            self.db.commit()
            self.db.refresh(product)

            return product

        except IntegrityError:
            self.db.rollback()
            raise ValueError(
                "Product could not be updated"
            )