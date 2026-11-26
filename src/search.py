"""Модуль для поиска транзакций по строке в описании."""
import re


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """Ищет транзакции, у которых в описании есть заданная строка.

    Args:
        data: список словарей с данными о банковских операциях.
        search: строка для поиска в описании.

    Returns:
        Список словарей с операциями, где описание содержит строку поиска.
    """
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    result: list[dict] = []
    for transaction in data:
        description = transaction.get("description", "")
        if description and pattern.search(description):
            result.append(transaction)
    return result
