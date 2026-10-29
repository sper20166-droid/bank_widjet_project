from typing import Any


def filter_by_state(
    transactions: list[dict[str, Any]], state: str = "EXECUTED"
) -> list[dict[str, Any]]:
    """Фильтрует список транзакций по статусу state."""
    result: list[dict[str, Any]] = []
    for transaction in transactions:
        if transaction.get("state") == state:
            result.append(transaction)
    return result


def sort_by_date(
    transactions: list[dict[str, Any]], reverse: bool = True
) -> list[dict[str, Any]]:
    """Сортирует транзакции по дате (по умолчанию — новые сверху)."""
    return sorted(transactions, key=lambda x: x.get("date", ""), reverse=reverse)
