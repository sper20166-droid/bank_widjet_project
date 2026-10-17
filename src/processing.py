"""Модуль с функциями обработки данных о банковских операциях."""

from typing import Any


def filter_by_state(
    list_of_dicts: list[dict[str, Any]],
    state: str = "EXECUTED",
) -> list[dict[str, Any]]:
    """Фильтрует список словарей по значению ключа state.

    Args:
        list_of_dicts: Список словарей с данными о банковских операциях.
        state: Значение ключа state для фильтрации. По умолчанию 'EXECUTED'.

    Returns:
        Новый список словарей, у которых ключ state равен переданному значению.

    """
    return [item for item in list_of_dicts if item.get("state") == state]


def sort_by_date(
    list_of_dicts: list[dict[str, Any]],
    reverse: bool = True,
) -> list[dict[str, Any]]:
    """Сортирует список словарей по дате операции.

    Args:
        list_of_dicts: Список словарей с данными о банковских операциях.
        reverse: Порядок сортировки. True — по убыванию (сначала новые),
                 False — по возрастанию. По умолчанию True.

    Returns:
        Новый список словарей, отсортированный по ключу date.

    """
    return sorted(
        list_of_dicts,
        key=lambda item: item["date"],
        reverse=reverse,
    )
