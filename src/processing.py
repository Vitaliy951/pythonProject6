from datetime import datetime
from typing import Dict, List


def filter_by_state(data: List[Dict], state: str) -> List[Dict]:
    """Фильтрация списка словарей по заданному статусу state."""
    return [item for item in data if item.get("state") == state]


def sort_by_date(data: List[Dict], ascending: bool = True) -> List[Dict]:
    """Сортировка списка словарей по датам."""
    return sorted(data, key=lambda x: x['date'], reverse=not ascending)

def format_date(date_str: str, current_format: str, desired_format: str) -> str:
    """Преобразование даты из одного формата в другой."""
    date_obj = datetime.strptime(date_str, current_format)
    return date_obj.strftime(desired_format)
