import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1234567812345678", "1234 56** **** 5678"),
    ],
)
def test_get_mask_card_number(card_number: str, expected: str) -> None:
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    "card_number",
    ["", "1234", "123456781234"],
)
def test_get_mask_card_number_invalid(card_number: str) -> None:
    with pytest.raises(Exception):
        get_mask_card_number(card_number)


@pytest.mark.parametrize(
    "account_number, expected",
    [
        ("73654108430135874305", "**4305"),
        ("1234", "**1234"),  # короткий счёт: маскируются последние 4 цифры
    ],
)
def test_get_mask_account(account_number: str, expected: str) -> None:
    assert get_mask_account(account_number) == expected


@pytest.mark.parametrize(
    "account_number",
    ["", "123"],
)
def test_get_mask_account_invalid(account_number: str) -> None:
    with pytest.raises(Exception):
        get_mask_account(account_number)
