from backend.app.ml.recommender import (
    ProductRecord,
    build_collaborative_scores,
    cosine_similarity,
    hybrid_scores,
    normalize_scores,
    tokenize,
)


def test_tokenize():
    result = tokenize(
        "Wireless Bluetooth Headphones"
    )

    assert result["wireless"] == 1
    assert result["bluetooth"] == 1
    assert result["headphones"] == 1


def test_cosine_similarity_identical():
    a = tokenize("wireless headphones")
    b = tokenize("wireless headphones")

    assert cosine_similarity(a, b) == 1.0


def test_normalize_scores():
    scores = {
        1: 10.0,
        2: 20.0,
        3: 30.0,
    }

    normalized = normalize_scores(scores)

    assert normalized[1] == 0.0
    assert normalized[3] == 1.0


def test_collaborative_filtering():
    events = [
        {
            "user_id": 1,
            "product_id": 10,
            "event_type": "purchase",
        },
        {
            "user_id": 1,
            "product_id": 20,
            "event_type": "product_click",
        },
        {
            "user_id": 2,
            "product_id": 10,
            "event_type": "purchase",
        },
        {
            "user_id": 2,
            "product_id": 30,
            "event_type": "purchase",
        },
    ]

    scores = build_collaborative_scores(
        user_id=1,
        events=events,
    )

    assert 30 in scores


def test_hybrid_scores():
    popularity = {
        1: 10.0,
        2: 20.0,
    }

    content = {
        1: 20.0,
        2: 10.0,
    }

    collaborative = {
        1: 5.0,
        2: 30.0,
    }

    scores = hybrid_scores(
        popularity,
        content,
        collaborative,
    )

    assert set(scores) == {1, 2}
    assert scores[2] > scores[1]