"""Модуль с генераторами для обработки транзакций.

Содержит функции:
- filter_by_currency — фильтрация транзакций по валюте;
- transaction_descriptions — выдача описаний операций;
- card_number_generator — генерация номеров карт в формате XXXX XXXX XXXX XXXX.
"""

from typing import Any, Iterator


def filter_by_currency(transactions: list[dict[str, Any]], currency_code: str) -> Iterator[dict[str, Any]]:
    """Фильтрует транзакции по коду валюты.

    Args:
        transactions: Список словарей с данными о транзакциях.
        currency_code: Код валюты для фильтрации, например 'USD'.

    Yields:
        Транзакции, у которых валюта совпадает с заданной.
    """
    for transaction in transactions:
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency_code:
            yield transaction


def transaction_descriptions(transactions: list[dict[str, Any]]) -> Iterator[str]:
    """Генерирует описания операций по очереди.

    Args:
        transactions: Список словарей с данными о транзакциях.

    Yields:
        Описание каждой транзакции.
    """
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """Генерирует номера банковских карт в заданном диапазоне.

    Номера выдаются в формате 'XXXX XXXX XXXX XXXX'.

    Args:
        start: Начальное значение диапазона (включительно).
        stop: Конечное значение диапазона (включительно).

    Yields:
        Отформатированный номер карты.
    """
    for number in range(start, stop + 1):
        card_number = f"{number:016d}"
        formatted = " ".join(card_number[i:i+4] for i in range(0, 16, 4))
        yield formatted
