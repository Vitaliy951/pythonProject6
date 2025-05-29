import pytest
from src.widget import mask_account_card

# Тестирование нормального случая
def test_mask_account_card_normal_case():
    result = mask_account_card("Visa 1234567890123456")
    assert result == "Visa 1234 56** **** 3456"

# Тестирование неизвестного типа аккаунта
def test_mask_account_card_unknown_type():
    with pytest.raises(ValueError, match="Неизвестный тип аккаунта или карты."):
        mask_account_card("unknown 1234567890123456")

# Тестирование недостаточной длины номера
def test_mask_account_card_short_number():
    with pytest.raises(ValueError, match="Номер карты должен состоять из 16 цифр."):
        mask_account_card("Visa 1234")

# Тестирование границы минимальной длины строки
def test_mask_account_card_minimal_string():
    with pytest.raises(ValueError, match="Строка должна содержать тип аккаунта и номер."):
        mask_account_card("V")

# Тестирование короткого имени типа аккаунта
def test_mask_account_card_too_short_type():
    with pytest.raises(ValueError, match="Неизвестный тип аккаунта или карты."):
        mask_account_card("v 1234567890123456")

# Тестирование границы с пустым номером
def test_mask_account_card_empty_number():
    with pytest.raises(ValueError, match="Строка должна содержать тип аккаунта и номер."):
        mask_account_card("Visa ")

# Тестирование короткого типа аккаунта
def test_mask_account_card_short_type():
    with pytest.raises(ValueError, match="Неизвестный тип аккаунта или карты."):
        mask_account_card("vi 1234567890123456")

# Тестирование слишком длинного имени типа аккаунта
def test_mask_account_card_long_type_name():
    with pytest.raises(ValueError, match="Неизвестный тип аккаунта или карты."):
        mask_account_card("superlongtypename 1234567890123456")

# Тестирование "счет"-типа
def test_mask_account_card_account():
    result = mask_account_card("счет 1234567890123456")
    assert result == "Счет **** **** **** 3456"