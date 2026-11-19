"""Модуль с утилитами для работы с файлами транзакций."""
import json
import os
from typing import Any, List


def get_transactions_data(path: str) -> List[Any]:
    """Читает JSON-файл и возвращает список словарей с транзакциями.

    Args:
        path: путь к JSON-файлу с данными о транзакциях.

    Returns:
        Список словарей с транзакциями.
        Если файл не найден, пустой или содержит не список — возвращает [].
    """
    if not os.path.exists(path):
        return []

    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        return []

    if not isinstance(data, list):
        return []
    return data
