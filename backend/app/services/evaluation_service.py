from __future__ import annotations

import math
from collections import defaultdict

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.ml.recommender import (
    ProductRecord,
    build_collaborative_scores,
    build_content_scores,
    build_popularity_scores,
    filter_seen_products,
    hybrid_scores,
    rank_candidates,
)
from backend.app.models.event import UserEvent
from backend.app.models.product import Product


class EvaluationService:

    @staticmethod
    def _load_products(
        db: Session,
    ) -> list[ProductRecord]:
        products = db.scalars(
            select(Product).where(
                Product.is_active.is_(True)
            )
        ).all()

        return [
            ProductRecord(
                product_id=int(product.id),
                external_id=str(product.external_id),
                title=product.title or "",
                description=product.description,
                brand=product.brand,
                category_id=(
                    int(product.category_id)
                    if product.category_id is not None
                    else None
                ),
                price=float(product.price or 0),
                rating=float(product.rating or 0),
                review_count=int(
                    product.review_count or 0
                ),
                features=product.features,
            )
            for product in products
        ]

    @staticmethod
    def _load_events(
        db: Session,
    ) -> list[dict]:
        events = db.scalars(
            select(UserEvent).order_by(
                UserEvent.occurred_at
            )
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
            if event.product_id is not None
        ]

    @staticmethod
    def _dcg(relevances: list[int]) -> float:
        return sum(
            relevance
            / math.log2(index + 2)
            for index, relevance in enumerate(relevances)
        )

    @classmethod
    def evaluate(
        cls,
        db: Session,
        k: int = 10,
    ) -> dict:
        products = cls._load_products(db)
        events = cls._load_events(db)

        by_user: dict[int, list[dict]] = defaultdict(list)

        for event in events:
            by_user[event["user_id"]].append(event)

        evaluated_users = 0

        precision_values = []
        recall_values = []
        ndcg_values = []

        recommended_products: set[int] = set()

        diversity_values = []

        for user_id, user_events in by_user.items():
            unique_products = []

            seen = set()

            for event in user_events:
                product_id = event["product_id"]

                if product_id not in seen:
                    unique_products.append(event)
                    seen.add(product_id)

            if len(unique_products) < 2:
                continue

            train_events = unique_products[:-1]
            test_event = unique_products[-1]

            ground_truth = int(
                test_event["product_id"]
            )

            popularity = build_popularity_scores(
                train_events,
                products,
            )

            content = build_content_scores(
                train_events,
                products,
            )

            collaborative = build_collaborative_scores(
                user_id,
                train_events,
            )

            popularity = filter_seen_products(
                popularity,
                train_events,
            )

            content = filter_seen_products(
                content,
                train_events,
            )

            collaborative = filter_seen_products(
                collaborative,
                train_events,
            )

            combined = hybrid_scores(
                popularity,
                content,
                collaborative,
            )

            recommendations = rank_candidates(
                combined,
                limit=k,
            )

            predicted = [
                item.product_id
                for item in recommendations
            ]

            if not predicted:
                continue

            evaluated_users += 1

            recommended_products.update(predicted)

            hits = (
                1
                if ground_truth in predicted
                else 0
            )

            precision_values.append(
                hits / k
            )

            recall_values.append(
                float(hits)
            )

            relevances = [
                1 if item == ground_truth else 0
                for item in predicted
            ]

            dcg = cls._dcg(relevances)

            ideal = cls._dcg(
                [1]
            )

            ndcg_values.append(
                dcg / ideal
                if ideal
                else 0.0
            )

            product_categories = {
                product.product_id: product.category_id
                for product in products
            }

            categories = [
                product_categories.get(item)
                for item in predicted
            ]

            categories = [
                category
                for category in categories
                if category is not None
            ]

            if categories:
                diversity_values.append(
                    len(set(categories))
                    / len(categories)
                )

        total_products = len(products)

        coverage = (
            len(recommended_products)
            / total_products
            if total_products
            else 0.0
        )

        return {
            "users_evaluated": evaluated_users,
            "k": k,
            "precision_at_k": (
                sum(precision_values)
                / len(precision_values)
                if precision_values
                else 0.0
            ),
            "recall_at_k": (
                sum(recall_values)
                / len(recall_values)
                if recall_values
                else 0.0
            ),
            "ndcg_at_k": (
                sum(ndcg_values)
                / len(ndcg_values)
                if ndcg_values
                else 0.0
            ),
            "coverage": coverage,
            "diversity": (
                sum(diversity_values)
                / len(diversity_values)
                if diversity_values
                else 0.0
            ),
        }