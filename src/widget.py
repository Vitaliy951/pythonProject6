from src.masks import get_mask_account as imported_get_mask_account
from src.masks import get_mask_card_number as imported_get_mask_card_number


def mask_account_card(input_str: str) -> str:
    parts = input_str.split()

    if len(parts) < 2:
        raise ValueError("Строка должна содержать тип аккаунта и номер.")

    account_type = parts[0].lower()
    number = "".join(parts[1:])

    if account_type not in ["visa", "maestro", "счет"]:
        raise ValueError("Неизвестный тип аккаунта или карты.")

    if len(number) < 16:
        raise ValueError("Номер карты должен состоять из 16 цифр.")

    if account_type == "счет":
        masked_number = imported_get_mask_account(number)  # Используем импортированную функцию
    else:
        masked_number = imported_get_mask_card_number(number)  # Используем импортированную функцию

    return f"{account_type.capitalize()} {masked_number}"


""" Функция маскирования карты"""

""" Первый блок 4 цифры, второй блок 2 цифры + *, последний блок 4 цифры"""


def local_get_mask_card_number(card_number: str) -> str:
    if len(card_number) != 16:
        raise ValueError("Номер карты должен состоять из 16 цифр.")
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


""" Новая функция маскирования счета"""


def local_get_mask_account(account_number: str) -> str:
    if len(account_number) != 16:
        raise ValueError("Номер счета должен состоять из 16 цифр.")
    masked_part = ("**** " * 3).strip()  # Создаем три блока по 4 звездочки
    last_four_digits = account_number[-4:]
    return f"{masked_part} {last_four_digits}"  # Оставляем видимыми только последние 4 цифры
