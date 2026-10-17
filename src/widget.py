import re
from datetime import datetime

from src.masks import get_mask_card_number, get_mask_account


def mask_account_card(card_info: str) -> str:
    """Обрабатывает информацию о картах и счетах.

    'Visa Platinum 7000792289606361' -> 'Visa Platinum 7000 79** **** 6361'
    'Счет 73654108430135874305' -> 'Счет **4305'
    """
    if not isinstance(card_info, str) or not card_info.strip():
        return "Некорректный ввод"

    parts = card_info.strip().split()

    # Название может быть из 1-2 слов + номер, всего 2 или 3 части
    if len(parts) < 2 or len(parts) > 3:
        return "Некорректный ввод"

    number = parts[-1]
    name = " ".join(parts[:-1])
    # В названии карты/счета не может быть цифр: 'Visa 123' — некорректно
    if not re.fullmatch(r"[А-Яа-яЁёA-Za-z -]+", name):
        return "Некорректный ввод"
    if re.fullmatch(r"\d{16}", number):
        return f"{name} {get_mask_card_number(number)}"
    if re.fullmatch(r"\d{20}", number):
        return f"{name} {get_mask_account(number)}"
    return "Некорректный ввод"


def get_date(date_str: str) -> str:
    """Преобразует ISO-дату в формат ДД.ММ.ГГГГ.

    '2024-03-11T02:26:18.671407' -> '11.03.2024'
    """
    if not isinstance(date_str, str):
        return "Некорректный ввод"
    try:
        dt = datetime.fromisoformat(date_str)
        return dt.strftime("%d.%m.%Y")
    except ValueError:
        return "Некорректный ввод"
