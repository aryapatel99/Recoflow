from decimal import Decimal

from sqlalchemy import select

from backend.app.db.database import SessionLocal
from backend.app.models.product import Category, Product


CATEGORIES = [
    "Electronics",
    "Computers",
    "Mobile Accessories",
    "Audio",
]


PRODUCTS = [
    {
        "external_id": "RF-LAPTOP-001",
        "title": "RecoFlow Performance Laptop",
        "description": "Demo laptop product for RecoFlow catalog testing.",
        "price": Decimal("89999.00"),
        "brand": "RecoTech",
        "category": "Computers",
        "features": {
            "ram": "16GB",
            "storage": "1TB SSD",
            "processor": "Performance CPU",
        },
        "images": [],
        "rating": Decimal("4.50"),
        "review_count": 124,
    },
    {
        "external_id": "RF-PHONE-001",
        "title": "RecoFlow Smart Phone",
        "description": "Demo smartphone product.",
        "price": Decimal("49999.00"),
        "brand": "RecoTech",
        "category": "Electronics",
        "features": {
            "display": "6.7 inch",
            "storage": "256GB",
        },
        "images": [],
        "rating": Decimal("4.30"),
        "review_count": 87,
    },
    {
        "external_id": "RF-HEADPHONE-001",
        "title": "RecoFlow Wireless Headphones",
        "description": "Wireless over-ear headphones for testing.",
        "price": Decimal("6999.00"),
        "brand": "RecoAudio",
        "category": "Audio",
        "features": {
            "type": "Over-ear",
            "wireless": True,
            "noise_cancellation": True,
        },
        "images": [],
        "rating": Decimal("4.60"),
        "review_count": 312,
    },
    {
        "external_id": "RF-MOUSE-001",
        "title": "RecoFlow Wireless Mouse",
        "description": "Wireless productivity mouse.",
        "price": Decimal("1499.00"),
        "brand": "RecoGear",
        "category": "Computers",
        "features": {
            "connection": "2.4GHz",
            "buttons": 6,
        },
        "images": [],
        "rating": Decimal("4.20"),
        "review_count": 201,
    },
    {
        "external_id": "RF-KEYBOARD-001",
        "title": "RecoFlow Mechanical Keyboard",
        "description": "Mechanical keyboard for developers and gamers.",
        "price": Decimal("3999.00"),
        "brand": "RecoGear",
        "category": "Computers",
        "features": {
            "switch": "Mechanical",
            "layout": "Full-size",
        },
        "images": [],
        "rating": Decimal("4.40"),
        "review_count": 156,
    },
    {
        "external_id": "RF-USB-001",
        "title": "RecoFlow USB-C Hub",
        "description": "Multi-port USB-C hub.",
        "price": Decimal("2499.00"),
        "brand": "RecoGear",
        "category": "Mobile Accessories",
        "features": {
            "ports": 7,
            "connection": "USB-C",
        },
        "images": [],
        "rating": Decimal("4.10"),
        "review_count": 98,
    },
    {
        "external_id": "RF-CHARGER-001",
        "title": "RecoFlow Fast Charger",
        "description": "High-speed USB-C charging adapter.",
        "price": Decimal("1799.00"),
        "brand": "RecoPower",
        "category": "Mobile Accessories",
        "features": {
            "power": "65W",
            "port": "USB-C",
        },
        "images": [],
        "rating": Decimal("4.50"),
        "review_count": 276,
    },
    {
        "external_id": "RF-EARBUD-001",
        "title": "RecoFlow Wireless Earbuds",
        "description": "Compact wireless earbuds.",
        "price": Decimal("2999.00"),
        "brand": "RecoAudio",
        "category": "Audio",
        "features": {
            "wireless": True,
            "microphone": True,
        },
        "images": [],
        "rating": Decimal("4.30"),
        "review_count": 189,
    },
]


def get_or_create_category(
    db,
    name: str,
):
    statement = select(Category).where(
        Category.name == name
    )

    category = db.execute(
        statement
    ).scalar_one_or_none()

    if category:
        return category

    category = Category(
        name=name,
    )

    db.add(category)
    db.flush()

    return category


def seed():
    db = SessionLocal()

    try:
        category_map = {}

        for category_name in CATEGORIES:
            category_map[category_name] = (
                get_or_create_category(
                    db,
                    category_name,
                )
            )

        db.commit()

        created = 0
        skipped = 0

        for item in PRODUCTS:
            statement = select(Product).where(
                Product.external_id
                == item["external_id"]
            )

            existing = db.execute(
                statement
            ).scalar_one_or_none()

            if existing:
                skipped += 1
                continue

            category = category_map[
                item["category"]
            ]

            product = Product(
                parent_product_id=None,
                external_id=item["external_id"],
                title=item["title"],
                description=item["description"],
                price=item["price"],
                brand=item["brand"],
                category_id=category.id,
                features=item["features"],
                images=item["images"],
                rating=item["rating"],
                review_count=item["review_count"],
                is_active=True,
            )

            db.add(product)
            created += 1

        db.commit()

        print(
            f"Catalog seed complete. "
            f"Created: {created}, "
            f"Skipped: {skipped}"
        )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed()