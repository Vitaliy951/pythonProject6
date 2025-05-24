def mask_account_card(input_str: str) -> str:
    """Разделение строки на тип и номер"""

    if not input_str.strip():
        raise ValueError("Неизвестный тип аккаунта или карты.")

    parts = input_str.split()
    account_type = parts[0]  # Извлекаем только первый элемент как тип аккаунта
    number = ''.join(parts[1:])  # Объединяем остальные части как номер

    if account_type.lower() not in ["visa", "maestro", "счет"]:
        raise ValueError("Неизвестный тип аккаунта или карты.")

    # Проверка на пустой номер или слишком короткий номер
    if len(number) < 4:
        raise ValueError("Номер карты слишком короткий.")

    masked_number = number[:-4].replace(number[:-4], '**') + number[-4:]  # Маскируем все, кроме последних 4 цифр

    if account_type.lower() == "счет":
        masked_number = number[:-4].replace(number[:-4], '****') + number[-4:]  # Маскируем все, кроме последних 4 цифр

    return f"{account_type} {masked_number}"
