import pytest


@pytest.fixture
def card_numbers():
    return [
        ("7000792289606361", "7000 79** **** 6361"),
        (" 7000 7922 8960 636 1 ", "7000 79** **** 6361"),
        ("1234567812345678", "1234 56** **** 5678")
    ]


@pytest.fixture
def invalid_card_numbers():
    return [
        "7000792289606361000000",  # > 16
        "70007922896",  # < 16
        "7000792289606lll",  # только цифры
        "  ",  # пробелы
        "",  # пусто
        None,  # None
    ]


@pytest.fixture
def card_accounts():
    return [
        ("73654108430135874305", "**4305"),
        (" 7365 4108 4301 3587 430 5 ", "**4305"),
        ("73654108430135872980", "**2980"),
    ]


@pytest.fixture
def invalid_card_accounts():
    return [
        "73",  # < 4
        "73lll",  # только цифры
        "  ",  # пробелы
        "",  # пусто
        None,  # None
    ]
