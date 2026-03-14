import json
import os
import pytest
from unittest.mock import mock_open, patch

from src.utils import get_transactions_from_json


# ---------------------------------------------------------------------------
# Фикстуры
# ---------------------------------------------------------------------------

SAMPLE_TRANSACTIONS = [
    {
        "id": 1,
        "state": "EXECUTED",
        "operationAmount": {"amount": "100.00", "currency": {"code": "RUB"}},
    },
    {
        "id": 2,
        "state": "CANCELED",
        "operationAmount": {"amount": "200.00", "currency": {"code": "USD"}},
    },
]

def test_returns_list_of_dicts(tmp_path: pytest.TempPathFactory) -> None:
    """Функция возвращает список словарей при корректном JSON-файле."""
    json_file = tmp_path / "operations.json"
    json_file.write_text(json.dumps(SAMPLE_TRANSACTIONS), encoding="utf-8")

    result = get_transactions_from_json(str(json_file))

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["id"] == 1


def test_returns_correct_data(tmp_path: pytest.TempPathFactory) -> None:
    """Данные в возвращаемом списке соответствуют содержимому файла."""
    json_file = tmp_path / "operations.json"
    json_file.write_text(json.dumps(SAMPLE_TRANSACTIONS), encoding="utf-8")

    result = get_transactions_from_json(str(json_file))

    assert result == SAMPLE_TRANSACTIONS

def test_empty_file_returns_empty_list(tmp_path: pytest.TempPathFactory) -> None:
    """Пустой JSON-файл (пустой список) возвращает пустой список."""
    json_file = tmp_path / "empty.json"
    json_file.write_text("[]", encoding="utf-8")

    result = get_transactions_from_json(str(json_file))

    assert result == []


def test_file_with_dict_returns_empty_list(tmp_path: pytest.TempPathFactory) -> None:
    """Если JSON содержит словарь (не список) — возвращает пустой список."""
    json_file = tmp_path / "dict.json"
    json_file.write_text(json.dumps({"key": "value"}), encoding="utf-8")

    result = get_transactions_from_json(str(json_file))

    assert result == []


def test_file_with_string_returns_empty_list(tmp_path: pytest.TempPathFactory) -> None:
    """Если JSON содержит строку — возвращает пустой список."""
    json_file = tmp_path / "string.json"
    json_file.write_text('"just a string"', encoding="utf-8")

    result = get_transactions_from_json(str(json_file))

    assert result == []


def test_file_not_found_returns_empty_list() -> None:
    """Если файл не существует — возвращает пустой список."""
    result = get_transactions_from_json("/non/existent/path/operations.json")

    assert result == []


def test_invalid_json_returns_empty_list(tmp_path: pytest.TempPathFactory) -> None:
    """Если файл содержит невалидный JSON — возвращает пустой список."""
    json_file = tmp_path / "broken.json"
    json_file.write_text("{not valid json", encoding="utf-8")

    result = get_transactions_from_json(str(json_file))

    assert result == []


def test_uses_open_with_utf8_encoding() -> None:
    """Функция открывает файл с кодировкой utf-8."""
    mock_data = json.dumps(SAMPLE_TRANSACTIONS)
    with patch("builtins.open", mock_open(read_data=mock_data)) as m:
        get_transactions_from_json("some_path.json")
        m.assert_called_once_with("some_path.json", "r", encoding="utf-8")
