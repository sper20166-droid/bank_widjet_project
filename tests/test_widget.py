"""Тесты для функций виджета: маскировка карт и счетов, форматирование даты."""
from src.widget import get_date, mask_account_card


def test_mask_card() -> None:
    """Маскировка номера карты."""
    assert mask_account_card("Maestro 1596837868705199") == (
        "Maestro 1596 83** **** 5199"
    )


def test_mask_account() -> None:
    """Маскировка номера счёта."""
    assert mask_account_card("Счет 73654108430135874305") == "Счет **4305"


def test_incorrect_input() -> None:
    """Некорректный ввод обрабатывается без ошибки."""
    assert mask_account_card("Visa") == "Некорректный ввод"
    assert mask_account_card("Visa 123 7000792289606361") == (
        "Некорректный ввод"
    )


def test_get_date() -> None:
    """Дата преобразуется в формат ДД.ММ.ГГГГ."""
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"
