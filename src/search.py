import re
from collections import Counter


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """
    Ищет транзакции по строке в поле description с помощью регулярных выражений.

    :param data: список словарей с банковскими операциями
    :param search: строка для поиска
    :return: список словарей, у которых description содержит искомую строку
    """
    pattern = re.compile(search, re.IGNORECASE)

    return [t for t in data if pattern.search(t.get("description", ""))]


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """
    Подсчитывает количество операций по категориям на основе поля description.

    :param data: список словарей с банковскими операциями
    :param categories: список категорий для подсчёта
    :return: словарь {категория: количество}
    """
    descriptions = [t.get("description", "") for t in data]
    counter = Counter(descriptions)

    return {category: counter.get(category, 0) for category in categories}
