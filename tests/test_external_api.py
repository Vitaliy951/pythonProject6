import unittest
from unittest.mock import patch
from external_api import convert_currency  # Предполагается, что ваш код в файле external_api.py

class TestConvertCurrency(unittest.TestCase):

    @patch('external_api.requests.get')
    def test_convert_currency_success(self, mock_get):
        # Имитация успешного ответа API
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'result': 1000}

        transaction = {'amount': 10, 'currency': 'USD'}
        result = convert_currency(transaction)

        self.assertEqual(result, 1000)
        mock_get.assert_called_once()  # Проверяем, что запрос был выполнен один раз

    @patch('external_api.requests.get')
    def test_convert_currency_rub(self, mock_get):
        # Проверяем, что RUB возвращается без конвертации
        transaction = {'amount': 100, 'currency': 'RUB'}
        result = convert_currency(transaction)

        self.assertEqual(result, 100)  # Ожидаем, что сумма останется без изменений
        mock_get.assert_not_called()  # Проверяем, что запрос к API не был выполнен

    @patch('external_api.requests.get')
    def test_convert_currency_api_error(self, mock_get):
        # Имитация ошибки API
        mock_get.return_value.status_code = 500

        transaction = {'amount': 10, 'currency': 'USD'}

        with self.assertRaises(ValueError) as context:
            convert_currency(transaction)

        self.assertEqual(str(context.exception), 'Не удалось конвертировать валюту')
        mock_get.assert_called_once()  # Проверяем, что запрос был выполнен один раз

    def test_convert_currency_key_error(self):
        # Проверяем, что выбрасывается KeyError при отсутствии ключа 'currency'
        transaction = {'amount': 10}

        with self.assertRaises(KeyError):
            convert_currency(transaction)

if __name__ == '__main__':
    unittest.main()
