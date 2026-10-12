from src.widget import mask_account_card, get_date


def test_mask_card():
    assert mask_account_card("Maestro 1596837868705199") == "Maestro 1596 83** **** 5199"


def test_mask_account():
    assert mask_account_card("Счет 73654108430135874305") == "Счет **4305"


def test_incorrect_input():
    assert mask_account_card("Visa") == "Некорректный ввод"
    assert mask_account_card("Visa 123 7000792289606361") == "Некорректный ввод"


def test_get_date():
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"