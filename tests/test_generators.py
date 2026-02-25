"""
Тесты для модуля generators.
"""

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def transactions():
    """Тестовый набор транзакций."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 615064591,
            "state": "CANCELED",
            "date": "2018-10-14T08:21:33.419441",
            "operationAmount": {
                "amount": "77751.04",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод организации",
            "from": "Maestro 3928549031574026",
            "to": "Счет 84163357546688983493",
        },
    ]


# filter_by_currency


def test_filter_by_currency_usd(transactions):
    """Возвращает только USD-транзакции."""
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 3
    assert all(t["operationAmount"]["currency"]["code"] == "USD" for t in result)


def test_filter_by_currency_rub(transactions):
    """Возвращает только RUB-транзакции."""
    result = list(filter_by_currency(transactions, "RUB"))
    assert len(result) == 2


def test_filter_by_currency_returns_iterator(transactions):
    """Функция возвращает итератор, а не список."""
    result = filter_by_currency(transactions, "USD")
    assert next(result)["operationAmount"]["currency"]["code"] == "USD"


def test_filter_by_currency_empty_list():
    """Пустой список — итератор пуст."""
    result = list(filter_by_currency([], "USD"))
    assert result == []


def test_filter_by_currency_not_found(transactions):
    """Валюта не найдена — возвращается пустой итератор."""
    result = list(filter_by_currency(transactions, "EUR"))
    assert result == []


def test_filter_by_currency_correct_ids(transactions):
    """Проверяем корректные ID для USD-транзакций."""
    result = list(filter_by_currency(transactions, "USD"))
    ids = [t["id"] for t in result]
    assert 939719570 in ids
    assert 895315941 in ids
    assert 142264268 in ids


@pytest.mark.parametrize(
    "currency, expected_count",
    [
        ("USD", 3),
        ("RUB", 2),
        ("EUR", 0),
    ],
)
def test_filter_by_currency_count(transactions, currency, expected_count):
    """Параметризованная проверка количества транзакций по валюте."""
    result = list(filter_by_currency(transactions, currency))
    assert len(result) == expected_count


# transaction_descriptions


def test_transaction_descriptions_count(transactions):
    """Возвращает описания для всех транзакций."""
    result = list(transaction_descriptions(transactions))
    assert len(result) == 5


def test_transaction_descriptions_order(transactions):
    """Описания возвращаются в порядке входных данных."""
    result = list(transaction_descriptions(transactions))
    assert result[0] == "Перевод организации"
    assert result[1] == "Перевод с карты на карту"
    assert result[2] == "Перевод организации"
    assert result[3] == "Перевод со счета на счет"
    assert result[4] == "Перевод организации"


def test_transaction_descriptions_returns_iterator(transactions):
    """Функция возвращает итератор."""
    result = transaction_descriptions(transactions)
    assert next(result) == "Перевод организации"


def test_transaction_descriptions_empty_list():
    """Пустой список — итератор пуст."""
    result = list(transaction_descriptions([]))
    assert result == []


def test_transaction_descriptions_missing_key():
    """Транзакция без ключа 'description' — возвращается пустая строка."""
    data = [{"id": 1, "state": "EXECUTED"}]
    result = list(transaction_descriptions(data))
    assert result == [""]


@pytest.mark.parametrize("count", [1, 3, 5])
def test_transaction_descriptions_next_n(transactions, count):
    """Можно получить первые N описаний через next()."""
    gen = transaction_descriptions(transactions)
    result = [next(gen) for _ in range(count)]
    assert len(result) == count
    assert all(isinstance(d, str) for d in result)


# card_number_generator


def test_card_number_generator_format():
    """Номер карты в правильном формате XXXX XXXX XXXX XXXX."""
    card = next(card_number_generator(1, 1))
    assert card == "0000 0000 0000 0001"


def test_card_number_generator_count():
    """Генерирует правильное количество карт."""
    result = list(card_number_generator(1, 5))
    assert len(result) == 5


def test_card_number_generator_sequence():
    """Карты генерируются последовательно."""
    result = list(card_number_generator(1, 3))
    assert result == [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
    ]


def test_card_number_generator_single():
    """Диапазон из одного элемента — один результат."""
    result = list(card_number_generator(100, 100))
    assert len(result) == 1
    assert result[0] == "0000 0000 0000 0100"


def test_card_number_generator_leading_zeros():
    """Номер дополняется ведущими нулями до 16 цифр."""
    card = next(card_number_generator(1, 1))
    digits = card.replace(" ", "")
    assert len(digits) == 16


def test_card_number_generator_spaces():
    """Карта содержит ровно 3 пробела-разделителя."""
    card = next(card_number_generator(1, 1))
    assert card.count(" ") == 3


def test_card_number_generator_max():
    """Максимальный номер корректно форматируется."""
    result = list(card_number_generator(9999999999999999, 9999999999999999))
    assert result == ["9999 9999 9999 9999"]


def test_card_number_generator_returns_iterator():
    """Функция возвращает итератор."""
    gen = card_number_generator(1, 10)
    assert next(gen) == "0000 0000 0000 0001"
    assert next(gen) == "0000 0000 0000 0002"


@pytest.mark.parametrize(
    "number, expected",
    [
        (1, "0000 0000 0000 0001"),
        (100, "0000 0000 0000 0100"),
        (9999, "0000 0000 0000 9999"),
    ],
)
def test_card_number_generator_parametrized(number, expected):
    """Параметризованная проверка форматирования номеров."""
    result = next(card_number_generator(number, number))
    assert result == expected
