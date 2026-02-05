import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize(
    "state, expected_count",
    [
        ("EXECUTED", 3),
        ("CANCELED", 1),
        ("NON_EXISTENT", 0),
    ],
)
def test_filter_by_state_various_states(sample_data_processing, state, expected_count):
    """Параметризованный тест для разных статусов"""
    result = filter_by_state(sample_data_processing, state)
    assert len(result) == expected_count
    for item in result:
        assert item["state"] == state


def test_filter_by_state_empty_list():
    """Проверка работы с пустым списком"""
    assert filter_by_state([], "EXECUTED") == []


def test_sort_by_date_descending(sample_data_processing):
    """Тест сортировки по убыванию (по умолчанию)"""
    result = sort_by_date(sample_data_processing)
    # Проверяем, что первая дата самая свежая
    assert result[0]["date"] == "2019-07-03T18:35:29"
    assert result[-1]["date"] == "2018-06-30T02:08:58"


def test_sort_by_date_ascending(sample_data_processing):
    """Тест сортировки по возрастанию"""
    result = sort_by_date(sample_data_processing, reverse=False)
    assert result[0]["date"] == "2018-06-30T02:08:58"
    assert result[-1]["date"] == "2019-07-03T18:35:29"


def test_sort_by_date_same_dates(sample_data_processing):
    result = sort_by_date(sample_data_processing)
    dates = [item["date"] for item in result]
    assert dates.count("2018-06-30T02:08:58") == 2


@pytest.mark.parametrize(
    "invalid_data, expected",
    [
        ([{"id": 1}], [{"id": 1}]),  # Отсутствует ключ date (по коду вернет как есть)
        ([{"date": "not-a-date"}], [{"date": "not-a-date"}]),  # Нестандартный формат
    ],
)
def test_sort_by_date_edge_cases(invalid_data, expected):
    """Тест на нестандартные входные данные"""
    assert sort_by_date(invalid_data) == expected
