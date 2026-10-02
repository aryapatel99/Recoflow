from collections import Counter

from backend.app.services.recommendation_service import (
    RecommendationService,
)


def test_tokenizer():
    tokens = RecommendationService._tokenize(
        "Sony Wireless Headphones"
    )

    assert "sony" in tokens
    assert "wireless" in tokens
    assert "headphones" in tokens


def test_cosine_similarity_identical_vectors():
    left = Counter(
        {
            "wireless": 2,
            "headphones": 3,
        }
    )

    right = Counter(
        {
            "wireless": 2,
            "headphones": 3,
        }
    )

    score = RecommendationService._cosine_similarity(
        left,
        right,
    )

    assert abs(score - 1.0) < 1e-9


def test_cosine_similarity_unrelated_vectors():
    left = Counter(
        {
            "camera": 2,
        }
    )

    right = Counter(
        {
            "headphones": 3,
        }
    )

    score = RecommendationService._cosine_similarity(
        left,
        right,
    )

    assert score == 0.0


def test_empty_vector_similarity():
    score = RecommendationService._cosine_similarity(
        Counter(),
        Counter({"test": 1}),
    )

    assert score == 0.0