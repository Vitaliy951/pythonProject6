from masks import get_mask_card_number, get_mask_account


def mask_account_card(input_str: str) -> str:
    """Разделение строки на тип и номер"""

    input_str = input_str.strip()  # Удаление лишних пробелов
    parts = input_str.split()

    if len(parts) < 2:
        raise ValueError("Строка должна содержать тип аккаунта и номер.")

    account_type = parts[0].strip().lower()  # Первый элемент как тип аккаунта
    number = " ".join(parts[1:]).strip()  # Остальные части как номер

    # Проверка типа карты
    if account_type in ["visa", "maestro"]:
        masked_number = get_mask_card_number(number)  # Номер карты
        return f"{account_type.capitalize()} {masked_number}"
    # Проверка типа счета
    elif account_type == "счет":
        masked_account = get_mask_account(number)  # Номер счета
        return f"{account_type.capitalize()} {masked_account}"
    else:
        raise ValueError("Неизвестный тип аккаунта или карты.")
