import pytest
from masks import get_mask_card_number, get_mask_account

def test_get_mask_card_number_valid():
    """Тестирование корректного маскирования номера карты"""
    result = get_mask_card_number("1234 5678 9012 3456")
    assert result == "1234 56** **** 3456"

def test_get_mask_card_number_invalid_length():
    """Тестирование обработки некорректной длины номера карты"""
    with pytest.raises(ValueError, match="Номер карты должен состоять из 16 цифр."):
        get_mask_card_number("1234 5678 9012")  # Слишком короткий

def test_get_mask_card_number_invalid_characters():
    """Тестирование обработки некорректных символов в номере карты"""
    with pytest.raises(ValueError, match="Номер карты должен состоять из 16 цифр."):
        get_mask_card_number("1234 5678 9012 ABCD")  # Содержит буквы

def test_get_mask_account_valid():
    """Тестирование корректного маскирования номера счета"""
    result = get_mask_account("1234567890")
    assert result == "**7890"

def test_get_mask_account_invalid_length():
    """Тестирование обработки некорректной длины номера счета"""
    with pytest.raises(ValueError, match="Номер счета должен состоять только из цифр и содержать хотя бы 4 цифры."):
        get_mask_account("123")  # Слишком короткий

def test_get_mask_account_invalid_characters():
    """Тестирование обработки некорректных символов в номере счета"""
    with pytest.raises(ValueError, match="Номер счета должен состоять только из цифр и содержать хотя бы 4 цифры."):
        get_mask_account("123A456")  # Содержит буквы

# Запуск тестов
if __name__ == "__main__":
    pytest.main()
