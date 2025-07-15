import re
from collections import Counter
from typing import Any, Dict, List

import pandas as pd

from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date
from src.utils import read_json_file
from src.widget import mask_account_card


def load_json(file_path: str) -> List[Dict[str, Any]]:
    """Загружает данные из JSON файла."""
    data = read_json_file(file_path)
    if data is None:
        return []

    """Преобразуем данные, чтобы гарантировать, что ключи - строки"""
    return [{str(k): v for k, v in item.items()} for item in data if isinstance(item, dict)]


def load_csv(file_path: str, delimiter: str = ";") -> List[Dict[str, Any]]:
    """Загружает данные из CSV файла."""
    df = pd.read_csv(file_path, delimiter=delimiter)
    # Преобразуем ключи столбцов в строки
    return [{str(k): v for k, v in item.items()} for item in df.to_dict(orient="records")]


def load_excel(file_path: str) -> List[Dict[str, Any]]:
    """Загружает данные из XLSX файла."""
    df = pd.read_excel(file_path)
    # Преобразуем ключи столбцов в строки
    return [{str(k): v for k, v in item.items()} for item in df.to_dict(orient="records")]


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
    print("Хай пипл! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Ваш выбор: ")
    file_path = ""

    try:
        if choice == "1":
            file_path = "data/operations.json"
            transactions = load_json(file_path)
        elif choice == "2":
            file_path = "data/transactions.csv"
            transactions = load_csv(file_path)
        elif choice == "3":
            file_path = "data/transactions_excel.xlsx"
            transactions = load_excel(file_path)
        else:
            print("Неверный выбор.")
            return

        if not transactions:
            print("Не удалось загрузить транзакции.")
            return

        """Фильтрация по статусу"""
        valid_states = ["EXECUTED", "CANCELED", "PENDING"]
        while True:
            state = (
                input(
                    "Введите статус, по которому необходимо выполнить фильтрацию. "
                    "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING: "
                )
                .strip()
                .upper()
            )
            if state in valid_states:
                break
            else:
                print(f'Статус операции "{state}" недоступен. Пожалуйста, выберите один из доступных статусов.')

        filtered_by_state = filter_by_state(transactions, state)
        print(f'Операции отфильтрованы по статусу "{state}".')

        """ Запрос на сортировку """
        sort_choice = input("Отсортировать операции по дате? Да/Нет: ").strip().lower()
        sorted_transactions = filtered_by_state
        if sort_choice == "да":
            order_choice = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
            ascending = order_choice == "возрастанию"  # не стал прописывать блок на искл. неправильного ввода
            sorted_transactions = sort_by_date(filtered_by_state, ascending)

        """Запрос на фильтрацию по валюте"""
        currency_filter_choice = input("Выводить только рублевые транзакции? Да/Нет: ").strip().lower()
        if currency_filter_choice == "да":
            sorted_transactions = filter_by_currency(sorted_transactions, "RUB")

        """Запрос на фильтрацию по слову в описании"""
        search_filter_choice = (
            input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет: ").strip().lower()
        )
        if search_filter_choice == "да":
            search_string = input("Введите слово для фильтрации: ")  # не совсем понятно, что он тут введет
            sorted_transactions = filter_by_search(sorted_transactions, search_string)

        """ Вывод результатов """
        if not sorted_transactions:
            print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
            return

        print("Распечатываю итоговый список транзакций...")
        print(f"Всего банковских операций в выборке: {len(sorted_transactions)}")
        for transaction in sorted_transactions:
            account_type = transaction.get("account_type", "счет")  # Предположим, что в транзакции есть этот ключ
            account_number = transaction.get("account_number", "")
            masked_info = mask_account_card(f"{account_type} {account_number}")
            description = transaction.get("description", "Без описания")
            amount = transaction.get("amount", "0")
            currency = transaction.get("currency", "руб.")
            date = transaction.get("date", "неизвестно")
            print(f"{date} {description}\n{masked_info}\nСумма: {amount} {currency}\n")

    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
