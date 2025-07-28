import pytest
import pandas as pd
from unittest.mock import patch, mock_open
from src.utils import read_json_file, create_json_file, process_events_data


def test_read_json_file_success():
    mock_data = '[{"id": 1, "description": "Транзакция 1"}]'
    with patch('builtins.open', mock_open(read_data=mock_data)):
        result = read_json_file('dummy_path')  # Используется замоканная версия
        expected = [{"id": 1, "description": "Транзакция 1"}]
        assert result == expected


def test_read_json_file_empty_list():
    mock_data = '[]'
    with patch('builtins.open', mock_open(read_data=mock_data)):
        result = read_json_file('dummy_path')
        assert result == []


def test_read_json_file_invalid_json():
    mock_data = '{"id": 1, "description": "Транзакция 1"'  # некорректный JSON
    with patch('builtins.open', mock_open(read_data=mock_data)):
        result = read_json_file('dummy_path')
        assert result is None


@patch('os.makedirs')
@patch('builtins.open', new_callable=mock_open)
def test_create_json_file_success(mock_file, mock_makedirs):
    data = [{"id": 1, "description": "Транзакция 1"}]
    create_json_file('data/transactions.json', data)
    mock_file.assert_called_once_with('data/transactions.json', 'w', encoding='utf-8')

    # Проверка, что write был вызван с корректными данными
    handle = mock_file()
    handle.write.assert_any_call('[\n    {\n        "id": 1,\n        "description": "Транзакция 1"\n    }\n]\n')


@patch('os.makedirs')
@patch('builtins.open', new_callable=mock_open)
def test_create_json_file_directory_creation(mock_file, mock_makedirs):
    data = [{"id": 1, "description": "Транзакция 1"}]
    create_json_file('data/transactions.json', data)
    mock_makedirs.assert_called_once_with('data')


def test_process_events_data():
    data = {
        'id': [1, 2],
        'description': ['Транзакция 1', 'Транзакция 2'],
        'Статус': ['OK', 'Ошибка']
    }
    df = pd.DataFrame(data)
    result = process_events_data(df)
    expected = {
        'total_transactions': 2,
        'successful_transactions': 1,
        'transactions': [{'id': 1, 'description': 'Транзакция 1', 'Статус': 'OK'}]
    }
    assert result == expected


def test_process_events_data_empty():
    df = pd.DataFrame(columns=['id', 'description', 'Статус'])
    result = process_events_data(df)
    expected = {
        'total_transactions': 0,
        'successful_transactions': 0,
        'transactions': []
    }
    assert result == expected
