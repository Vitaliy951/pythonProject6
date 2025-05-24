import pytest
from widget import mask_account_card

def test_mask_account_card_visa():
    """Тестирование маскирования номера карты Visa"""
    result = mask_account_card("Visa 1234 5678 9012 3456")
    assert result == "Visa **3456"

def test_mask_account_card_maestro():
    """Тестирование маскирования номера карты Maestro"""
    result = mask_account_card("Maestro 1234 5678 9012 3456")
    assert result == "Maestro **3456"

def test_mask_account_card_account():
    """Тестирование маскирования номера счета"""
    result = mask_account_card("Счет 123456789012345678")
    assert result == "Счет ****5678"

def test_mask_account_card_unknown_type():
    """Тестирование обработки неизвестного типа аккаунта"""
    with pytest.raises(ValueError, match="Неизвестный тип аккаунта или карты."):
        mask_account_card("UnknownType 1234 5678 9012 3456")

def test_mask_account_card_empty_input():
    """Тестирование обработки пустого ввода"""
    with pytest.raises(ValueError, match="Неизвестный тип аккаунта или карты."):
        mask_account_card("")

def test_mask_account_card_invalid_format():
    """Тестирование обработки некорректного формата"""
    with pytest.raises(ValueError, match="Неизвестный тип аккаунта или карты."):
        mask_account_card("Visa1234567890123456")  # Без пробелов

def test_mask_account_card_short_number():
    """Тестирование обработки слишком короткого номера"""
    with pytest.raises(ValueError, match="Номер карты слишком короткий."):
        mask_account_card("Visa 123")  # Слишком короткий номер

def test_mask_account_card_no_number():
    """Тестирование обработки отсутствия номера"""
    with pytest.raises(ValueError, match="Номер карты слишком короткий."):
        mask_account_card("Visa")  # Отсутствует номер

# Запуск тестов
if __name__ == "__main__":
    pytest.main()
