import pytest

from src.processing import filter_by_state, format_date, sort_by_date


def test_filter_by_state():
    """Тестирование фильтрации по статусу."""
    data = [
        {"state": "approved", "date": "2025-05-01"},
        {"state": "pending", "date": "2025-05-02"},
        {"state": "approved", "date": "2025-05-03"},
    ]
    result = filter_by_state(data, "approved")
    assert len(result) == 2
    assert all(item["state"] == "approved" for item in result)

def test_sort_by_date_ascending():
    """Тестирование сортировки по дате в порядке возрастания."""
    data = [
        {"state": "pending", "date": "2025-05-02"},
        {"state": "approved", "date": "2025-05-01"},
        {"state": "completed", "date": "2025-05-03"},
    ]
    result = sort_by_date(data, ascending=True)
    assert result[0]["date"] == "2025-05-01"  # Проверка, что первая дата - 1 мая

def test_sort_by_date_descending():
    """Тестирование сортировки по дате в порядке убывания."""
    data = [
        {"state": "pending", "date": "2025-05-02"},
        {"state": "approved", "date": "2025-05-01"},
        {"state": "completed", "date": "2025-05-03"},
    ]
    result = sort_by_date(data, ascending=False)
    assert result[0]["date"] == "2025-05-03"  # Проверка, что первая дата - 3 мая

def test_format_date():
    """Тестирование преобразования формата даты."""
    date_str = "2025-05-01"
    current_format = "%Y-%m-%d"
    desired_format = "%d/%m/%Y"
    result = format_date(date_str, current_format, desired_format)
    assert result == "01/05/2025"  # Проверка правильного преобразования даты

def test_format_date_invalid():
    """Тестирование обработки неверного формата даты."""
    with pytest.raises(ValueError):
        format_date("invalid-date", "%Y-%m-%d", "%d/%m/%Y")
