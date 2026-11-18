"""Тесты для декоратора log."""
from pathlib import Path

import pytest

from src.decorators import log


def test_log_to_console_ok(capsys: pytest.CaptureFixture) -> None:
    """Успешный вызов функции логируется в консоль."""

    @log()
    def add(a: int, b: int) -> int:
        """Возвращает сумму чисел."""
        return a + b

    add(1, 2)
    captured = capsys.readouterr()
    assert "add ok" in captured.out


def test_log_to_console_error(capsys: pytest.CaptureFixture) -> None:
    """Ошибка логируется в консоль с типом и входными параметрами."""

    @log()
    def divide(a: int, b: int) -> float:
        """Делит a на b."""
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)
    captured = capsys.readouterr()
    assert "divide error: ZeroDivisionError" in captured.out
    assert "Inputs: (1, 0), {}" in captured.out


def test_log_to_file_ok(tmp_path: Path) -> None:
    """Успешный вызов функции логируется в файл."""
    file_path = tmp_path / "log.txt"

    @log(filename=str(file_path))
    def multiply(a: int, b: int) -> int:
        """Умножает числа."""
        return a * b

    multiply(2, 3)
    assert "multiply ok" in file_path.read_text(encoding="utf-8")


def test_log_to_file_error(tmp_path: Path) -> None:
    """Ошибка логируется в файл с типом ошибки и параметрами."""
    file_path = tmp_path / "log.txt"

    @log(filename=str(file_path))
    def raise_error() -> None:
        """Вызывает ошибку для теста."""
        raise ValueError("test")

    with pytest.raises(ValueError):
        raise_error()
    content = file_path.read_text(encoding="utf-8")
    assert "raise_error error: ValueError" in content
    assert "Inputs: (), {}" in content


def test_log_with_kwargs() -> None:
    """Декоратор корректно работает с keyword-аргументами."""

    @log()
    def power(base: int, exponent: int) -> int:
        """Возводит base в степень exponent."""
        return base ** exponent

    assert power(base=2, exponent=3) == 8



