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
    к Exchange Rates Data API для конвертации в рубли.

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
            params={"base": currency, "symbols": "RUB"},
            headers={"apikey": API_KEY},
        )
        response.raise_for_status()
        rate = response.json()["rates"]["RUB"]
        return round(amount * rate, 2)

    raise ValueError(f"Неизвестная валюта: {currency}")
