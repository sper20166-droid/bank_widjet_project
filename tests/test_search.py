"""Тесты для функции поиска по описанию."""
from src.search import process_bank_search

operations = [
    {"description": "Перевод организации", "amount": 100},
    {"description": "Открытие вклада", "amount": 200},
    {"description": "Перевод с карты на карту", "amount": 300},
    {"amount": 400},
]


def test_search_finds_matches() -> None:
    result = process_bank_search(operations, "перевод")
    assert len(result) == 2


def test_search_case_insensitive() -> None:
    result = process_bank_search(operations, "ПЕРЕВОД")
    assert len(result) == 2


def test_search_no_results() -> None:
    assert process_bank_search(operations, "ипотека") == []


def test_search_empty_string() -> None:
    result = process_bank_search(operations, "")
    assert len(result) == 3


def test_search_special_chars() -> None:
    assert process_bank_search(operations, "100%") == []
