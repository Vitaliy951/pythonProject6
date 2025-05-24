from datetime import datetime
from typing import List, Dict

def filter_by_state(data: List[Dict], state: str) -> List[Dict]:
    """Фильтрация списка словарей по заданному статусу state."""
    return [item for item in data if item.get("state") == state]
def sort_by_date(data: List[Dict], ascending: bool = True) -> List[Dict]:
    """Сортировка списка словарей по датам."""
    return sorted(data, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=not ascending)
