import pytest
from src.masks import get_mask_card_number, get_mask_account


def test_get_mask_card_number_correct(card_numbers):
    for card_num, expected in card_numbers:
        assert get_mask_card_number(card_num) == expected


def test_get_mask_card_number_value_error(invalid_card_numbers):
    for card_num in invalid_card_numbers:
        with pytest.raises(ValueError):
            get_mask_card_number(card_num)


def test_get_mask_account_correct(card_accounts):
    for card_num, expected in card_accounts:
        assert get_mask_account(card_num) == expected


def test_get_mask_account_value_error(invalid_card_accounts):
    for card_num in invalid_card_accounts:
        with pytest.raises(ValueError):
            get_mask_account(card_num)
