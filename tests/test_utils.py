"""Тесты для функции чтения JSON-файла."""
import json
from unittest.mock import mock_open, patch

from src.utils import get_transactions_data


def test_read_valid_file() -> None:
    """Файл с корректным JSON возвращает список словарей."""
    data = [{"id": 1, "amount": "100"}]
    with patch("builtins.open", mock_open(read_data=json.dumps(data))):
        result = get_transactions_data("data/operations.json")
    assert result == data


def test_file_not_found() -> None:
    """Несуществующий файл возвращает пустой список."""
    assert get_transactions_data("no_such_file.json") == []


def test_invalid_json() -> None:
    """Битый JSON возвращает пустой список."""
    with patch("builtins.open", mock_open(read_data="{not json")):
        result = get_transactions_data("data/operations.json")
    assert result == []


def test_not_a_list() -> None:
    """JSON без списка (например, словарь) возвращает пустой список."""
    with patch("builtins.open", mock_open(read_data=json.dumps({"key": 1}))):
        result = get_transactions_data("data/operations.json")
    assert result == []


def test_empty_file() -> None:
    """Пустой файл возвращает пустой список."""
    with patch("builtins.open", mock_open(read_data="")):
        result = get_transactions_data("data/operations.json")
    assert result == []
