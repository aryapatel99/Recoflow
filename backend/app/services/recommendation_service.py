import math
import re
from collections import Counter, defaultdict
from typing import Any

from sqlalchemy.orm import Session

from backend.app.repositories.behavior_repository import (
    BehaviorRepository,
)
from backend.app.repositories.recommendation_repository import (
    RecommendationRepository,
)
from backend.app.schemas.recommendation import (
    RecommendedProduct,
    RecommendationResponse,
)


EVENT_WEIGHTS = {
    "product_view": 1.0,
    "product_click": 2.0,
    "wishlist_add": 4.0,
    "add_to_cart": 5.0,
    "purchase": 8.0,
    "recommendation_click": 3.0,
    "recommendation_impression": 0.25,
    "search": 0.5,
}


class RecommendationService:

    @staticmethod
    def _tokenize(value: Any) -> list[str]:
        if value is None:
            return []

        if isinstance(value, list):
            value = " ".join(
                str(item)
                for item in value
            )

        if isinstance(value, dict):
            value = " ".join(
                f"{key} {val}"
                for key, val in value.items()
            )

        text = str(value).lower()

        return re.findall(
            r"[a-z0-9]+",
            text,
        )

    @staticmethod
    def _product_text(product) -> list[str]:
        tokens = []

        tokens.extend(
            RecommendationService._tokenize(
                product.title
            )
        )

        tokens.extend(
            RecommendationService._tokenize(
                product.description
            )
        )

        tokens.extend(
            RecommendationService._tokenize(
                product.brand
            )
        )

        tokens.extend(
            RecommendationService._tokenize(
                product.features
            )
        )

        return tokens

    @staticmethod
    def _cosine_similarity(
        left: Counter,
        right: Counter,
    ) -> float:

        if not left or not right:
            return 0.0

        common = set(left) & set(right)

        dot_product = sum(
            left[token] * right[token]
            for token in common
        )

        left_norm = math.sqrt(
            sum(
                value * value
                for value in left.values()
            )
        )

        right_norm = math.sqrt(
            sum(
                value * value
                for value in right.values()
            )
        )

        if left_norm == 0 or right_norm == 0:
            return 0.0

        return dot_product / (
            left_norm * right_norm
        )

    @staticmethod
    def _to_response_item(
        product,
        score: float,
        strategy: str,
    ) -> RecommendedProduct:

        return RecommendedProduct(
            product_id=product.id,
            external_id=product.external_id,
            title=product.title,
            score=round(float(score), 6),
            strategy=strategy,
        )

    @staticmethod
    def popular(
        db: Session,
        user_id: int,
        limit: int = 10,
    ) -> RecommendationResponse:

        products = (
            RecommendationRepository.get_active_products(
                db
            )
        )

        event_counts = (
            RecommendationRepository.get_global_event_counts(
                db
            )
        )

        user_events = (
            RecommendationRepository.get_user_events(
                db,
                user_id,
            )
        )

        seen_products = {
            event.product_id
            for event in user_events
            if event.product_id is not None
        }

        ranked = []

        for product in products:
            if product.id in seen_products:
                continue

            interaction_count = event_counts.get(
                product.id,
                0,
            )

            rating = (
                float(product.rating)
                if product.rating is not None
                else 0.0
            )

            review_count = (
                product.review_count or 0
            )

            score = (
                math.log1p(interaction_count)
                + 0.15 * rating
                + 0.02 * math.log1p(review_count)
            )

            ranked.append(
                (
                    product,
                    score,
                )
            )

        ranked.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        items = [
            RecommendationService._to_response_item(
                product,
                score,
                "popularity",
            )
            for product, score in ranked[:limit]
        ]

        return RecommendationResponse(
            user_id=user_id,
            strategy="popularity",
            count=len(items),
            items=items,
        )

    @staticmethod
    def content_based(
        db: Session,
        user_id: int,
        limit: int = 10,
    ) -> RecommendationResponse:

        products = (
            RecommendationRepository.get_active_products(
                db
            )
        )

        events = (
            BehaviorRepository.get_user_events(
                db,
                user_id,
            )
        )

        product_by_id = {
            product.id: product
            for product in products
        }

        seen_products = {
            event.product_id
            for event in events
            if event.product_id is not None
        }

        profile = Counter()

        for event in events:
            product_id = event.product_id

            if product_id is None:
                continue

            product = product_by_id.get(product_id)

            if product is None:
                continue

            weight = EVENT_WEIGHTS.get(
                event.event_type,
                1.0,
            )

            for token in RecommendationService._product_text(
                product
            ):
                profile[token] += weight

        if not profile:
            return RecommendationService.popular(
                db,
                user_id,
                limit,
            )

        ranked = []

        for product in products:
            if product.id in seen_products:
                continue

            product_tokens = Counter(
                RecommendationService._product_text(
                    product
                )
            )

            similarity = (
                RecommendationService._cosine_similarity(
                    profile,
                    product_tokens,
                )
            )

            if similarity <= 0:
                continue

            ranked.append(
                (
                    product,
                    similarity,
                )
            )

        ranked.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        items = [
            RecommendationService._to_response_item(
                product,
                score,
                "content_based",
            )
            for product, score in ranked[:limit]
        ]

        if not items:
            return RecommendationService.popular(
                db,
                user_id,
                limit,
            )

        return RecommendationResponse(
            user_id=user_id,
            strategy="content_based",
            count=len(items),
            items=items,
        )