import pytest
from widget import mask_account_card

def test_mask_account_card_visa():
    """Тестирование маскирования номера карты Visa"""
    result = mask_account_card("Visa 1234 5678 9012 3456")
    assert result == "Visa 1234 56** **** 3456"

def test_mask_account_card_maestro():
    """Тестирование маскирования номера карты Maestro"""
    result = mask_account_card("Maestro 1234 5678 9012 3456")
    assert result == "Maestro 1234 56** **** 3456"

def test_mask_account_card_account():
    """Тестирование маскирования номера счета"""
    result = mask_account_card("Счет 1234567890")
    assert result == "Счет **7890"

def test_mask_account_card_invalid_type():
    """Тестирование обработки неизвестного типа аккаунта"""
    with pytest.raises(ValueError, match="Неизвестный тип аккаунта или карты."):
        mask_account_card("UnknownType 1234 5678 9012 3456")

def test_mask_account_card_empty_input():
    """Тестирование обработки пустого ввода"""
    with pytest.raises(ValueError, match="Строка должна содержать тип аккаунта и номер."):
        mask_account_card("")

def test_mask_account_card_invalid_format():
    """Тестирование обработки некорректного формата"""
    with pytest.raises(ValueError, match="Строка должна содержать тип аккаунта и номер."):
        mask_account_card("Visa1234567890123456")  # Без пробелов

def test_mask_account_card_spaces():
    """Тестирование обработки лишних пробелов"""
    result = mask_account_card("   Visa    1234 5678 9012 3456   ")
    assert result == "Visa 1234 56** **** 3456"

def test_mask_account_card_extra_spaces():
    """Тестирование обработки лишних пробелов в типе и номере"""
    result = mask_account_card("   Maestro    1234  5678  9012  3456   ")
    assert result == "Maestro 1234 56** **** 3456"

# Запуск тестов
if __name__ == "__main__":
    pytest.main()
