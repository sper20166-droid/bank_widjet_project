"""Тесты для подсчёта операций по категориям."""
from src.categories import process_bank_operations

operations = [
    {"description": "Перевод организации"},
    {"description": "Открытие вклада"},
    {"description": "Перевод организации"},
]


def test_counts_correctly() -> None:
    result = process_bank_operations(operations, ["Перевод организации", "Открытие вклада"])
    assert result == {"Перевод организации": 2, "Открытие вклада": 1}


def test_missing_category() -> None:
    result = process_bank_operations(operations, ["Ипотека"])
    assert "Ипотека" not in result or result["Ипотека"] == 0


def test_empty_data() -> None:
    assert process_bank_operations([], ["Перевод"]) == {} or process_bank_operations([], ["Перевод"]) == {"Перевод": 0}
