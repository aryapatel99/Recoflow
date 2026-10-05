
from __future__ import annotations

from collections import Counter

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.ml.recommender import (
    ProductRecord,
    build_collaborative_scores,
    build_content_scores,
    build_popularity_scores,
    cosine_similarity,
    filter_seen_products,
    hybrid_scores,
    rank_candidates,
    tokenize,
)
from backend.app.models.event import UserEvent
from backend.app.models.product import Product


class RecommendationService:

    # Compatibility helpers for the original Day 7 unit tests.
    @staticmethod
    def _tokenize(text: str) -> Counter[str]:
        return tokenize(text)

    @staticmethod
    def _cosine_similarity(
        vector_a: Counter[str],
        vector_b: Counter[str],
    ) -> float:
        return cosine_similarity(
            vector_a,
            vector_b,
        )

    @staticmethod
    def _load_products(
        db: Session,
    ) -> list[ProductRecord]:
        products = db.scalars(
            select(Product).where(
                Product.is_active.is_(True)
            )
        ).all()

        result = []

        for product in products:
            result.append(
                ProductRecord(
                    product_id=int(product.id),
                    external_id=str(
                        product.external_id
                    ),
                    title=product.title or "",
                    description=product.description,
                    brand=product.brand,
                    category_id=(
                        int(product.category_id)
                        if product.category_id is not None
                        else None
                    ),
                    price=float(
                        product.price or 0
                    ),
                    rating=float(
                        product.rating or 0
                    ),
                    review_count=int(
                        product.review_count or 0
                    ),
                    features=product.features,
                )
            )

        return result

    @staticmethod
    def _load_events(
        db: Session,
    ) -> list[dict]:
        events = db.scalars(
            select(UserEvent)
        ).all()

        return [
            {
                "user_id": int(event.user_id),
                "product_id": (
                    int(event.product_id)
                    if event.product_id is not None
                    else None
                ),
                "event_type": event.event_type,
                "occurred_at": event.occurred_at,
            }
            for event in events
        ]

    @staticmethod
    def _to_response_item(
        product: ProductRecord,
        score: float,
        strategy: str,
    ) -> dict:
        return {
            "product_id": product.product_id,
            "external_id": product.external_id,
            "title": product.title,
            "score": round(
                float(score),
                6,
            ),
            "strategy": strategy,
        }

    @classmethod
    def collaborative(
        cls,
        db: Session,
        user_id: int,
        limit: int = 10,
    ) -> dict:
        products = cls._load_products(db)
        events = cls._load_events(db)

        user_events = [
            event
            for event in events
            if event["user_id"] == int(user_id)
        ]

        scores = build_collaborative_scores(
            user_id=user_id,
            events=events,
        )

        scores = filter_seen_products(
            scores,
            user_events,
        )

        ranked = sorted(
            scores.items(),
            key=lambda item: item[1],
            reverse=True,
        )[:limit]

        products_by_id = {
            product.product_id: product
            for product in products
        }

        items = []

        for product_id, score in ranked:
            product = products_by_id.get(
                product_id
            )

            if not product:
                continue

            items.append(
                cls._to_response_item(
                    product,
                    score,
                    "collaborative",
                )
            )

        return {
            "user_id": int(user_id),
            "strategy": "collaborative",
            "count": len(items),
            "items": items,
        }

    @classmethod
    def hybrid(
        cls,
        db: Session,
        user_id: int,
        limit: int = 10,
    ) -> dict:
        products = cls._load_products(db)
        events = cls._load_events(db)

        user_events = [
            event
            for event in events
            if event["user_id"] == int(user_id)
        ]

        popularity = build_popularity_scores(
            events,
            products,
        )

        content = build_content_scores(
            user_events,
            products,
        )

        collaborative = build_collaborative_scores(
            user_id,
            events,
        )

        popularity = filter_seen_products(
            popularity,
            user_events,
        )

        content = filter_seen_products(
            content,
            user_events,
        )

        collaborative = filter_seen_products(
            collaborative,
            user_events,
        )

        combined = hybrid_scores(
            popularity,
            content,
            collaborative,
        )

        ranked = rank_candidates(
            combined,
            limit=limit,
        )

        products_by_id = {
            product.product_id: product
            for product in products
        }

        items = []

        for candidate in ranked:
            product = products_by_id.get(
                candidate.product_id
            )

            if not product:
                continue

            items.append(
                cls._to_response_item(
                    product,
                    candidate.score,
                    "hybrid",
                )
            )

        return {
            "user_id": int(user_id),
            "strategy": "hybrid",
            "count": len(items),
            "items": items,
        }

    @classmethod
    def _rank(
        cls,
        db: Session,
        user_id: int,
        limit: int,
        strategy: str,
    ) -> dict:
        products = cls._load_products(db)
        events = cls._load_events(db)
        user_events = [event for event in events if event["user_id"] == int(user_id)]
        if strategy == "popular":
            scores = build_popularity_scores(events, products)
        elif strategy == "content-based":
            scores = build_content_scores(user_events, products)
        else:
            raise ValueError(f"Unsupported recommendation strategy: {strategy}")
        scores = filter_seen_products(scores, user_events)
        ranked = rank_candidates(scores, limit=limit)
        products_by_id = {product.product_id: product for product in products}
        items = [
            cls._to_response_item(products_by_id[candidate.product_id], candidate.score, strategy)
            for candidate in ranked
            if candidate.product_id in products_by_id
        ]
        return {
            "user_id": int(user_id),
            "strategy": strategy,
            "count": len(items),
            "items": items,
        }

    @classmethod
    def popular(cls, db: Session, user_id: int, limit: int = 10) -> dict:
        return cls._rank(db, user_id, limit, "popular")

    @classmethod
    def content_based(cls, db: Session, user_id: int, limit: int = 10) -> dict:
        return cls._rank(db, user_id, limit, "content-based")
