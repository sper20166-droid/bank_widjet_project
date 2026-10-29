import pytest


@pytest.fixture
def sample_transactions() -> list[dict]:
    """Список словарей с транзакциями для тестов processing."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-03-11T02:26:18.671407"},
        {"id": 2, "state": "CANCELED", "date": "2023-10-01T10:00:00.000000"},
        {"id": 3, "state": "EXECUTED", "date": "2024-06-20T12:30:00.000000"},
        {"id": 4, "state": "PENDING", "date": "2024-01-15T08:45:00.000000"},
        {"id": 5, "state": "EXECUTED", "date": "2024-03-11T02:26:18.671407"},
    ]


@pytest.fixture
def empty_transactions() -> list[dict]:
    return []

    """Пустой список транзакций."""
