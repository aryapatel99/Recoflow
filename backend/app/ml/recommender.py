from __future__ import annotations

import math
from collections import Counter, defaultdict
from dataclasses import dataclass


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


@dataclass
class ProductRecord:
    product_id: int
    external_id: str
    title: str
    description: str | None
    brand: str | None
    category_id: int | None
    price: float
    rating: float
    review_count: int
    features: dict | None = None


@dataclass
class RecommendationCandidate:
    product_id: int
    score: float
    strategy: str


def event_weight(event_type: str) -> float:
    return EVENT_WEIGHTS.get(event_type, 1.0)


def normalize_scores(
    scores: dict[int, float],
) -> dict[int, float]:
    if not scores:
        return {}

    values = list(scores.values())

    minimum = min(values)
    maximum = max(values)

    if math.isclose(minimum, maximum):
        return {
            product_id: 1.0
            for product_id in scores
        }

    denominator = maximum - minimum

    return {
        product_id: (
            (score - minimum) / denominator
        )
        for product_id, score in scores.items()
    }


def cosine_similarity(
    vector_a: Counter[str],
    vector_b: Counter[str],
) -> float:
    """
    Calculate cosine similarity between two sparse vectors.

    Returns:
        0.0 when either vector is empty.
        A value between 0.0 and 1.0 otherwise.
    """

    if not vector_a or not vector_b:
        return 0.0

    common = set(vector_a).intersection(vector_b)

    dot_product = sum(
        vector_a[key] * vector_b[key]
        for key in common
    )

    magnitude_a = math.sqrt(
        sum(
            value * value
            for value in vector_a.values()
        )
    )

    magnitude_b = math.sqrt(
        sum(
            value * value
            for value in vector_b.values()
        )
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    score = dot_product / (
        magnitude_a * magnitude_b
    )

    # Remove tiny floating-point errors such as:
    # 0.9999999999999998 -> 1.0
    score = round(score, 12)

    # Protect against tiny numerical values outside
    # the mathematical [0, 1] range.
    return max(
        0.0,
        min(1.0, score),
    )


def tokenize(text: str) -> Counter[str]:
    tokens = [
        token.lower()
        for token in text.split()
        if len(token) > 1
    ]

    return Counter(tokens)


def product_text(
    product: ProductRecord,
) -> str:
    parts = [
        product.title or "",
        product.description or "",
        product.brand or "",
    ]

    if product.features:
        parts.extend(
            str(value)
            for value in product.features.values()
        )

    return " ".join(parts)


def build_popularity_scores(
    events: list[dict],
    products: list[ProductRecord],
) -> dict[int, float]:
    counts: Counter[int] = Counter()

    for event in events:
        product_id = event.get("product_id")

        if product_id is None:
            continue

        counts[int(product_id)] += event_weight(
            event.get("event_type", "")
        )

    scores: dict[int, float] = {}

    for product in products:
        interaction_score = counts.get(
            product.product_id,
            0.0,
        )

        score = (
            math.log1p(interaction_score)
            + 0.15 * float(
                product.rating or 0.0
            )
            + 0.02 * math.log1p(
                float(
                    product.review_count or 0
                )
            )
        )

        scores[product.product_id] = score

    return scores


def build_user_profile(
    events: list[dict],
    products_by_id: dict[int, ProductRecord],
) -> Counter[str]:
    profile: Counter[str] = Counter()

    for event in events:
        product_id = event.get("product_id")

        if product_id is None:
            continue

        product = products_by_id.get(
            int(product_id)
        )

        if not product:
            continue

        weight = event_weight(
            event.get("event_type", "")
        )

        tokens = tokenize(
            product_text(product)
        )

        for token, value in tokens.items():
            profile[token] += (
                value * weight
            )

    return profile


def build_content_scores(
    user_events: list[dict],
    products: list[ProductRecord],
) -> dict[int, float]:
    products_by_id = {
        product.product_id: product
        for product in products
    }

    profile = build_user_profile(
        user_events,
        products_by_id,
    )

    if not profile:
        return {
            product.product_id: 0.0
            for product in products
        }

    scores: dict[int, float] = {}

    for product in products:
        product_vector = tokenize(
            product_text(product)
        )

        scores[product.product_id] = (
            cosine_similarity(
                profile,
                product_vector,
            )
        )

    return scores


def build_collaborative_scores(
    user_id: int,
    events: list[dict],
) -> dict[int, float]:
    """
    Item-based collaborative filtering.

    Builds:

        user -> products

    and:

        product -> users

    Then calculates product-to-product similarity
    through shared users.

    This is intentionally lightweight and suitable
    for the RecoFlow V1 implementation.
    """

    user_products: dict[
        int,
        Counter[int],
    ] = defaultdict(Counter)

    for event in events:
        uid = event.get("user_id")
        product_id = event.get("product_id")

        if uid is None or product_id is None:
            continue

        uid = int(uid)
        product_id = int(product_id)

        user_products[uid][product_id] += (
            event_weight(
                event.get(
                    "event_type",
                    "",
                )
            )
        )

    target_products = user_products.get(
        int(user_id),
        Counter(),
    )

    if not target_products:
        return {}

    product_users: dict[
        int,
        dict[int, float],
    ] = defaultdict(dict)

    for uid, products_for_user in (
        user_products.items()
    ):
        for product_id, weight in (
            products_for_user.items()
        ):
            product_users[product_id][uid] = (
                weight
            )

    scores: dict[int, float] = Counter()

    for (
        source_product,
        source_weight,
    ) in target_products.items():

        source_users = product_users.get(
            source_product,
            {},
        )

        source_norm = math.sqrt(
            sum(
                value * value
                for value in source_users.values()
            )
        )

        if source_norm == 0:
            continue

        for (
            candidate_product,
            candidate_users,
        ) in product_users.items():

            if candidate_product == source_product:
                continue

            common_users = (
                set(source_users)
                .intersection(
                    candidate_users
                )
            )

            if not common_users:
                continue

            dot = sum(
                source_users[uid]
                * candidate_users[uid]
                for uid in common_users
            )

            candidate_norm = math.sqrt(
                sum(
                    value * value
                    for value in candidate_users.values()
                )
            )

            if candidate_norm == 0:
                continue

            similarity = dot / (
                source_norm
                * candidate_norm
            )

            similarity = max(
                0.0,
                min(
                    1.0,
                    round(
                        similarity,
                        12,
                    ),
                ),
            )

            scores[candidate_product] += (
                similarity * source_weight
            )

    return dict(scores)


def filter_seen_products(
    scores: dict[int, float],
    user_events: list[dict],
) -> dict[int, float]:
    seen = {
        int(event["product_id"])
        for event in user_events
        if event.get("product_id")
        is not None
    }

    return {
        product_id: score
        for product_id, score in scores.items()
        if product_id not in seen
    }


def hybrid_scores(
    popularity_scores: dict[int, float],
    content_scores: dict[int, float],
    collaborative_scores: dict[int, float],
) -> dict[int, float]:

    normalized_popularity = normalize_scores(
        popularity_scores
    )

    normalized_content = normalize_scores(
        content_scores
    )

    normalized_collaborative = normalize_scores(
        collaborative_scores
    )

    product_ids = (
        set(normalized_popularity)
        | set(normalized_content)
        | set(normalized_collaborative)
    )

    scores: dict[int, float] = {}

    for product_id in product_ids:
        popularity = (
            normalized_popularity.get(
                product_id,
                0.0,
            )
        )

        content = (
            normalized_content.get(
                product_id,
                0.0,
            )
        )

        collaborative = (
            normalized_collaborative.get(
                product_id,
                0.0,
            )
        )

        scores[product_id] = (
            0.30 * popularity
            + 0.30 * content
            + 0.40 * collaborative
        )

    return scores


def rank_candidates(
    scores: dict[int, float],
    limit: int = 10,
) -> list[RecommendationCandidate]:

    ranked = sorted(
        scores.items(),
        key=lambda item: (
            -item[1],
            item[0],
        ),
    )

    return [
        RecommendationCandidate(
            product_id=product_id,
            score=float(score),
            strategy="hybrid",
        )
        for product_id, score in ranked[:limit]
    ]