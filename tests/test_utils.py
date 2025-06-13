import pytest
from src.utils import read_json_file
import os


def test_read_json_file(mocker):
    mock_open = mocker.patch("builtins.open", mocker.mock_open(read_data='[{"amount": 100, "currency": "RUB"}]'))
    result = read_json_file("data/operations.json")
    assert result == [{"amount": 100, "currency": "RUB"}]


def test_read_json_file_empty():
    result = read_json_file("data/empty.json")
    assert result == []


def test_read_json_file_not_found():
    result = read_json_file("data/non_existent.json")
    assert result == []
