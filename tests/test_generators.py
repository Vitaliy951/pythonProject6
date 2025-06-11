from typing import Any, Dict, List  # Импортируем необходимые типы

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions  # Импортируем функции


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура для тестирования с образцом транзакций."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        },
    ]


def test_filter_by_currency(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тестирование функции фильтрации транзакций по валюте."""
    usd_transactions = list(filter_by_currency(sample_transactions, "USD"))
    assert len(usd_transactions) == 2
    assert all(tx["operationAmount"]["currency"]["code"] == "USD" for tx in usd_transactions)

    rub_transactions = list(filter_by_currency(sample_transactions, "RUB"))
    assert len(rub_transactions) == 1
    assert all(tx["operationAmount"]["currency"]["code"] == "RUB" for tx in rub_transactions)

    eur_transactions = list(filter_by_currency(sample_transactions, "EUR"))
    assert len(eur_transactions) == 0


def test_transaction_descriptions(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тестирование функции получения описаний транзакций."""
    descriptions = list(transaction_descriptions(sample_transactions))
    assert descriptions == [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет"
    ]

    empty_descriptions = list(transaction_descriptions([]))
    assert empty_descriptions == []


def test_card_number_generator() -> None:
    """Тестирование генератора номеров карт."""
    card_numbers = list(card_number_generator(1, 5))
    assert card_numbers == [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005"
    ]
