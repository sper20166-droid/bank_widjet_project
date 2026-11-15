"""Тесты для модуля generators."""

from typing import Any

import pytest

from generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def transactions() -> list[dict[str, Any]]:
    """Возвращает список тестовых транзакций."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
    ]


class TestFilterByCurrency:
    """Тесты функции filter_by_currency."""

    def test_returns_iterator(self, transactions: list[dict[str, Any]]) -> None:
        """Функция возвращает итератор."""
        result = filter_by_currency(transactions, "USD")
        assert iter(result) is not None
        assert list(result) == list(filter_by_currency(transactions, "USD"))

    def test_filters_by_currency(self, transactions: list[dict[str, Any]]) -> None:
        """Функция отбирает только транзакции в заданной валюте."""
        result = list(filter_by_currency(transactions, "USD"))
        assert len(result) == 2
        assert all(t["operationAmount"]["currency"]["code"] == "USD" for t in result)
        assert result[0]["id"] == 939719570
        assert result[1]["id"] == 142264268

    def test_next_yields_sequentially(self, transactions: list[dict[str, Any]]) -> None:
        """Генератор выдает транзакции по одной."""
        usd_transactions = filter_by_currency(transactions, "RUB")
        first = next(usd_transactions)
        assert first["id"] == 873106923
        with pytest.raises(StopIteration):
            next(usd_transactions)

    def test_no_matching_currency(self, transactions: list[dict[str, Any]]) -> None:
        """Отсутствие транзакций в заданной валюте даёт пустой результат без ошибок."""
        assert list(filter_by_currency(transactions, "EUR")) == []

    @pytest.mark.parametrize(
        "input_data",
        [
            [],
            [{"id": 1, "description": "Без валюты"}],
        ],
    )
    def test_empty_or_incomplete_data(self, input_data: list[dict[str, Any]]) -> None:
        """Пустой список и словарь без полей валюты обрабатываются без ошибок."""
        assert list(filter_by_currency(input_data, "USD")) == []


class TestTransactionDescriptions:
    """Тесты функции-генератора transaction_descriptions."""

    def test_descriptions_in_order(self, transactions: list[dict[str, Any]]) -> None:
        """Описания выдаются в порядке следования транзакций."""
        descriptions = transaction_descriptions(transactions)
        assert next(descriptions) == "Перевод организации"
        assert next(descriptions) == "Перевод со счета на счет"
        assert next(descriptions) == "Перевод со счета на счет"

    def test_exhausts_after_all_items(self, transactions: list[dict[str, Any]]) -> None:
        """После перебора всех описаний генератор завершается StopIteration."""
        descriptions = transaction_descriptions(transactions)
        for _ in range(len(transactions)):
            next(descriptions)
        with pytest.raises(StopIteration):
            next(descriptions)

    @pytest.mark.parametrize(
        "input_data, expected",
        [
            ([], []),
            ([{"description": "Перевод с карты на карту"}], ["Перевод с карты на карту"]),
            (
                [{"description": "A"}, {"description": "B"}, {"description": "C"}],
                ["A", "B", "C"],
            ),
            ([{"id": 1}], [""]),  # описание отсутствует — выдаётся пустая строка
        ],
    )
    def test_different_inputs(self, input_data: list[dict[str, Any]], expected: list[str]) -> None:
        """Функция корректно работает с разным числом транзакций."""
        assert list(transaction_descriptions(input_data)) == expected


class TestCardNumberGenerator:
    """Тесты генератора card_number_generator."""

    def test_basic_range(self) -> None:
        """Генератор выдает номера в заданном диапазоне."""
        result = list(card_number_generator(1, 5))
        assert result == [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
            "0000 0000 0000 0004",
            "0000 0000 0000 0005",
        ]

    def test_is_generator(self) -> None:
        """Функция возвращает генератор."""
        result = card_number_generator(1, 3)
        assert next(result) == "0000 0000 0000 0001"

    def test_boundary_values(self) -> None:
        """Генератор корректно обрабатывает крайние значения диапазона."""
        assert next(card_number_generator(1, 1)) == "0000 0000 0000 0001"
        assert list(card_number_generator(9999999999999998, 9999999999999999)) == [
            "9999 9999 9999 9998",
            "9999 9999 9999 9999",
        ]

    def test_empty_range(self) -> None:
        """При start > stop генератор не выдает значений и не падает."""
        assert list(card_number_generator(5, 1)) == []

    @pytest.mark.parametrize(
        "start, stop, first, last",
        [
            (1, 5, "0000 0000 0000 0001", "0000 0000 0000 0005"),
            (16, 17, "0000 0000 0000 0016", "0000 0000 0000 0017"),
            (1000, 1001, "0000 0000 0000 1000", "0000 0000 0000 1001"),
        ],
    )
    def test_formatting(self, start: int, stop: int, first: str, last: str) -> None:
        """Номера карт форматируются группами по 4 цифры через пробел."""
        numbers = list(card_number_generator(start, stop))
        assert numbers[0] == first
        assert numbers[-1] == last
        for number in numbers:
            parts = number.split(" ")
            assert len(parts) == 4
            assert all(len(part) == 4 and part.isdigit() for part in parts)
