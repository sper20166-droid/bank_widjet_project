import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "info, expected",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ],
)
def test_mask_account_card(info: str, expected: str) -> None:
    assert mask_account_card(info) == expected


@pytest.mark.parametrize(
    "info",
    ["", "Visa Platinum", "Счёт 12", "Visa 123", "Visa Platinum 12345"],
)
def test_mask_account_card_invalid(info: str) -> None:
    assert mask_account_card(info) == "Некорректный ввод"


@pytest.mark.parametrize(
    "date_str, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2024-03-11", "11.03.2024"),  # дата без времени — fromisoformat это умеет
    ],
)
def test_get_date(date_str: str, expected: str) -> None:
    assert get_date(date_str) == expected


@pytest.mark.parametrize(
    "date_str",
    ["", "not a date"],
)
def test_get_date_invalid(date_str: str) -> None:
    assert get_date(date_str) == "Некорректный ввод"


def test_get_date_not_string() -> None:
    assert get_date(20240311) == "Некорректный ввод"


@pytest.mark.parametrize(
    "info",
    [
        "Visa 12 7000792289606361",  # цифры в названии
        "Visa Gold Platinum 7000792289606361",  # слишком много слов
    ],
)
def test_mask_account_card_extra_invalid(info: str) -> None:
    assert mask_account_card(info) == "Некорректный ввод"
