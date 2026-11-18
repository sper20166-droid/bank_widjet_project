"""Модуль содержит декоратор log для логирования работы функций."""

from functools import wraps
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable[..., Any]:
    """Декоратор, который логирует начало, конец и результат выполнения функции.

    Если filename задан — логи пишутся в файл, иначе выводятся в консоль.

    Args:
        filename (Optional[str]): имя файла для логов. По умолчанию None.

    Returns:
        Callable: обёрнутая функция с логированием.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Оборачивает функцию и записывает лог её работы."""
            try:
                result = func(*args, **kwargs)
                message = f"{func.__name__} ok"
                _write_log(message, filename)
                return result
            except Exception as error:
                message = (
                    f"{func.__name__} error: {type(error).__name__}. "
                    f"Inputs: {args}, {kwargs}"
                )
                _write_log(message, filename)
                raise
        return wrapper
    return decorator


def _write_log(message: str, filename: Optional[str]) -> None:
    """Записывает сообщение в файл или выводит его в консоль.

    Args:
        message (str): текст лога.
        filename (Optional[str]): путь к файлу логов или None.
    """
    if filename:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(message + "\n")
    else:
        print(message)
