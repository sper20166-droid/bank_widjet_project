"""Модуль для работы с внешним API конвертации валют."""
import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EXCHANGE_API_KEY")
API_URL = "https://api.apilayer.com/exchangerates_data/latest"


def get_transaction_amount(transaction: Dict[str, Any]) -> float:
    """Возвращает сумму транзакции в рублях.

    Если валюта операции — USD или EUR, происходит обращение
    к Exchange Rates Data API для конвертации в рублях.

    Args:
        transaction: словарь с данными о транзакции.

    Returns:
        Сумма транзакции в рублях (float).

    Raises:
        ValueError: если валюта не RUB, USD или EUR.
        KeyError: если в транзакции нет нужных ключей.
    """
    amount = transaction["operationAmount"]["amount"]
    currency = transaction["operationAmount"]["currency"]["code"]
    amount = float(amount)

    if currency == "RUB":
        return amount

    if currency in ("USD", "EUR"):
        response = requests.get(
            API_URL,
            params={"from": currency, "to": "RUB"},
            headers={"apikey": API_KEY or ""},
        )
        response.raise_for_status()
        rate = float(response.json()["rates"]["RUB"])
        return amount * rate
    raise ValueError(f"Неизвестная валюта: {currency}")
