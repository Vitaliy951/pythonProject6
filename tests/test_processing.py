import pytest
from processing import filter_by_state, sort_by_date

@pytest.mark.parametrize("data, state, expected", [
    ([{"id": 1, "state": "active"}, {"id": 2, "state": "inactive"}], "active", [{"id": 1, "state": "active"}]),
    ([{"id": 1, "state": "active"}, {"id": 2, "state": "inactive"}], "inactive", [{"id": 2, "state": "inactive"}]),
    ([{"id": 1, "state": "active"}, {"id": 2, "state": "inactive"}], "pending", []),  # Нет словарей с таким статусом
    ([{"id": 1, "state": "active"}, {"id": 2, "state": "active"}], "active", [{"id": 1, "state": "active"}, {"id": 2, "state": "active"}]),
])
def test_filter_by_state(data, state, expected):
    assert filter_by_state(data, state) == expected

def test_sort_by_date_ascending():
    data = [
        {"id": 1, "date": "2023-05-01"},
        {"id": 2, "date": "2023-04-01"},
        {"id": 3, "date": "2023-05-01"},
    ]
    sorted_data = sort_by_date(data, ascending=True)
    assert sorted_data == [
        {"id": 2, "date": "2023-04-01"},
        {"id": 1, "date": "2023-05-01"},
        {"id": 3, "date": "2023-05-01"},
    ]
def test_sort_by_date_descending():
    data = [
        {"id": 1, "date": "2023-05-01"},
        {"id": 2, "date": "2023-04-01"},
        {"id": 3, "date": "2023-05-01"},
    ]
    sorted_data = sort_by_date(data, ascending=False)
    assert sorted_data == [
        {"id": 1, "date": "2023-05-01"},
        {"id": 3, "date": "2023-05-01"},
        {"id": 2, "date": "2023-04-01"},
    ]

def test_sort_by_date_invalid_format():
    data = [
        {"id": 1, "date": "2023-05-01"},
        {"id": 2, "date": "invalid-date"},
    ]
    with pytest.raises(ValueError):
        sort_by_date(data)
