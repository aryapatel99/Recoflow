from backend.app.services.evaluation_service import EvaluationService


def test_dcg():
    result = EvaluationService._dcg([1, 0, 0])

    assert result == 1.0


def test_dcg_multiple_hits():
    result = EvaluationService._dcg([1, 1])

    assert result > 1.0