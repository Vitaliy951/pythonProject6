def get_mask_card_number(card_number: str) -> str:
    card_number = card_number.replace(" ", "")

    # Проверка, что ввод состоит только из цифр и имеет длину 16
    if not card_number.isdigit() or len(card_number) != 16:
        raise ValueError("Номер карты должен состоять из 16 цифр.")

    # Форматирование номера карты
    masked_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[12:]}"
    return masked_number


def get_mask_account(account_number: str) -> str:
    # Удаление пробелов
    account_number = account_number.replace(" ", "")

    # Проверка, что ввод состоит только из цифр и имеет длину 4 или более
    if not account_number.isdigit() or len(account_number) < 4:
        raise ValueError("Номер счета должен состоять только из цифр и содержать хотя бы 4 цифры.")

    # Форматирование номера счета
    masked_account = f"**{account_number[-4:]}"  # Извлечение последних 4 цифр
    return masked_account
