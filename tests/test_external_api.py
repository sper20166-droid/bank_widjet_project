"""Тесты для функции конвертации валют."""
from unittest.mock import MagicMock, patch

import pytest
from requests.exceptions import HTTPError

from src.external_api import get_transaction_amount


def get_transaction(currency_code: str) -> dict:
    """Вспомогательная функция: создаёт тестовую транзакцию."""
    return {
        "operationAmount": {
            "amount": "100",
            "currency": {"code": currency_code},
        }
    }


def test_rub_transaction() -> None:
    """Транзакция в рублях возвращается без обращения к API."""
    assert get_transaction_amount(get_transaction("RUB")) == 100.0


@patch("src.external_api.requests.get")
def test_usd_transaction(mock_get: MagicMock) -> None:
    """Для USD сумма конвертируется по курсу из API."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"rates": {"RUB": 90.0}}
    mock_get.return_value = mock_response

    result = get_transaction_amount(get_transaction("USD"))

    mock_get.assert_called_once()
    assert result == 9000.0


@patch("src.external_api.requests.get")
def test_eur_transaction(mock_get: MagicMock) -> None:
    """Для EUR сумма конвертируется по курсу из API."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"rates": {"RUB": 100.0}}
    mock_get.return_value = mock_response

    result = get_transaction_amount(get_transaction("EUR"))

    assert result == 10000.0


def test_unknown_currency() -> None:
    """Неизвестная валюта вызывает ValueError."""
    with pytest.raises(ValueError):
        get_transaction_amount(get_transaction("GBP"))


@patch("src.external_api.requests.get")
def test_api_error(mock_get: MagicMock) -> None:
    """Ошибка API (статус 500) вызывает HTTPError."""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPError("Server error")
    mock_get.return_value = mock_response

    with pytest.raises(HTTPError):
        get_transaction_amount(get_transaction("USD"))
