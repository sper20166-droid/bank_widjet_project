"""Тесты для модуля masks."""

import pytest

from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number() -> None:
    assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"


def test_get_mask_account() -> None:
    assert get_mask_account("73654108430135874305") == "**4305"


def test_get_mask_card_number_invalid_length() -> None:
    with pytest.raises(ValueError):
        get_mask_card_number("123")


def test_get_mask_account_invalid_length() -> None:
    with pytest.raises(ValueError):
        get_mask_account("123")
