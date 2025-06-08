from typing import Dict, Iterator, List


def filter_by_currency(transactions: List[Dict], currency_code: str) -> List[Dict]:
    """Фильтрует транзакции по коду валюты."""
    return [tx for tx in transactions if tx["operationAmount"]["currency"]["code"] == currency_code]


def transaction_descriptions(transactions: List[Dict]) -> Iterator[str]:
    """Возвращает список описаний транзакций."""
    return (tx["description"] for tx in transactions)


def card_number_generator(start: int, count: int) -> Iterator[str]:
    """Генерирует номера карт в формате 'dddd dddd dddd dddd'."""
    for i in range(start, start + count):
        yield f"{0:04d} {0:04d} {0:04d} {i:04d}"
