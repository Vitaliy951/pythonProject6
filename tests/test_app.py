import sys
import os
from pathlib import Path

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import app  # Импортируем Flask приложение


def test_home(client):
    """Тестируем главную страницу."""
    response = client.get('/')
    assert response.status_code == 200
    assert 'Главная страница' in response.data.decode('utf-8')


def test_load_json_route(client):
    """Тестируем загрузку JSON файла."""
    response = client.get('/load_json')
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_load_csv_route(client):
    """Тестируем загрузку CSV файла."""
    response = client.get('/load_csv')
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_load_excel_route(client):
    """Тестируем загрузку Excel файла."""
    response = client.get('/load_excel')
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_cashback_analysis(client):
    """Тестируем анализ кешбэка."""
    payload = {
        'year': 2023,
        'month': 7,
        'transactions': [{'amount': 100, 'category': 'food'}]  # Пример тестовой транзакции
    }
    response = client.post('/services/cashback_analysis', json=payload)
    assert response.status_code == 200
    assert 'result' in response.json


def test_investment_service(client):
    """Тестируем сервис инвестиций."""
    payload = {
        'month': 7,
        'transactions': [{'amount': 200, 'category': 'investment'}],  # Пример тестовой транзакции
        'limit': 100
    }
    response = client.post('/services/investment_bank', json=payload)
    assert response.status_code == 200
    assert 'total_investment' in response.json


def test_simple_search(client):
    """Тестируем простой поиск."""
    payload = {'query': 'example'}
    response = client.post('/services/simple_search', json=payload)
    assert response.status_code == 200
    assert 'result' in response.json


def test_phone_search(client):
    """Тестируем поиск по номеру телефона."""
    payload = {'phone_number': '1234567890'}
    response = client.post('/services/phone_search', json=payload)
    assert response.status_code == 200
    assert 'result' in response.json


def test_person_transfer_search(client):
    """Тестируем поиск по переводам между людьми."""
    payload = {'person_id': 1}
    response = client.post('/services/person_transfer_search', json=payload)
    assert response.status_code == 200
    assert 'result' in response.json


def test_spending_by_category_report(client):
    """Тестируем отчет по тратам по категории."""
    payload = {
        'transactions': [{'amount': 50, 'category': 'food'}],  # Пример тестовой транзакции
        'category': 'food',
        'date': '2023-07-01'
    }
    response = client.post('/reports/spending_by_category', json=payload)
    assert response.status_code == 200
    assert 'report' in response.json
