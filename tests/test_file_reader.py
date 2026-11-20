"""Тесты для модуля file_reader: функции чтения CSV и Excel."""
from unittest.mock import MagicMock, patch

import pandas as pd

from src.file_reader import get_transactions_from_csv, get_transactions_from_excel


@patch("src.file_reader.pd.read_csv")
def test_get_transactions_from_csv(mock_read_csv: MagicMock) -> None:
    """Тест: функция возвращает список словарей из CSV."""
    mock_read_csv.return_value = pd.DataFrame(
        [{"id": 1, "amount": "100.0", "description": "Перевод"}]
    )
    result = get_transactions_from_csv("fake_path.csv")

    mock_read_csv.assert_called_once_with("fake_path.csv", sep=";")
    assert isinstance(result, list)
    assert result == [{"id": 1, "amount": "100.0", "description": "Перевод"}]


@patch("src.file_reader.pd.read_excel")
def test_get_transactions_from_excel(mock_read_excel: MagicMock) -> None:
    """Тест: функция возвращает список словарей из Excel."""
    mock_read_excel.return_value = pd.DataFrame(
        [{"id": 2, "amount": "250.0", "description": "Оплата"}]
    )
    result = get_transactions_from_excel("fake_path.xlsx")

    mock_read_excel.assert_called_once_with("fake_path.xlsx")
    assert isinstance(result, list)
    assert result == [{"id": 2, "amount": "250.0", "description": "Оплата"}]
