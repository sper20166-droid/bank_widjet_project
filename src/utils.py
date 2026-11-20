import json
import logging
import os
from typing import Any, List

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

log_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "logs", "utils.log"
)
os.makedirs(os.path.dirname(log_path), exist_ok=True)

file_handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

"""Модуль с утилитами для работы с файлами транзакций."""


def get_transactions_data(path: str) -> List[Any]:
    """Читает JSON-файл и возвращает список словарей с транзакциями.

    Args:
        path: путь к JSON-файлу с данными о транзакциях.

    Returns:
        Список словарей с транзакциями. Если файл не найден, пустой
        или содержит не список — возвращает [].
    """
    if not os.path.exists(path):
        logger.error(f"Файл по пути {path} не найден")
        return []

    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError) as e:
        logger.error(f"Ошибка при чтении файла {path}: {e}")
        return []

    if not isinstance(data, list):
        logger.error("Данные не являются списком")
        return []

    logger.info(f"Файл {path} успешно прочитан")
    return data
