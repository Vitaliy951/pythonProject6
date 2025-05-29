def get_mask_card_number(card_number: str) -> str:
    """
    Возвращает замаскированный номер карты.
    Формат вывода: XXXX XX** **** XXXX
    """
    # Проверка длины и состава
    if not card_number.isdigit() or len(card_number) != 16:
        raise ValueError("Номер карты должен состоять из 16 цифр.")

    # Разбиваем карту на группы по 4 цифры
    groups = [
        card_number[i:i+4] for i in range(0, len(card_number), 4)
    ]

    # Первая группа (4 цифры) остается открытой
    first_group = groups[0]
    # Вторая группа: первая пара цифр открыта, вторая — звездочки
    second_group = f"{groups[1][:2]}**"
    # Третья группа полностью закрытая
    third_group = "****"
    # Четвёртая группа остаётся открытой
    fourth_group = groups[3]

    # Собираем обратно с пробелами между группами
    return f"{first_group} {second_group} {third_group} {fourth_group}"


def get_mask_account(account_number: str) -> str:
    """
    Возвращает замаскированный номер счёта.
    Формат вывода: **** **** **** XXXX
    """
    # Проверка длины и состава
    if not account_number.isdigit() or len(account_number) != 16:
        raise ValueError("Номер счёта должен состоять из 16 цифр.")

    # Формируем группы по 4 символа звездочек, оставляя открытыми последние 4 цифры
    masked_groups = ['****'] * 3  # Три группы звездочек
    last_four_digits = account_number[-4:]  # Последние 4 цифры
    return ' '.join(masked_groups + [last_four_digits])