import os
import requests
from dotenv import load_dotenv

""" Загружаем переменные окружения """

load_dotenv()

""" Получаем API ключ один раз в глобальной области """

API_KEY = os.getenv('EXCHANGE_API_KEY')


def convert_currency(transaction: dict) -> float:

    """Конвертирует сумму транзакции в рубли."""

    amount = transaction.get('amount', 0)
    currency = transaction['currency']  # Используем прямой доступ, чтобы вызвать KeyError при отсутствии ключа

    if currency == 'RUB':
        return float(amount)

    """ Формируем URL и параметры запроса """

    url = 'https://api.apilayer.com/exchangerates_data/convert'
    params = {'to': 'RUB', 'from': currency, 'amount': amount}
    headers = {'apikey': API_KEY}

    """ Выполняем запрос к API """

    response = requests.get(url, headers=headers, params=params)

    """ Проверяем статус ответа """

    if response.status_code != 200:
        raise ValueError('Не удалось конвертировать валюту')  # Выбрасываем исключение при ошибке

    """  Парсим ответ """

    data = response.json()
    return data['result']  # Возвращаем результат конвертации
