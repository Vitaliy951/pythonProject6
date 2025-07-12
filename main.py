import re
from collections import Counter
from typing import List, Dict, Any
from src.generators import filter_by_currency, transaction_descriptions
from src.processing import filter_by_state, sort_by_date
from src.utils import read_json_file
from src.widget import mask_account_card

def filter_by_search(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по заданной строке поиска."""
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    return [transaction for transaction in transactions if pattern.search(transaction.get("description", ""))]

def count_transactions_by_category(transactions: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """Подсчитывает количество транзакций по заданным категориям."""
    category_counter: Counter = Counter()  # Явная аннотация типа для переменной category_counter
    for transaction in transactions:
        category = transaction.get("category")
        if category in categories:
            category_counter[category] += 1
    return dict(category_counter)

def main() -> None:
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    """Загрузка транзакций"""
    file_path = input("Введите путь к файлу с транзакциями (JSON): ")
    transactions = read_json_file(file_path)

    if not transactions:
        print("Не удалось загрузить транзакции.")
        return

    """Фильтрация по валюте"""
    currency_code = input("Введите код валюты для фильтрации: ")
    filtered_transactions = filter_by_currency(transactions, currency_code)

    """Фильтрация по строке поиска"""
    search_string = input("Введите строку для поиска в описаниях транзакций: ")
    filtered_by_search = filter_by_search(filtered_transactions, search_string)

    if not filtered_by_search:
        print("Не найдено транзакций по заданной строке поиска.")
        return

    """Вывод описаний транзакций"""
    descriptions = list(transaction_descriptions(filtered_by_search))
    print("Описание транзакций:")
    for desc in descriptions:
        print(desc)

    """Запрос статуса для фильтрации"""
    state = input("Введите статус для фильтрации (например, 'EXECUTED', 'CANCELED', 'PENDING'): ").strip().upper()
    filtered_by_state = filter_by_state(filtered_by_search, state)

    if not filtered_by_state:
        print("Не найдено транзакций с указанным статусом.")
        return

    """Сортировка по дате"""
    sort_order = input("Сортировать по дате (возрастание/убывание)? ").strip().lower()
    ascending = sort_order == "возрастание"
    sorted_transactions = sort_by_date(filtered_by_state, ascending)

    """Маскирование карт и счетов"""
    for transaction in sorted_transactions:
        account_type = transaction.get("account_type", "счет")  # Предположим, что в транзакции есть этот ключ
        account_number = transaction.get("account_number", "")
        masked_info = mask_account_card(f"{account_type} {account_number}")
        print(masked_info)

    """Подсчет операций по категориям"""
    categories = input("Введите категории для подсчета (через запятую): ").split(",")
    categories = [cat.strip() for cat in categories]
    category_counts = count_transactions_by_category(filtered_by_state, categories)

    print("Количество операций по категориям:")
    for category, count in category_counts.items():
        print(f"{category}: {count}")

if __name__ == "__main__":
    main()
