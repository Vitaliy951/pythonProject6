import json
import os
import logging
from typing import List, Dict, Union

""" Настройка логирования для модуля utils """

logger = logging.getLogger('utils')
logger.setLevel(logging.DEBUG)

""" Создание обработчика для записи логов в файл """

file_handler = logging.FileHandler('logs/utils.log')
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
