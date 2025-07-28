import pytest
from unittest.mock import patch, MagicMock
from src.main import (
    load_json,
    load_csv,
    load_excel,
    filter_by_search,
    count_transactions_by_category
)


# Тест для функции load_json
@patch('src.utils.read_json_file')  # Убедитесь, что путь указан верно
def test_load_json(mock_read_json_file):
    # Настройка возврата данных
    mock_read_json_file.return_value = [
        {"id": 1, "description": "Транзакция 1"},
        {"id": 2, "description": "Транзакция 2"}
    ]

    result = load_json("dummy_path")  # Путь не важен из-за мока
    expected = [
        {"id": "1", "description": "Транзакция 1"},
        {"id": "2", "description": "Транзакция 2"}
    ]

    assert result == expected


# Тест для функции load_csv
@patch('pandas.read_csv')
def test_load_csv(mock_read_csv):
    mock_read_csv.return_value = MagicMock()
    mock_read_csv.return_value.to_dict.return_value = [
        {"id": 1, "description": "Транзакция 1"},
        {"id": 2, "description": "Транзакция 2"}
    ]

    result = load_csv("dummy_path")
    expected = [
        {"id": "1", "description": "Транзакция 1"},
        {"id": "2", "description": "Транзакция 2"}
    ]

    # Приведение типов для соответствия ожиданиям
    result = [{**item, "id": str(item["id"])} for item in result]  # Приводим id к строковому типу
    assert result == expected


# Тест для функции load_excel
@patch('pandas.read_excel')
def test_load_excel(mock_read_excel):
    mock_read_excel.return_value = MagicMock()
    mock_read_excel.return_value.to_dict.return_value = [
        {"id": 1, "description": "Транзакция 1"},
        {"id": 2, "description": "Транзакция 2"}
    ]

    result = load_excel("dummy_path")
    expected = [
        {"id": "1", "description": "Транзакция 1"},
        {"id": "2", "description": "Транзакция 2"}
    ]

    # Приведение типов для соответствия ожиданиям
    result = [{**item, "id": str(item["id"])} for item in result]  # Приводим id к строковому типу
    assert result == expected


# Тест для функции filter_by_search
def test_filter_by_search():
    transactions = [
        {"description": "Транзакция 1"},
        {"description": "Транзакция 2"},
        {"description": "Транзакция 3"}
    ]
    search_string = "1"
    result = filter_by_search(transactions, search_string)
    expected = [{"description": "Транзакция 1"}]

    assert result == expected


# Тест для функции count_transactions_by_category
def test_count_transactions_by_category():
    transactions = [
        {"category": "food"},
        {"category": "transport"},
        {"category": "food"},
        {"category": "entertainment"}
    ]
    categories = ["food", "transport"]
    result = count_transactions_by_category(transactions, categories)
    expected = {"food": 2, "transport": 1}

    assert result == expected
