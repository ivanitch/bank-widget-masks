"""
Модуль generators — генераторы для обработки банковских транзакций.

Содержит функции для эффективной работы с большими объёмами данных
с использованием генераторов и итераторов Python.
"""

from typing import Any, Iterator


def filter_by_currency(transactions: list[dict[str, Any]], currency: str) -> Iterator[dict[str, Any]]:
    """
    Фильтрует транзакции по коду валюты операции.

    Принимает список транзакций и код валюты, возвращает итератор,
    который поочерёдно выдаёт только те транзакции, где валюта операции
    соответствует заданной.

    Аргументы:
        transactions (list[dict]): Список словарей с данными о транзакциях.
                                   Каждый словарь должен содержать ключ
                                   'operationAmount' с вложенным 'currency'.
        currency (str): Код валюты для фильтрации, например 'USD' или 'RUB'.

    Возвращает:
        Iterator[dict]: Итератор транзакций с заданной валютой.

    Примеры:
        >>> usd_transactions = filter_by_currency(transactions, 'USD')
        >>> for t in usd_transactions:
        ...     print(t['id'])
    """
    for transaction in transactions:
        transaction_currency = transaction.get("operationAmount", {}).get("currency", {}).get("code", "")
        if transaction_currency == currency:
            yield transaction


def transaction_descriptions(transactions: list[dict[str, Any]]) -> Iterator[str]:
    """
    Генератор описаний банковских транзакций.

    Принимает список транзакций и поочерёдно возвращает описание
    каждой операции из поля 'description'.

    Аргументы:
        transactions (list[dict]): Список словарей с данными о транзакциях.
                                   Каждый словарь должен содержать ключ
                                   'description'.

    Возвращает:
        Iterator[str]: Итератор строк с описаниями операций.

    Примеры:
        >>> descriptions = transaction_descriptions(transactions)
        >>> print(next(descriptions))
        Перевод организации
    """
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """
    Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.

    Генерирует номера карт в заданном диапазоне от start до stop включительно.
    Диапазон значений: от 0000 0000 0000 0001 до 9999 9999 9999 9999.

    Аргументы:
        start (int): Начальное значение диапазона (включительно).
        stop (int): Конечное значение диапазона (включительно).

    Возвращает:
        Iterator[str]: Итератор строк с отформатированными номерами карт.

    Примеры:
        >>> for card in card_number_generator(1, 3):
        ...     print(card)
        0000 0000 0000 0001
        0000 0000 0000 0002
        0000 0000 0000 0003
    """
    for number in range(start, stop + 1):
        # Дополняем нулями до 16 цифр и разбиваем на блоки по 4
        raw = str(number).zfill(16)
        yield f"{raw[0:4]} {raw[4:8]} {raw[8:12]} {raw[12:16]}"
