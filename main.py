from src.generators import filter_by_currency, transaction_descriptions
from src.processing import filter_by_state, sort_by_date
from src.utils import read_json_file
from src.widget import mask_account_card


def main() -> None:
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    """ Загрузка транзакций"""

    file_path = input("Введите путь к файлу с транзакциями (JSON): ")
    transactions = read_json_file(file_path)

    if not transactions:
        print("Не удалось загрузить транзакции.")
        return

    """ Фильтрация по валюте"""

    currency_code = input("Введите код валюты для фильтрации: ")
    filtered_transactions = filter_by_currency(transactions, currency_code)

    """ Вывод описаний транзакций"""

    descriptions = list(transaction_descriptions(filtered_transactions))
    print("Описание транзакций:")
    for desc in descriptions:
        print(desc)

    """ Запрос статуса для фильтрации"""

    state = input("Введите статус для фильтрации (например, 'EXECUTED', 'CANCELED', 'PENDING'): ")
    filtered_by_state = filter_by_state(filtered_transactions, state)

    """ Сортировка по дате"""

    sort_order = input("Сортировать по дате (возрастание/убывание)? ").strip().lower()
    ascending = sort_order == "возрастание"
    sorted_transactions = sort_by_date(filtered_by_state, ascending)

    """ Маскирование карт и счетов"""

    for transaction in sorted_transactions:
        account_type = transaction.get("account_type", "счет")  # Предположим, что в транзакции есть этот ключ
        account_number = transaction.get("account_number", "")
        masked_info = mask_account_card(f"{account_type} {account_number}")
        print(masked_info)


if __name__ == "__main__":
    main()
