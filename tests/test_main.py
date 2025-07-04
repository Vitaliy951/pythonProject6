import pytest
from unittest.mock import patch, MagicMock
from main import main


@pytest.fixture
def mock_transactions():
    return [
        {
            "operationAmount": {
                "currency": {"code": "RUB"},
                "amount": 1000
            },
            "description": "Транзакция 1",
            "state": "EXECUTED",
            "account_type": "счет",
            "account_number": "1234567812345678",
            "date": "2023-01-01"
        },
        {
            "operationAmount": {
                "currency": {"code": "USD"},
                "amount": 500
            },
            "description": "Транзакция 2",
            "state": "CANCELED",
            "account_type": "visa",
            "account_number": "8765432187654321",
            "date": "2023-02-01"
        }
    ]


@patch('main.read_json_file')
@patch('main.mask_account_card')
def test_main(mock_mask_account_card, mock_read_json_file, mock_transactions):
    mock_read_json_file.return_value = mock_transactions
    mock_mask_account_card.return_value = "MASKED_ACCOUNT 1234"

    with patch('builtins.input', side_effect=["mock_path.json", "RUB", "EXECUTED", "возрастание"]):
        main()

    mock_read_json_file.assert_called_once_with("mock_path.json")
    mock_mask_account_card.assert_called_with("счет 1234567812345678")
    assert mock_mask_account_card.call_count == 1


if __name__ == "__main__":
    pytest.main()
