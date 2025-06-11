import pytest

from src.masks import get_mask_account, get_mask_card_number


# Тестирование get_mask_card_number
def test_get_mask_card_number_normal_case():
    result = get_mask_card_number("1234567890123456")
    assert result == "1234 56** **** 3456"

def test_get_mask_card_number_incorrect_length():
    with pytest.raises(ValueError, match="Номер карты должен состоять из 16 цифр."):
        get_mask_card_number("123456789012345")

def test_get_mask_card_number_non_digit():
    with pytest.raises(ValueError, match="Номер карты должен состоять из 16 цифр."):
        get_mask_card_number("1234abcd90123456")

# Тестирование get_mask_account
def test_get_mask_account_normal_case():
    result = get_mask_account("1234567890123456")
    assert result == "**** **** **** 3456"

def test_get_mask_account_incorrect_length():
    with pytest.raises(ValueError, match="Номер счёта должен состоять из 16 цифр."):
        get_mask_account("123456789012345")

def test_get_mask_account_non_digit():
    with pytest.raises(ValueError, match="Номер счёта должен состоять из 16 цифр."):
        get_mask_account("1234abcd90123456")