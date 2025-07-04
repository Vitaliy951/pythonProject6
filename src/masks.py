import logging
import os

""" Определяем путь к папке logs """

log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(log_dir, exist_ok=True)  # Создаем папку, если она не существует

""" Настройка логирования для модуля masks """

logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

""" Создание обработчика для записи логов в файл """

file_handler = logging.FileHandler(os.path.join(log_dir, "masks.log"))
file_handler.setLevel(logging.DEBUG)

""" Настройка форматирования логов """

file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)

""" Добавление обработчика к логгеру """

logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """
    Возвращает замаскированный номер карты.
    Формат вывода: XXXX XX** **** XXXX
    """
    """ Проверка длины и состава """

    if not card_number.isdigit() or len(card_number) != 16:
        logger.error("Номер карты должен состоять из 16 цифр.")
        raise ValueError("Номер карты должен состоять из 16 цифр.")

    """ Разбиваем карту на группы по 4 цифры """

    groups = [card_number[i: i + 4] for i in range(0, len(card_number), 4)]

    """ Первая группа (4 цифры) остается открытой """

    first_group = groups[0]

    """ Вторая группа: первая пара цифр открыта, вторая — звездочки """

    second_group = f"{groups[1][:2]}**"

    """ Третья группа полностью закрытая """

    third_group = "****"

    """ Четвёртая группа остаётся открытой """

    fourth_group = groups[3]

    """ Собираем обратно с пробелами между группами """
    masked_card_number = f"{first_group} {second_group} {third_group} {fourth_group}"
    logger.info(f"Замаскированный номер карты: {masked_card_number}")
    return masked_card_number


def get_mask_account(account_number: str) -> str:
    """
    Возвращает замаскированный номер счёта.
    Формат вывода: **** **** **** XXXX
    """
    """ Проверка длины и состава """

    if not account_number.isdigit() or len(account_number) != 16:
        logger.error("Номер счёта должен состоять из 16 цифр.")
        raise ValueError("Номер счёта должен состоять из 16 цифр.")

    """ Формируем группы по 4 символа звездочек, оставляя открытыми последние 4 цифры """

    masked_groups = ["****"] * 3  # Три группы звездочек
    last_four_digits = account_number[-4:]  # Последние 4 цифры
    masked_account_number = " ".join(masked_groups + [last_four_digits])
    logger.info(f"Замаскированный номер счёта: {masked_account_number}")
    return masked_account_number
