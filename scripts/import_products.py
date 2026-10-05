"""Import a small, reproducible Amazon Electronics metadata catalog.

The source is the Amazon Reviews 2023 Electronics metadata JSONL file:
https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023

The full source is several gigabytes. For local catalog work, download a
bounded byte range to data/raw/meta_Electronics.sample.jsonl and pass that
file to this script. The importer is deliberately idempotent and never
removes existing products.
"""

from __future__ import annotations

import argparse
import json
import re
from collections.abc import Iterator
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from sqlalchemy import func, select

from backend.app.db.database import SessionLocal
from backend.app.models.product import Category, Product
from backend.app.services.catalog_pricing import price_for_product


DEFAULT_SOURCE = Path("data/raw/meta_Electronics.sample.jsonl")
DEFAULT_TARGET = 92
CATEGORY_NAMES = ("Electronics", "Computers", "Mobile Accessories", "Audio")
PRICE_PATTERN = re.compile(r"[-+]?(?:\d+(?:,\d{3})*|\d+)(?:\.\d+)?")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help="JSONL metadata file to import",
    )
    parser.add_argument(
        "--target-new",
        type=int,
        default=DEFAULT_TARGET,
        help="maximum number of new products to import",
    )
    return parser.parse_args()


def iter_records(source: Path) -> Iterator[dict[str, Any]]:
    with source.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(record, dict):
                yield record


def first_text(value: Any) -> str | None:
    if isinstance(value, str) and value.strip():
        return value.strip()
    if isinstance(value, list):
        for item in value:
            text = first_text(item)
            if text:
                return text
    return None


def parse_price(value: Any) -> Decimal | None:
    if isinstance(value, (int, float)):
        return Decimal(str(value)).quantize(Decimal("0.01"))
    if not isinstance(value, str):
        return None
    match = PRICE_PATTERN.search(value.replace(",", ""))
    if not match:
        return None
    try:
        return Decimal(match.group()).quantize(Decimal("0.01"))
    except InvalidOperation:
        return None


def image_urls(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    urls: list[str] = []
    for image in value:
        if not isinstance(image, dict):
            continue
        for key in ("hi_res", "large", "thumb"):
            url = image.get(key)
            if isinstance(url, str) and url.startswith(("http://", "https://")):
                if url not in urls:
                    urls.append(url)
                break
    return urls[:6]


def category_for(record: dict[str, Any]) -> str:
    values = [
        first_text(record.get("main_category")) or "",
        " ".join(
            value
            for value in record.get("categories", [])
            if isinstance(value, str)
        ),
        first_text(record.get("title")) or "",
    ]
    text = " ".join(values).lower()

    if any(term in text for term in ("headphone", "earbud", "speaker", "audio", "microphone")):
        return "Audio"
    if any(
        term in text
        for term in ("laptop", "computer", "desktop", "keyboard", "mouse", "monitor", "pc ")
    ):
        return "Computers"
    if any(
        term in text
        for term in ("charger", "cable", "usb", "phone", "tablet", "mobile", "power bank")
    ):
        return "Mobile Accessories"
    return "Electronics"


def normalize(record: dict[str, Any]) -> dict[str, Any] | None:
    external_id = first_text(record.get("asin")) or first_text(record.get("parent_asin"))
    title = first_text(record.get("title"))
    images = image_urls(record.get("images"))
    if not external_id or not title or not images:
        return None

    details = record.get("details")
    details = details if isinstance(details, dict) else {}
    brand = first_text(details.get("Brand")) or first_text(record.get("store"))
    description = first_text(record.get("description"))
    features = record.get("features")
    if not isinstance(features, list):
        features = []

    return {
        "external_id": external_id[:100],
        "parent_product_id": first_text(record.get("parent_asin")),
        "title": title[:1000],
        "description": description,
        "price": parse_price(record.get("price")),
        "brand": brand[:255] if brand else None,
        "category": category_for(record),
        "features": features,
        "images": images,
        "rating": record.get("average_rating"),
        "review_count": int(record.get("rating_number") or 0),
    }


def get_or_create_category(db: Any, name: str) -> Category:
    category = db.scalar(select(Category).where(Category.name == name))
    if category:
        return category
    category = Category(name=name)
    db.add(category)
    db.flush()
    return category


def import_products(source: Path, target_new: int) -> None:
    if not source.exists():
        raise FileNotFoundError(
            f"Metadata source not found: {source}. "
            "Download a bounded sample of meta_Electronics.jsonl first."
        )

    db = SessionLocal()
    try:
        categories = {
            name: get_or_create_category(db, name) for name in CATEGORY_NAMES
        }
        db.commit()

        existing_ids = set(
            db.scalars(select(Product.external_id)).all()
        )
        discovered = 0
        selected = 0
        skipped = 0
        with_images = 0
        candidates: list[dict[str, Any]] = []
        seen_source_ids: set[str] = set()

        for record in iter_records(source):
            discovered += 1
            if len(candidates) >= target_new:
                break
            item = normalize(record)
            if item is None:
                skipped += 1
                continue
            external_id = item["external_id"]
            if external_id in seen_source_ids:
                skipped += 1
                continue
            seen_source_ids.add(external_id)
            candidates.append(item)

        for item in candidates:
            external_id = item["external_id"]
            if external_id in existing_ids:
                skipped += 1
                continue

            product = Product(
                parent_product_id=item["parent_product_id"],
                external_id=external_id,
                title=item["title"],
                description=item["description"],
                price=item["price"]
                if item["price"] is not None and item["price"] > 500
                else price_for_product(
                    title=item["title"],
                    category=item["category"],
                    external_id=external_id,
                ),
                brand=item["brand"],
                category_id=categories[item["category"]].id,
                features=item["features"],
                images=item["images"],
                rating=item["rating"],
                review_count=item["review_count"],
                is_active=True,
            )
            db.add(product)
            existing_ids.add(external_id)
            selected += 1
            with_images += 1

        db.commit()
        total = db.scalar(select(func.count()).select_from(Product)) or 0
        print(f"Source: {source}")
        print(f"Products discovered: {discovered}")
        print(f"Products selected: {selected}")
        print(f"Products inserted: {selected}")
        print(f"Products skipped: {skipped}")
        print(f"Products with images: {with_images}")
        print(f"Products without images: 0")
        print(f"Total products now: {total}")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    arguments = parse_args()
    import_products(arguments.source, arguments.target_new)
