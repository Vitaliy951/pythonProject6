import pytest
import json
import os
from collections import Counter
from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date
from src.utils import read_json_file
from src.widget import mask_account_card
from main import load_json, filter_by_search, count_transactions_by_category


@pytest.fixture
def transactions():
    """Фикстура для предоставления тестовых данных."""
    return [
        {
            "date": "2023-01-01",
            "description": "Оплата услуги",
            "amount": 100,
            "currency": "RUB",
            "status": "EXECUTED",
            "account_number": "1234567890123456",
            "category": "Услуги",
            "operationAmount": {
                "amount": 100,
                "currency": {
                    "code": "RUB"
                }
            }
        },
        {
            "date": "2023-01-02",
            "description": "Перевод средств",
            "amount": 200,
            "currency": "RUB",
            "status": "CANCELED",
            "account_number": "1234567890123456",
            "category": "Переводы",
            "operationAmount": {
                "amount": 200,
                "currency": {
                    "code": "RUB"
                }
            }
        },
        {
            "date": "2023-01-03",
            "description": "Оплата товара",
            "amount": 150,
            "currency": "USD",
            "status": "PENDING",
            "account_number": "1234567890123456",
            "category": "Товары",
            "operationAmount": {
                "amount": 150,
                "currency": {
                    "code": "USD"
                }
            }
        }
    ]


@pytest.fixture
def temp_json_file(tmp_path):
    """Создает временный JSON файл для тестирования."""
    data = [
        {
            "date": "2023-01-01",
            "description": "Оплата услуги",
            "amount": 100,
            "currency": "RUB",
            "status": "EXECUTED",
            "account_number": "1234567890123456",
            "category": "Услуги",
            "operationAmount": {
                "amount": 100,
                "currency": {
                    "code": "RUB"
                }
            }
        },
        {
            "date": "2023-01-02",
            "description": "Перевод средств",
            "amount": 200,
            "currency": "RUB",
            "status": "CANCELED",
            "account_number": "1234567890123456",
            "category": "Переводы",
            "operationAmount": {
                "amount": 200,
                "currency": {
                    "code": "RUB"
                }
            }
        }
    ]
    # Создаем временный файл
    json_file = tmp_path / "test_data.json"
    with open(json_file, 'w') as f:
        json.dump(data, f)
    return json_file


def load_json(file_path: str):
    """Загружает данные из JSON файла."""
    return read_json_file(file_path)


def read_json_file(file_path: str):
    """Читает JSON-файл и возвращает список словарей с данными о транзакциях или пустой список в случае ошибки."""

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
            if isinstance(data, list):
                return data
            return []
        except json.JSONDecodeError:
            return []


def test_load_json(temp_json_file):
    """Тестирует функцию загрузки данных из JSON файла."""
    result = load_json(temp_json_file)
    assert len(result) == 2  # Проверяем, что загружено 2 записи
    assert result[0]["description"] == "Оплата услуги"  # Проверяем первое описание
    assert result[1]["status"] == "CANCELED"  # Проверяем статус второй записи


def test_load_json_invalid_file():
    """Тестирует функцию загрузки данных из несуществующего файла."""
    with pytest.raises(FileNotFoundError):
        load_json("non_existent_file.json")


def test_load_json_empty_file(tmp_path):
    """Тестирует функцию загрузки данных из пустого JSON файла."""
    empty_file = tmp_path / "empty.json"
    with open(empty_file, 'w') as f:
        f.write("")
    result = load_json(empty_file)
    assert result == []  # Ожидаем, что результат будет пустым списком


def filter_by_search(transactions, query):
    """Фильтрует транзакции по описанию."""
    return [tx for tx in transactions if query.lower() in tx["description"].lower()]


def test_filter_by_search(transactions):
    result = filter_by_search(transactions, "услуги")
    assert len(result) == 1
    assert result[0]["description"] == "Оплата услуги"


def count_transactions_by_category(transactions, categories):
    """Считает количество транзакций по категориям."""
    counts = Counter(tx["category"] for tx in transactions if tx["category"] in categories)
    return dict(counts)


def test_count_transactions_by_category(transactions):
    categories = ["Услуги", "Переводы"]
    counts = count_transactions_by_category(transactions, categories)
    assert counts["Услуги"] == 1
    assert counts["Переводы"] == 1
    assert "Товары" not in counts


def filter_by_currency(transactions, currency_code):
    """Фильтрует транзакции по коду валюты."""
    return [
        tx for tx in transactions
        if "operationAmount" in tx and
           "currency" in tx["operationAmount"] and
           tx["operationAmount"]["currency"]["code"] == currency_code
    ]


def test_filter_by_currency(transactions):
    result = filter_by_currency(transactions, "RUB")
    assert len(result) == 2  # Две транзакции в рублях


def filter_by_state(transactions, state):
    """Фильтрует транзакции по статусу."""
    return [tx for tx in transactions if "status" in tx and tx["status"] == state]


def test_filter_by_state(transactions):
    result = filter_by_state(transactions, "EXECUTED")
    assert len(result) == 1
    assert result[0]["status"] == "EXECUTED"


def sort_by_date(transactions, ascending=True):
    """Сортирует транзакции по дате."""
    return sorted(transactions, key=lambda x: x["date"], reverse=not ascending)


def test_sort_by_date(transactions):
    sorted_transactions = sort_by_date(transactions, ascending=True)
    assert sorted_transactions[0]["date"] == "2023-01-01"


if __name__ == '__main__':
    pytest.main()
