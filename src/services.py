import pandas as pd
from typing import List, Dict, Any


def analyze_cashback_categories(data: List[Dict[str, Any]], year: int, month: int) -> Dict[str, float]:
    """Анализирует выгодные категории повышенного кешбэка."""
    df = pd.DataFrame(data)
    df['Дата операции'] = pd.to_datetime(df['Дата операции'])

    # Фильтрация по году и месяцу
    filtered_df = df[(df['Дата операции'].dt.year == year) & (df['Дата операции'].dt.month == month)]

    # Группировка по категориям
    cashback_analysis = filtered_df.groupby('Категория')['Сумма операции'].sum().to_dict()

    # Рассчитываем кешбэк
    cashback_analysis = {category: amount // 100 for category, amount in cashback_analysis.items()}

    return cashback_analysis


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """Возвращает сумму, которую удалось бы отложить в «Инвесткопилку»."""
    df = pd.DataFrame(transactions)
    df['Дата операции'] = pd.to_datetime(df['Дата операции'])

    # Фильтруем транзакции по месяцу
    filtered_df = df[df['Дата операции'].dt.strftime('%Y-%m') == month]

    # Рассчитываем округление
    total_investment = 0.0
    for amount in filtered_df['Сумма операции']:
        rounded_amount = (amount // limit + 1) * limit
        total_investment += rounded_amount - amount

    return total_investment
