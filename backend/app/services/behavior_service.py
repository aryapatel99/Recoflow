from collections import Counter, defaultdict
from datetime import datetime

from sqlalchemy.orm import Session

from backend.app.repositories.behavior_repository import (
    BehaviorRepository,
)
from backend.app.schemas.behavior import (
    BehaviorEventSummary,
    ProductBehaviorSummary,
    UserBehaviorResponse,
)


EVENT_WEIGHTS: dict[str, float] = {
    "product_view": 1.0,
    "product_click": 2.0,
    "search": 0.5,
    "wishlist_add": 4.0,
    "add_to_cart": 5.0,
    "purchase": 8.0,
    "recommendation_impression": 0.25,
    "recommendation_click": 3.0,
}


class BehaviorService:

    @staticmethod
    def get_user_behavior(
        db: Session,
        user_id: int,
    ) -> UserBehaviorResponse:

        events = BehaviorRepository.get_user_events(
            db,
            user_id,
        )

        event_counter = Counter()
        product_scores: defaultdict[int, float] = defaultdict(float)
        product_counts: defaultdict[int, int] = defaultdict(int)
        product_last_seen: dict[int, datetime] = {}

        for event in events:
            event_type = event.event_type

            event_counter[event_type] += 1

            weight = EVENT_WEIGHTS.get(
                event_type,
                1.0,
            )

            if event.product_id is not None:
                product_id = event.product_id

                product_scores[product_id] += weight
                product_counts[product_id] += 1

                current_time = product_last_seen.get(product_id)

                if (
                    current_time is None
                    or event.occurred_at > current_time
                ):
                    product_last_seen[product_id] = event.occurred_at

        event_breakdown = [
            BehaviorEventSummary(
                event_type=event_type,
                count=count,
                weight=EVENT_WEIGHTS.get(
                    event_type,
                    1.0,
                ),
            )
            for event_type, count in sorted(
                event_counter.items(),
                key=lambda item: (-item[1], item[0]),
            )
        ]

        ranked_products = sorted(
            product_scores.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        top_products = [
            ProductBehaviorSummary(
                product_id=product_id,
                score=score,
                interaction_count=product_counts[product_id],
                last_interaction_at=product_last_seen.get(product_id),
            )
            for product_id, score in ranked_products[:20]
        ]

        unique_products = len(product_scores)

        return UserBehaviorResponse(
            user_id=user_id,
            total_events=len(events),
            unique_products=unique_products,
            event_breakdown=event_breakdown,
            top_products=top_products,
        )