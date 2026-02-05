import pytest


@pytest.fixture
def card_numbers():
    return [
        ("7000792289606361", "7000 79** **** 6361"),
        (" 7000 7922 8960 636 1 ", "7000 79** **** 6361"),
        ("1234567812345678", "1234 56** **** 5678"),
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


@pytest.fixture
def payment_info():
    return [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 7000792289606361", "Maestro 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ]


@pytest.fixture
def invalid_payment_info():
    return [
        None,
        "",
        "Visa Platinum",
        "Счет",
        "Счет **4305",
        "7000792289606361",
    ]


@pytest.fixture
def dates():
    return [
        ("2026-02-01T02:32:02.000Z", "01.02.2026"),
        ("2026-02-05T02:32:02.379Z", "05.02.2026"),
    ]


@pytest.fixture
def invalid_dates():
    return [
        "2023/10/25T14:30:00",
        "2023-10-25T14:30:00 GMT+3",
        "2023-02-30T10:00:00",
    ]


@pytest.fixture
def sample_data_processing():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2019-07-03T18:35:29"},
        {"id": 2, "state": "EXECUTED", "date": "2018-06-30T02:08:58"},
        {"id": 3, "state": "CANCELED", "date": "2018-09-12T21:27:25"},
        {"id": 4, "state": "EXECUTED", "date": "2018-06-30T02:08:58"},
    ]
