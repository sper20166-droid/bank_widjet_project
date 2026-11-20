"""Модуль для считывания финансовых операций из файлов CSV и Excel."""
import logging
import os
from typing import Any, List, cast

import pandas as pd

logger = logging.getLogger("file_reader")
logger.setLevel(logging.DEBUG)

log_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "logs", "file_reader.log"
)
os.makedirs(os.path.dirname(log_path), exist_ok=True)

file_handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_transactions_from_csv(file_path: str) -> List[dict[str, Any]]:
    """Считывает финансовые операции из CSV-файла.

    Args:
        file_path: путь к CSV-файлу с транзакциями.

    Returns:
        Список словарей, где каждый словарь — одна финансовая операция.
    """
    logger.info(f"Считывание транзакций из CSV: {file_path}")
    transactions = pd.read_csv(file_path, sep=";")
    logger.info(f"Считано {len(transactions)} транзакций из CSV")
    return cast(List[dict[str, Any]], transactions.to_dict(orient="records"))


def get_transactions_from_excel(file_path: str) -> List[dict[str, Any]]:
    """Считывает финансовые операции из Excel-файла.

    Args:
        file_path: путь к файлу Excel с транзакциями.

    Returns:
        Список словарей, где каждый словарь — одна финансовая операция.
    """
    logger.info(f"Считывание транзакций из Excel: {file_path}")
    transactions = pd.read_excel(file_path)
    logger.info(f"Считано {len(transactions)} транзакций из Excel")
    return cast(List[dict[str, Any]], transactions.to_dict(orient="records"))
