import logging
import os

logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

log_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "logs", "masks.log"
)
file_handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

"""Функции маскировки номеров банковских карт и счетов."""


def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер банковской карты.

    Принимает на вход номер карты и возвращает строку в формате
    XXXX XX** **** XXXX, где видны первые 6 и последние 4 цифры.

    Args:
        card_number: Номер банковской карты в виде строки.

    Returns:
        Строка с замаскированным номером карты.
    """
    if len(card_number) != 16 or not card_number.isdigit():
        raise ValueError("Номер карты должен состоять из 16 цифр")

    masked = card_number[:6] + "*" * 6 + card_number[-4:]
    return f"{masked[:4]} {masked[4:8]} {masked[8:12]} {masked[12:]}"


def get_mask_account(account_number: str) -> str:
    """Маскирует номер банковского счета.

    Принимает на вход номер счета и возвращает строку в формате **XXXX,
    где видны только последние 4 цифры.

    Args:
        account_number: Номер банковского счета в виде строки.

    Returns:
        Строка с замаскированным номером счета.
    """
    if len(account_number) < 4 or not account_number.isdigit():
        raise ValueError("Номер счета должен состоять минимум из 4 цифр")

    return f"**{account_number[-4:]}"
