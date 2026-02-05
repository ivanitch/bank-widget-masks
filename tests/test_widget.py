import pytest
from src.widget import mask_account_card, get_date


def test_get_mask_account_card(payment_info):
    for payment, expected in payment_info:
        assert mask_account_card(payment) == expected


def test_get_mask_account_card_invalid_value(invalid_payment_info):
    for payment in invalid_payment_info:
        with pytest.raises(ValueError):
            mask_account_card(payment)


def test_get_date(dates):
    for date, expected in dates:
        assert get_date(date) == expected


def test_get_date_invalid_value(invalid_dates):
    for date in invalid_dates:
        with pytest.raises(ValueError):
            get_date(date)
