import unittest
from unittest.mock import patch, MagicMock
from collections import Counter
from src.utils import read_json_file
from main import filter_by_search, count_transactions_by_category, main


class TestTransactionProcessing(unittest.TestCase):

    def setUp(self):
        self.transactions = [
            {"description": "Оплата за услуги", "category": "Услуги", "account_number": "1234-5678-9012-3456",
             "account_type": "карта"},
            {"description": "Перевод между счетами", "category": "Переводы", "account_number": "9876-5432-1098-7654",
             "account_type": "счет"},
            {"description": "Оплата за покупки", "category": "Покупки", "account_number": "1111-2222-3333-4444",
             "account_type": "карта"},
            {"description": "Возврат товара", "category": "Покупки", "account_number": "5555-6666-7777-8888",
             "account_type": "счет"},
        ]

    def test_filter_by_search(self):
        """ Тестируем фильтрацию по строке поиска"""

        filtered = filter_by_search(self.transactions, "Оплата")
        self.assertEqual(len(filtered), 2)  # Должно вернуть 2 транзакции

        filtered = filter_by_search(self.transactions, "Перевод")
        self.assertEqual(len(filtered), 1)  # Должно вернуть 1 транзакцию

        filtered = filter_by_search(self.transactions, "Неизвестно")
        self.assertEqual(len(filtered), 0)  # Должно вернуть 0 транзакций

    def test_count_transactions_by_category(self):
        # Тестируем подсчет по категориям
        category_counts = count_transactions_by_category(self.transactions, ["Услуги", "Покупки"])
        self.assertEqual(category_counts, {"Услуги": 1, "Покупки": 2})  # Проверяем количество по категориям

        category_counts = count_transactions_by_category(self.transactions, ["Переводы"])
        self.assertEqual(category_counts, {"Переводы": 1})  # Должно вернуть 1

        category_counts = count_transactions_by_category(self.transactions, ["Неизвестно"])
        self.assertEqual(category_counts, {})  # Должно вернуть пустой словарь

    @patch('src.utils.read_json_file')
    @patch('builtins.input',
           side_effect=["path/to/file.json", "RUB", "Оплата", "EXECUTED", "возрастание", "Услуги, Покупки"])
    @patch('builtins.print')
    def test_main(self, mock_print, mock_input, mock_read_json):
        """ Имитация чтения JSON файла"""
        mock_read_json.return_value = self.transactions

        """ Вызов основной функции"""
        main()

        """ Проверка, что print был вызван"""
        mock_print.assert_any_call("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
        mock_print.assert_any_call("Описание транзакций:")
        mock_print.assert_any_call("Оплата за услуги")
        mock_print.assert_any_call("Оплата за покупки")
        mock_print.assert_any_call("Количество операций по категориям:")
        mock_print.assert_any_call("Услуги: 1")
        mock_print.assert_any_call("Покупки: 2")


if __name__ == '__main__':
    unittest.main()
