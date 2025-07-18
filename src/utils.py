import json
import os
import logging
import pandas as pd
from typing import List, Dict, Union

""" Настройка логирования для модуля utils """

logger = logging.getLogger('utils')
logger.setLevel(logging.DEBUG)

""" Создание директории для логов, если она не существует """
log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

""" Создание обработчика для записи логов в файл """
file_handler = logging.FileHandler(os.path.join(log_directory, 'utils.log'))
file_handler.setLevel(logging.DEBUG)

""" Настройка форматирования логов """
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

""" Добавление обработчика к логгеру """
logger.addHandler(file_handler)

def read_json_file(file_path: str) -> Union[List[Dict], None]:
    """Читает JSON-файл и возвращает список словарей с данными о транзакциях или None в случае ошибки."""

    if not os.path.exists(file_path):
        logger.error(f"Файл не найден: {file_path}")
        return None

    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
            if isinstance(data, list):
                logger.info(f"Успешно прочитан файл: {file_path}")
                return data
            logger.warning(f"Файл не содержит список: {file_path}")
            return None
        except json.JSONDecodeError:
            logger.error(f"Ошибка декодирования JSON в файле: {file_path}")
            return None


def process_events_data(df: pd.DataFrame) -> Dict[str, Union[str, List[Dict]]]:
    """Обрабатывает данные о транзакциях из DataFrame и возвращает структурированные данные.

    Аргументы:
    df -- DataFrame с данными о транзакциях.

    Возвращает:
    Словарь с итоговыми данными или сообщением об ошибке.
    """
    try:
        # Преобразуем DataFrame в список словарей
        transactions = df.to_dict(orient='records')

        # Пример обработки: фильтрация успешных операций
        successful_transactions = [t for t in transactions if t['Статус'] == 'OK']

        logger.info(f"Обработано {len(transactions)} транзакций, из них {len(successful_transactions)} успешных.")

        # Возвращаем обработанные данные
        return {
            'total_transactions': len(transactions),
            'successful_transactions': len(successful_transactions),
            'transactions': successful_transactions
        }
    except Exception as e:
        logger.error(f"Ошибка при обработке данных: {str(e)}")
        return {'error': 'Ошибка при обработке данных.'}
