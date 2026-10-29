import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [1, 3, 5]),
        ("CANCELED", [2]),
        ("PENDING", [4]),
    ],
)
def test_filter_by_state(sample_transactions: list, state: str, expected_ids: list) -> None:
    result = filter_by_state(sample_transactions, state=state)
    assert [item["id"] for item in result] == expected_ids


def test_filter_by_state_empty(empty_transactions: list) -> None:
    """Пустой список на входе — пустой список на выходе."""
    assert filter_by_state(empty_transactions) == []


def test_filter_by_state_not_found(sample_transactions: list) -> None:
    """Такого статуса нет ни у одной транзакции."""
    assert filter_by_state(sample_transactions, state="UNKNOWN") == []


@pytest.mark.parametrize("reverse, expected_ids", [(False, [2, 4, 1, 5, 3]), (True, [3, 1, 5, 4, 2])])
def test_sort_by_date(sample_transactions: list, reverse: bool, expected_ids: list) -> None:
    result = sort_by_date(sample_transactions, reverse=reverse)
    assert [item["id"] for item in result] == expected_ids


def test_sort_by_date_same_dates(sample_transactions: list) -> None:
    """Транзакции 1 и 5 с одинаковой датой — порядок между ними не важен, важна стабильность."""
    result = sort_by_date(sample_transactions, reverse=True)
    dates = [item["date"] for item in result]
    assert dates == sorted(dates, reverse=True)
