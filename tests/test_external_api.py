import pytest
from src.external_api import convert_currency
import requests
from unittest.mock import patch


def test_convert_currency_to_rub():
    transaction = {"amount": 100, "currency": "RUB"}
    result = convert_currency(transaction)
    assert result == 100.0


@patch("src.external_api.requests.get")
def test_convert_currency_usd(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"rates": {"RUB": 75.0}}

    transaction = {"amount": 100, "currency": "USD"}
    result = convert_currency(transaction)
    assert result == 7500.0


@patch("src.external_api.requests.get")
def test_convert_currency_invalid_currency(mock_get):
    mock_get.return_value.status_code = 400

    transaction = {"amount": 100, "currency": "EUR"}
    result = convert_currency(transaction)
    assert result == 100.0  # Возвращаем исходную сумму
