import os
import requests
from dotenv import load_dotenv

load_dotenv()


def convert_currency(transaction):
    """Конвертирует сумму транзакции в рубли."""
    amount = transaction.get('amount', 0)
    currency = transaction.get('currency')

    if currency == 'RUB':
        return float(amount)

    api_key = os.getenv('EXCHANGE_API_KEY')
    url = f'https://api.apilayer.com/exchangerates_data/latest?base={currency}&symbols=RUB'

    headers = {
        "apikey": api_key
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return float(amount)  # Возвращаем исходную сумму в случае ошибки

    data = response.json()
    rate = data['rates'].get('RUB', 1)
    return float(amount) * rate
