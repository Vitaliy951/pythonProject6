from typing import Dict, List  # Объединяем импорты в одну строку


def filter_by_state(list_of_dictionaries: List[Dict[str, str]], state: str = 'EXECUTED') -> List[Dict[str, str]]:
    """Функция фильтрации по ключу 'state'."""

    return [item for item in list_of_dictionaries if item.get('state') == state]

def sort_by_date(list_of_dictionaries: List[Dict[str, str]], reverse: bool = True) -> List[Dict[str, str]]:
    """ Функция сортировки по дате может изменить reverse на True по умолчанию."""

    return sorted(list_of_dictionaries, key=lambda item: item.get('date'), reverse=reverse)