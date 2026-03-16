import os
from typing import Any

import requests
from dotenv import load_dotenv

from src.logger import get_logger

load_dotenv()

EXCHANGE_RATES_API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")
EXCHANGE_RATES_BASE_URL = "https://api.apilayer.com/exchangerates_data/convert"

logger = get_logger(__name__)


def convert_transaction_amount(transaction: dict[str, Any]) -> float:
    """
    Возвращает сумму транзакции в рублях (RUB).

    Если валюта транзакции RUB — возвращает сумму как есть.
    Если валюта USD или EUR — обращается к Exchange Rates Data API
    для получения актуального курса и конвертирует сумму в рубли.

    :param transaction: Словарь с данными о транзакции. Ожидается ключ
                        operationAmount -> amount / currency -> code.
    :return: Сумма транзакции в рублях, тип float.
    :raises ValueError: Если данные транзакции некорректны или API недоступен.
    """
    try:
        operation = transaction["operationAmount"]
        amount = float(operation["amount"])
        currency_code = operation["currency"]["code"]
    except (KeyError, TypeError, ValueError) as e:
        logger.error(f"Некорректные данные транзакции: {e}")
        raise ValueError(f"Некорректные данные транзакции: {e}") from e

    logger.info(f"Валюта: {currency_code}, Количество: {amount}")

    if currency_code == "RUB":
        return amount

    if currency_code not in ("USD", "EUR"):
        logger.error(f"Неподдерживаемая валюта: {currency_code}")
        raise ValueError(f"Неподдерживаемая валюта: {currency_code}")

    return _fetch_converted_amount(amount, currency_code, "RUB")


def _fetch_converted_amount(amount: float, from_currency: str, to_currency: str) -> float:
    """
    Выполняет запрос к Exchange Rates Data API для конвертации суммы.

    :param amount: Сумма для конвертации.
    :param from_currency: Исходная валюта (например, 'USD').
    :param to_currency: Целевая валюта (например, 'RUB').
    :return: Сконвертированная сумма, тип float.
    :raises ValueError: Если API вернул ошибку или ключ не задан.
    """
    if not EXCHANGE_RATES_API_KEY:
        logger.error("API-ключ не задан")
        raise ValueError("API-ключ не задан. Установите EXCHANGE_RATES_API_KEY в файле .env")

    params = {
        "to": to_currency,
        "from": from_currency,
        "amount": amount,
    }
    headers = {"apikey": EXCHANGE_RATES_API_KEY}

    try:
        response = requests.get(EXCHANGE_RATES_BASE_URL, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        logger.error(f"Ошибка запроса к API конвертации: {e}")
        raise ValueError(f"Ошибка запроса к API конвертации: {e}") from e

    if not data.get("success"):
        error_info = data.get("error", {})
        logger.error(f"API вернул ошибку: {error_info}")
        raise ValueError(f"API вернул ошибку: {error_info}")

    result: float = data["result"]
    return result
