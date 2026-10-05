"""Repair missing or low catalog prices without changing product identity."""

from sqlalchemy import select

from backend.app.db.database import SessionLocal
from backend.app.models.product import Product
from backend.app.services.catalog_pricing import price_for_product


def repair_product_prices() -> int:
    db = SessionLocal()
    changed = 0
    try:
        products = db.scalars(select(Product).order_by(Product.id)).all()
        for product in products:
            text = f"{product.title} {product.category.name if product.category else ''}".lower()
            accessory_terms = ("case", "cover", "stand", "holder", "skin", "decal", "sticker", "band", "strap")
            clearly_misclassified = (
                product.price is not None
                and product.price > 10000
                and any(term in text for term in accessory_terms)
            )
            if (
                product.price is not None
                and product.price > 500
                and not clearly_misclassified
            ):
                continue
            category = product.category.name if product.category else None
            product.price = price_for_product(
                title=product.title,
                category=category,
                external_id=product.external_id,
            )
            changed += 1
        db.commit()
        return changed
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print(f"Products repriced: {repair_product_prices()}")
