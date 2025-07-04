from typing import Dict, List


def filter_by_state(list_of_dictionaries: List[Dict[str, str]], state: str = "EXECUTED") -> List[Dict[str, str]]:
    """Функция фильтрации по ключу 'state'."""

    return [item for item in list_of_dictionaries if item.get("state") == state]


def sort_by_date(list_of_dictionaries: List[Dict[str, str]], reverse: bool = True) -> List[Dict[str, str]]:
    """Функция сортировки по дате может изменить reverse на True по умолчанию."""

    """ Фильтруем словари, у которых значение по ключу 'date' не None"""

    filtered_list = [item for item in list_of_dictionaries if item.get("date") is not None]

    return sorted(
        filtered_list, key=lambda item: item["date"], reverse=reverse  # Теперь мы уверены, что 'date' не None
    )
