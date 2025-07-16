from typing import Dict, Iterator, List

def filter_by_currency(transactions: List[Dict], currency_code: str) -> List[Dict]:
    """Фильтрует транзакции по коду валюты."""
    filtered_transactions = []
    for tx in transactions:
        # Проверяем, есть ли ключи для JSON и для CSV/Excel
        if "operationAmount" in tx:
            # Для JSON формата
            if tx["operationAmount"]["currency"]["code"] == currency_code:
                filtered_transactions.append(tx)
        elif "currency_code" in tx:
            # Для CSV и Excel форматов
            if tx["currency_code"] == currency_code:
                filtered_transactions.append(tx)
    return filtered_transactions

def transaction_descriptions(transactions: List[Dict]) -> Iterator[str]:
    """Возвращает список описаний транзакций."""
    return (tx["description"] for tx in transactions)

def card_number_generator(start: int, count: int) -> Iterator[str]:
    """Генерирует номера карт в формате 'dddd dddd dddd dddd'."""
    for i in range(start, start + count):
        yield f"{0:04d} {0:04d} {0:04d} {i:04d}"
