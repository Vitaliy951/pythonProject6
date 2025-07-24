import logging
import pandas as pd
from functools import wraps
import json

logging.basicConfig(level=logging.INFO)


def report_decorator(filename='default_report.json'):
    """Декоратор для записи отчетов в файл."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=4)
            return result

        return wrapper

    return decorator


@report_decorator('spending_report.json')
def spending_by_category(transactions, category, date=None):
    """Возвращает траты по заданной категории за последние три месяца."""
    df = pd.DataFrame(transactions)
    if date:
        current_date = pd.to_datetime(date)
    else:
        current_date = pd.to_datetime('now')

    three_months_ago = current_date - pd.DateOffset(months=3)
    filtered_df = df[(df['Дата операции'] >= three_months_ago) & (df['Категория'] == category)]

    total_spent = filtered_df['Сумма операции'].sum()

    return {category: total_spent}
