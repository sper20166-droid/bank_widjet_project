"""Модуль для подсчёта операций по категориям."""
from collections import Counter


def process_bank_operations(data: list[dict], categories: list[str]) -> dict:
    """Считает количество операций по каждой категории из списка.

    Args:
        data: список словарей с данными о банковских операциях.
        categories: список категорий для подсчёта.

    Returns:
        Словарь: ключ — название категории, значение — количество операций.
    """
    counter: Counter[str] = Counter()
    for transaction in data:
        description = transaction.get("description", "")
        if description in categories:
            counter[description] += 1
    return dict(counter)
