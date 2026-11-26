"""Основной модуль программы работы с банковскими транзакциями."""
import csv
import json
from datetime import datetime
from typing import Any

from openpyxl import load_workbook

from src.masks import mask_from_to
from src.search import process_bank_search


def load_xlsx_transactions(filename: str) -> list[dict]:
    """Читает транзакции из XLSX-файла.

    Args:
        filename: путь к XLSX-файлу.

    Returns:
        Список словарей: ключи — заголовки колонок, значения — данные ячеек.
    """
    book = load_workbook(filename)
    sheet = book.active
    if sheet is None:
        return []
    rows = sheet.iter_rows(values_only=True)
    header = next(rows, None)
    if header is None:
        return []
    return [dict(zip(header, row)) for row in rows]


def load_transactions(filename: str, file_type: str) -> list[dict]:
    """Читает транзакции из JSON-, CSV- или XLSX-файла.

    Args:
        filename: путь к файлу с транзакциями.
        file_type: пункт меню ("1" — JSON, "2" — CSV, "3" — XLSX).

    Returns:
        Список словарей с данными о транзакциях.
    """
    if file_type == "1":
        print("Для обработки выбран JSON-файл.")
        with open(filename, encoding="utf-8") as file:
            result: list[dict] = json.load(file)
            return result
    elif file_type == "2":
        print("Для обработки выбран CSV-файл.")
        with open(filename, encoding="utf-8", newline="") as file:
            return list(csv.DictReader(file, delimiter=";"))
    print("Для обработки выбран XLSX-файл.")
    return load_xlsx_transactions(filename)


def format_date(iso_date: str) -> str:
    """Преобразует дату формата ISO в формат ДД.ММ.ГГГГ.

    Args:
        iso_date: строка с датой.

    Returns:
        Дата в формате ДД.ММ.ГГГГ или исходная строка, если дата невалидна.
    """
    try:
        return datetime.fromisoformat(iso_date).strftime("%d.%m.%Y")
    except (ValueError, TypeError):
        return iso_date


def get_amount_and_currency(transaction: dict) -> tuple[Any, Any]:
    """Возвращает сумму и валюту операции для разных форматов файлов.

    Args:
        transaction: словарь с данными о транзакции.

    Returns:
        Кортеж: сумма и название (код) валюты.
    """
    operation = transaction.get("operationAmount")
    if isinstance(operation, dict):
        amount = operation.get("amount", 0)
        currency = operation.get("currency", {})
        if isinstance(currency, dict):
            return amount, currency.get("name", "руб.")
        return amount, currency
    return transaction.get("amount", 0), transaction.get("currency_name", "руб.")


def filter_rub_transactions(transactions: list[dict]) -> list[dict]:
    """Отбирает только рублевые транзакции.

    Args:
        transactions: список словарей с транзакциями.

    Returns:
        Список рублевых транзакций.
    """
    result: list[dict] = []
    for transaction in transactions:
        operation = transaction.get("operationAmount")
        if isinstance(operation, dict):
            currency = operation.get("currency", {})
            code = currency.get("code", "") if isinstance(currency, dict) else currency
        else:
            code = transaction.get("currency_name", transaction.get("currency", ""))
        if code in ("RUB", "руб."):
            result.append(transaction)
    return result


def print_transaction(transaction: dict) -> None:
    """Печатает одну транзакцию в удобном формате.

    Args:
        transaction: словарь с данными о транзакции.
    """
    description = transaction.get("description", "Нет описания")
    from_info = mask_from_to(transaction.get("from", ""))
    to_info = mask_from_to(transaction.get("to", ""))
    amount, currency = get_amount_and_currency(transaction)
    print(f"{format_date(str(transaction.get('date', '')))} {description}")
    if from_info or to_info:
        print(f"{from_info} -> {to_info}")
    print(f"Сумма: {amount} {currency}\n")


def main() -> None:
    """Основная логика: меню, фильтрация, сортировка и вывод операций."""
    print(
        "Привет! Добро пожаловать в программу работы с банковскими "
        "транзакциями.\n"
        "Выберите необходимый пункт меню:\n"
        "1. Получить информацию о транзакциях из JSON-файла\n"
        "2. Получить информацию о транзакциях из CSV-файла\n"
        "3. Получить информацию о транзакциях из XLSX-файла"
    )
    choice = input("Ваш выбор: ").strip()
    if choice not in ("1", "2", "3"):
        print("Такого пункта меню нет, программа завершена.")
        return

    filename = input("Введите имя файла: ").strip()
    transactions = load_transactions(filename, choice)

    available_statuses = ("EXECUTED", "CANCELED", "PENDING")
    while True:
        status = input(
            "Введите статус, по которому необходимо выполнить фильтрацию.\n"
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
        ).strip().upper()
        if status in available_statuses:
            break
        print(f'Статус операции "{status}" недоступен.')

    transactions = [
        t for t in transactions
        if str(t.get("state", "")).upper() == status
    ]
    print(f'Операции отфильтрованы по статусу "{status}"')

    if input("Отсортировать операции по дате? Да/Нет ").strip().lower() == "да":
        answer = input("Отсортировать по возрастанию или по убыванию? ")
        reverse = answer.strip().lower() == "по убыванию"
        transactions = sorted(
            transactions,
            key=lambda t: str(t.get("date", "")),
            reverse=reverse,
        )

    rub_answer = input("Выводить только рублевые транзакции? Да/Нет ")
    if rub_answer.strip().lower() == "да":
        transactions = filter_rub_transactions(transactions)

    search_answer = input(
        "Отфильтровать список транзакций по определенному слову в описании? Да/Нет "
    ).strip().lower()
    if search_answer == "да":
        word = input("Введите слово для поиска: ").strip()
        transactions = process_bank_search(transactions, word)

    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print("Распечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(transactions)}\n")
    for transaction in transactions:
        print_transaction(transaction)


if __name__ == "__main__":
    main()
