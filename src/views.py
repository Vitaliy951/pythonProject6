import json
import os
import pandas as pd
import requests
from django.http import JsonResponse
from datetime import datetime
from dotenv import load_dotenv
from src.services import analyze_cashback_categories, investment_bank

# Загружаем переменные окружения
load_dotenv()

# Получаем API ключ один раз в глобальной области
API_KEY = os.getenv('EXCHANGE_API_KEY')


def fetch_currency_rates(base_currency, symbols):
    """Получает текущие курсы валют."""
    url = f'https://api.apilayer.com/exchangerates_data/live?base={base_currency}&symbols={",".join(symbols)}'
    headers = {'apikey': API_KEY}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise ValueError('Не удалось получить курсы валют')

    return response.json()


def fetch_stock_prices(stocks):
    """Получает цены акций из S&P 500."""
    # Для примера просто возвращаем фиктивные данные
    return {stock: 100.0 for stock in stocks}  # Замените на реальный запрос к API


def greeting_message(current_time):
    """Возвращает приветственное сообщение в зависимости от времени суток."""
    if current_time.hour < 6:
        return "Доброй ночи"
    elif current_time.hour < 12:
        return "Доброе утро"
    elif current_time.hour < 18:
        return "Добрый день"
    else:
        return "Добрый вечер"


def events_view(request):
    """
    Обрабатывает данные событий и возвращает JSON-ответ.
    Ожидает входящую дату и данные о транзакциях.
    """
    try:
        data = json.loads(request.body)
        input_date_str = data.get('input_date')  # Ожидаем входящую дату в формате 'YYYY-MM-DD HH:MM:SS'
        transactions = data.get('transactions', [])

        if not input_date_str:
            return JsonResponse({'error': 'Не указана входящая дата.'}, status=400)

        input_date = datetime.strptime(input_date_str, '%Y-%m-%d %H:%M:%S')
        current_time = datetime.now()

        # Приветствие
        greeting = greeting_message(current_time)

        # Обработка транзакций
        df = pd.DataFrame(transactions)

        # Получение данных по картам
        card_summary = df.groupby('Номер карты').agg(
            total_spent=('Сумма операции', 'sum'),
            cashback=('Сумма операции', lambda x: (x.sum() // 100))
        ).reset_index()

        card_summary['last_digits'] = card_summary['Номер карты'].astype(str).str[-4:]

        # Топ-5 транзакций
        top_transactions = df.nlargest(5, 'Сумма операции')[
            ['Дата операции', 'Сумма операции', 'Категория', 'Описание']].to_dict(orient='records')

        # Получение курсов валют и цен акций
        user_currencies = ["USD", "EUR"]  # Замените на получение из user_settings.json
        currency_rates = fetch_currency_rates('USD', user_currencies)
        stock_prices = fetch_stock_prices(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"])

        # Формирование JSON-ответа
        response_data = {
            "greeting": greeting,
            "cards": card_summary[['last_digits', 'total_spent', 'cashback']].to_dict(orient='records'),
            "top_transactions": top_transactions,
            "currency_rates": [{"currency": k, "rate": v} for k, v in currency_rates['rates'].items()],
            "stock_prices": [{"stock": stock, "price": price} for stock, price in stock_prices.items()]
        }

        return JsonResponse(response_data, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
