from unittest.mock import MagicMock, patch

import pytest

from src.external_api import convert_transaction_amount


@pytest.fixture
def rub_transaction() -> dict:
    return {
        "operationAmount": {
            "amount": "5000.00",
            "currency": {"name": "руб.", "code": "RUB"},
        }
    }


@pytest.fixture
def usd_transaction() -> dict:
    return {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"name": "USD", "code": "USD"},
        }
    }


@pytest.fixture
def eur_transaction() -> dict:
    return {
        "operationAmount": {
            "amount": "50.00",
            "currency": {"name": "EUR", "code": "EUR"},
        }
    }


def test_rub_transaction_returns_amount_as_is(rub_transaction: dict) -> None:
    """RUB-транзакция возвращает сумму без вызова API."""
    result = convert_transaction_amount(rub_transaction)
    assert result == 5000.0


def test_rub_transaction_does_not_call_api(rub_transaction: dict) -> None:
    """При RUB-транзакции requests.get не вызывается."""
    with patch("src.external_api.requests.get") as mock_get:
        convert_transaction_amount(rub_transaction)
        mock_get.assert_not_called()


def test_usd_transaction_calls_api(usd_transaction: dict) -> None:
    """При USD-транзакции происходит обращение к внешнему API."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"success": True, "result": 9000.0}
    mock_response.raise_for_status = MagicMock()

    with patch("src.external_api.requests.get", return_value=mock_response) as mock_get:
        with patch("src.external_api.EXCHANGE_RATES_API_KEY", "test_key"):
            result = convert_transaction_amount(usd_transaction)

    mock_get.assert_called_once()
    assert result == 9000.0


def test_usd_transaction_returns_converted_amount(usd_transaction: dict) -> None:
    """Функция возвращает сконвертированную сумму из ответа API."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"success": True, "result": 9123.45}
    mock_response.raise_for_status = MagicMock()

    with patch("src.external_api.requests.get", return_value=mock_response):
        with patch("src.external_api.EXCHANGE_RATES_API_KEY", "test_key"):
            result = convert_transaction_amount(usd_transaction)

    assert result == 9123.45


def test_eur_transaction_returns_converted_amount(eur_transaction: dict) -> None:
    """EUR-транзакция корректно конвертируется в рубли."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"success": True, "result": 5250.0}
    mock_response.raise_for_status = MagicMock()

    with patch("src.external_api.requests.get", return_value=mock_response):
        with patch("src.external_api.EXCHANGE_RATES_API_KEY", "test_key"):
            result = convert_transaction_amount(eur_transaction)

    assert result == 5250.0


def test_api_called_with_correct_params(usd_transaction: dict) -> None:
    """Запрос к API содержит корректные параметры (from, to, amount)."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"success": True, "result": 9000.0}
    mock_response.raise_for_status = MagicMock()

    with patch("src.external_api.requests.get", return_value=mock_response) as mock_get:
        with patch("src.external_api.EXCHANGE_RATES_API_KEY", "test_key"):
            convert_transaction_amount(usd_transaction)

    _, kwargs = mock_get.call_args
    params = kwargs.get("params", mock_get.call_args[0][1] if len(mock_get.call_args[0]) > 1 else {})
    assert params["from"] == "USD"
    assert params["to"] == "RUB"
    assert params["amount"] == 100.0


def test_missing_api_key_raises_value_error(usd_transaction: dict) -> None:
    """Если API-ключ не задан, выбрасывается ValueError."""
    with patch("src.external_api.EXCHANGE_RATES_API_KEY", ""):
        with pytest.raises(ValueError, match="API-ключ не задан"):
            convert_transaction_amount(usd_transaction)


def test_api_error_response_raises_value_error(usd_transaction: dict) -> None:
    """Если API возвращает success=False, выбрасывается ValueError."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"success": False, "error": {"code": 101, "type": "invalid_access_key"}}
    mock_response.raise_for_status = MagicMock()

    with patch("src.external_api.requests.get", return_value=mock_response):
        with patch("src.external_api.EXCHANGE_RATES_API_KEY", "test_key"):
            with pytest.raises(ValueError, match="API вернул ошибку"):
                convert_transaction_amount(usd_transaction)


def test_network_error_raises_value_error(usd_transaction: dict) -> None:
    """Сетевая ошибка (RequestException) поднимается как ValueError."""
    import requests as req_lib

    with patch("src.external_api.requests.get", side_effect=req_lib.ConnectionError("timeout")):
        with patch("src.external_api.EXCHANGE_RATES_API_KEY", "test_key"):
            with pytest.raises(ValueError, match="Ошибка запроса к API"):
                convert_transaction_amount(usd_transaction)


def test_invalid_transaction_structure_raises_value_error() -> None:
    """Если структура транзакции некорректна, выбрасывается ValueError."""
    bad_transaction = {"id": 1, "state": "EXECUTED"}

    with pytest.raises(ValueError, match="Некорректные данные транзакции"):
        convert_transaction_amount(bad_transaction)


def test_unsupported_currency_raises_value_error() -> None:
    """Неподдерживаемая валюта (не RUB/USD/EUR) вызывает ValueError."""
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"name": "GBP", "code": "GBP"},
        }
    }

    with pytest.raises(ValueError, match="Неподдерживаемая валюта"):
        convert_transaction_amount(transaction)
