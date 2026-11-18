## Модуль generators

Модуль содержит генераторы для эффективной обработки массивов транзакций
без загрузки всех результатов в память.

### filter_by_currency

Возвращает итератор по транзакциям в заданной валюте:

    usd_transactions = filter_by_currency(transactions, "USD")
    for _ in range(2):
        print(next(usd_transactions))

### transaction_descriptions

Генератор описаний операций:

    descriptions = transaction_descriptions(transactions)
    for _ in range(5):
        print(next(descriptions))

### card_number_generator

Генерирует номера карт в формате `XXXX XXXX XXXX XXXX`:

    for card_number in card_number_generator(1, 5):
        print(card_number)

## Новый функционал

Добавлен декоратор log (src/decorators.py).

Декоратор логирует работу функции:
- при успешном выполнении — имя функции;
- при ошибке — имя функции, тип ошибки и входные параметры;
- если задан аргумент filename — лог пишется в файл;
- если не задан — лог выводится в консоль.

Пример использования:

@log(filename="mylog.txt")
def my_function(x, y):
    return x + y

Запуск тестов с отчётом покрытия:

pytest --cov=src --cov-report=html --cov-report=term
