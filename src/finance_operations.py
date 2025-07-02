import logging
from typing import Dict, List

import pandas as pd

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def read_financial_operations_from_csv(file_path: str) -> List[Dict]:
    """
    Считывает финансовые операции из CSV файла.

    :param file_path: Путь к файлу CSV.
    :return: Список словарей с транзакциями.
    """
    try:
        # Чтение CSV файла с разделителем ';'
        df = pd.read_csv(file_path, sep=";")
        # Преобразование DataFrame в список словарей
        transactions = df.to_dict(orient="records")
        logger.info(f"Успешно считано {len(transactions)} транзакций из {file_path}.")
        return transactions
    except Exception as e:
        logger.error(f"Ошибка при чтении CSV файла: {e}")
        return []


def read_financial_operations_from_excel(file_path: str) -> List[Dict]:
    """
    Считывает финансовые операции из Excel файла.

    :param file_path: Путь к файлу Excel.
    :return: Список словарей с транзакциями.
    """
    try:
        # Чтение Excel файла
        df = pd.read_excel(file_path)
        # Преобразование DataFrame в список словарей
        transactions = df.to_dict(orient="records")
        logger.info(f"Успешно считано {len(transactions)} транзакций из {file_path}.")
        return transactions
    except Exception as e:
        logger.error(f"Ошибка при чтении Excel файла: {e}")
        return []
