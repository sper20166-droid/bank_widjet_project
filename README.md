## Считывание финансовых операций из файлов

Проект поддерживает загрузку транзакций не только из JSON, но и из файлов
форматов CSV и Excel.

Функции находятся в модуле `src/file_reader.py`:

- `get_transactions_from_csv(file_path: str)` — принимает путь к CSV-файлу
  и возвращает список словарей с финансовыми операциями;
- `get_transactions_from_excel(file_path: str)` — принимает путь к файлу Excel
  и возвращает список словарей с финансовыми операциями.

Пример использования:

```python
from src.file_reader import get_transactions_from_csv

transactions = get_transactions_from_csv("data/transactions.csv")
print(transactions[0])

