from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from backend.app.models.product import Category, Product


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_product(self, product_id: int) -> Product | None:
        return self.db.get(Product, product_id)

    def get_product_by_external_id(self, external_id: str) -> Product | None:
        statement = select(Product).where(
            Product.external_id == external_id
        )

        return self.db.execute(statement).scalar_one_or_none()

    def list_products(
        self,
        page: int,
        page_size: int,
        search: str | None = None,
        category_id: int | None = None,
        brand: str | None = None,
        active_only: bool = True,
    ) -> tuple[list[Product], int]:

        filters = []

        if active_only:
            filters.append(Product.is_active.is_(True))

        if category_id is not None:
            filters.append(Product.category_id == category_id)

        if brand:
            filters.append(Product.brand.ilike(f"%{brand}%"))

        if search:
            search_filter = or_(
                Product.title.ilike(f"%{search}%"),
                Product.description.ilike(f"%{search}%"),
                Product.brand.ilike(f"%{search}%"),
                Product.external_id.ilike(f"%{search}%"),
            )

            filters.append(search_filter)

        count_statement = select(
            func.count(Product.id)
        ).where(*filters)

        total = self.db.execute(count_statement).scalar_one()

        statement = (
            select(Product)
            .where(*filters)
            .order_by(Product.id.asc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        products = list(
            self.db.execute(statement).scalars().all()
        )

        return products, total

    def list_categories(self) -> list[Category]:
        statement = (
            select(Category)
            .order_by(Category.name.asc())
        )

        return list(
            self.db.execute(statement).scalars().all()
        )

    def get_category(self, category_id: int) -> Category | None:
        return self.db.get(Category, category_id)

    def get_category_by_name(self, name: str) -> Category | None:
        statement = select(Category).where(
            Category.name == name
        )

        return self.db.execute(statement).scalar_one_or_none()

    def create_category(
        self,
        name: str,
        parent_category_id: int | None,
    ) -> Category:

        category = Category(
            name=name,
            parent_category_id=parent_category_id,
        )

        self.db.add(category)
        self.db.flush()

        return category

    def create_product(
        self,
        product_data: dict,
    ) -> Product:

        product = Product(**product_data)

        self.db.add(product)
        self.db.flush()

        return product

    def update_product(
        self,
        product: Product,
        product_data: dict,
    ) -> Product:

        for field, value in product_data.items():
            setattr(product, field, value)

        self.db.flush()

        return product