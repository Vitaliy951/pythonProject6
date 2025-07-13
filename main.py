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

<<<<<<< HEAD
def load_json(file_path: str) -> List[Dict[str, Any]]:
    """Загружает данные из JSON файла."""
    return read_json_file(file_path)


def load_csv(file_path: str) -> List[Dict[str, Any]]:
    """Загружает данные из CSV файла."""
    df = pd.read_csv(file_path)
    return df.to_dict(orient='records')


def load_excel(file_path: str) -> List[Dict[str, Any]]:
    """Загружает данные из XLSX файла."""
    df = pd.read_excel(file_path)
    return df.to_dict(orient='records')

def filter_by_search(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по заданной строке поиска."""
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    return [transaction for transaction in transactions if pattern.search(transaction.get("description", ""))]

def count_transactions_by_category(transactions: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """Подсчитывает количество транзакций по заданным категориям."""
    category_counter: Counter = Counter()
    for transaction in transactions:
        category = transaction.get("category")
        if category in categories:
            category_counter[category] += 1
    return dict(category_counter)

def main() -> None:
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Ваш выбор: ")
    file_path = ""

    if choice == "1":
        file_path = input("Введите путь к JSON-файлу: ")
        transactions = load_json(file_path)
    elif choice == "2":
        file_path = input("Введите путь к CSV-файлу: ")
        transactions = load_csv(file_path)
    elif choice == "3":
        file_path = input("Введите путь к XLSX-файлу: ")
        transactions = load_excel(file_path)
    else:
        print("Неверный выбор.")
        return

=======
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

>>>>>>> 8c6d2b8bca74ec3fec9f0cd037aef1601d9ca49b
    if not transactions:
        print("Не удалось загрузить транзакции.")
        return

<<<<<<< HEAD
    # Фильтрация по валюте
    currency_code = input("Введите код валюты для фильтрации: ")
    filtered_transactions = filter_by_currency(transactions, currency_code)

    # Фильтрация по строке поиска
=======
    """Фильтрация по валюте"""
    currency_code = input("Введите код валюты для фильтрации: ")
    filtered_transactions = filter_by_currency(transactions, currency_code)

    """Фильтрация по строке поиска"""
>>>>>>> 8c6d2b8bca74ec3fec9f0cd037aef1601d9ca49b
    search_string = input("Введите строку для поиска в описаниях транзакций: ")
    filtered_by_search = filter_by_search(filtered_transactions, search_string)

    if not filtered_by_search:
        print("Не найдено транзакций по заданной строке поиска.")
        return

<<<<<<< HEAD
    # Вывод описаний транзакций
=======
    """Вывод описаний транзакций"""
>>>>>>> 8c6d2b8bca74ec3fec9f0cd037aef1601d9ca49b
    descriptions = list(transaction_descriptions(filtered_by_search))
    print("Описание транзакций:")
    for desc in descriptions:
        print(desc)

<<<<<<< HEAD
    # Запрос статуса для фильтрации
=======
    """Запрос статуса для фильтрации"""
>>>>>>> 8c6d2b8bca74ec3fec9f0cd037aef1601d9ca49b
    state = input("Введите статус для фильтрации (например, 'EXECUTED', 'CANCELED', 'PENDING'): ").strip().upper()
    filtered_by_state = filter_by_state(filtered_by_search, state)

    if not filtered_by_state:
        print("Не найдено транзакций с указанным статусом.")
        return

<<<<<<< HEAD
    # Сортировка по дате
=======
    """Сортировка по дате"""
>>>>>>> 8c6d2b8bca74ec3fec9f0cd037aef1601d9ca49b
    sort_order = input("Сортировать по дате (возрастание/убывание)? ").strip().lower()
    ascending = sort_order == "возрастание"
    sorted_transactions = sort_by_date(filtered_by_state, ascending)

<<<<<<< HEAD
    # Маскирование карт и счетов
=======
    """Маскирование карт и счетов"""
>>>>>>> 8c6d2b8bca74ec3fec9f0cd037aef1601d9ca49b
    for transaction in sorted_transactions:
        account_type = transaction.get("account_type", "счет")  # Предположим, что в транзакции есть этот ключ
        account_number = transaction.get("account_number", "")
        masked_info = mask_account_card(f"{account_type} {account_number}")
        print(masked_info)

<<<<<<< HEAD
    # Подсчет операций по категориям
=======
    """Подсчет операций по категориям"""
>>>>>>> 8c6d2b8bca74ec3fec9f0cd037aef1601d9ca49b
    categories = input("Введите категории для подсчета (через запятую): ").split(",")
    categories = [cat.strip() for cat in categories]
    category_counts = count_transactions_by_category(filtered_by_state, categories)

    print("Количество операций по категориям:")
    for category, count in category_counts.items():
        print(f"{category}: {count}")

if __name__ == "__main__":
    main()
