import pytest
import os
import logging
from src.decorators import log

""" Логируем в консоль """


@log(filename=None)
def add(x: int, y: int) -> int:
    return x + y


@log(filename=None)
def divide(x: int, y: int) -> float:
    return x / y


def test_add_success(caplog):
    with caplog.at_level(logging.INFO):
        result = add(2, 3)
        assert result == 5

    """  Проверяем вывод в логах"""

    assert "Функция 'add' завершена успешно, результат: 5" in caplog.text


def test_divide_success(caplog):
    with caplog.at_level(logging.INFO):
        result = divide(10, 2)
        assert result == 5.0

    """  Проверяем вывод в логах """
    assert "Функция 'divide' завершена успешно, результат: 5.0" in caplog.text


def test_divide_zero_division(caplog):
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    """  Проверяем вывод в логах """

    assert "Функция 'divide' вызвана с ошибкой: division by zero. Inputs: (10, 0), {}" in caplog.text


def test_log_file_created():
    logfile = "test_log.txt"
    log_decorator = log(filename=logfile)

    @log_decorator
    def test_func():
        return "test"

    test_func()

    assert os.path.exists(logfile)

    """ # Удаляем файл после теста """

    os.remove(logfile)


def test_log_file_content():
    logfile = "test_log.txt"
    log_decorator = log(filename=logfile)

    @log_decorator
    def test_func(x):
        return x

    test_func(42)

    with open(logfile, "r") as f:
        log_content = f.read()

    assert "Функция 'test_func' завершена успешно, результат: 42" in log_content


"""  Удаляем файл после теста"""

os.remove(logfile)
