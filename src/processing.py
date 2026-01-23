"""
Модуль для обработки данных о банковских операциях.
Содержит функции для фильтрации операций по статусу и сортировки по дате.
"""

from typing import Any


def filter_by_state(data: list[dict[str, Any]], state: str = "EXECUTED") -> list[dict[str, Any]]:
    """
    Фильтрует список операций по статусу.

    Аргументы:
        data (list[dict[str, Any]]): Список словарей с данными о банковских операциях.
                                     Каждый словарь должен содержать ключи: 'id', 'state', 'date'.
        state (str): Значение статуса для фильтрации. По умолчанию 'EXECUTED'.
                     Возможные значения: 'EXECUTED', 'CANCELED'.

    Возвращает:
        list[dict[str, Any]]: Новый список словарей, содержащий только операции
                              с указанным статусом.

    Примеры:
        >>> operations = [
        ...     {'id': 414288290, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29'},
        ...     {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58'},
        ...     {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25'}
        ... ]

        >>> filter_by_state(operations)
        [{'id': 414288290, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29'},
         {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58'}]

        >>> filter_by_state(operations, state='CANCELED')
        [{'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25'}]
    """
    # Создаем новый список, содержащий только операции с нужным статусом
    filtered_data = []

    for operation in data:
        # Проверяем, есть ли ключ 'state' в словаре и соответствует ли его значение
        if operation.get("state") == state:
            filtered_data.append(operation)

    return filtered_data


def sort_by_date(data: list[dict[str, Any]], reverse: bool = True) -> list[dict[str, Any]]:
    """
    Сортирует список операций по дате.

    Аргументы:
        data (list[dict[str, Any]]): Список словарей с данными о банковских операциях.
                                     Каждый словарь должен содержать ключ 'date' в формате ISO 8601.
        reverse (bool): Порядок сортировки. По умолчанию True (убывание - сначала новые).
                        - True: сортировка по убыванию (от новых к старым)
                        - False: сортировка по возрастанию (от старых к новым)

    Возвращает:
        list[dict[str, Any]]: Новый список словарей, отсортированный по дате.

    Примеры:
        >>> operations = [
        ...     {'id': 414288290, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29'},
        ...     {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58'},
        ...     {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33'}
        ... ]

        >>> # Сортировка по убыванию (сначала самые новые)
        >>> sort_by_date(operations)
        [{'id': 414288290, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29'},
         {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33'},
         {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58'}]

        >>> # Сортировка по возрастанию (сначала самые старые)
        >>> sort_by_date(operations, reverse=False)
        [{'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58'},
         {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33'},
         {'id': 414288290, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29'}]
    """

    # Если ключ 'date' отсутствует, возвращаем пустую строку (она будет в конце при сортировке)
    def get_date(operation: dict[str, Any]) -> Any:
        return operation.get("date", "")

    # key=get_date - указываем, по какому полю сортировать
    # reverse=reverse - задаем порядок сортировки
    sorted_data = sorted(data, key=get_date, reverse=reverse)

    return sorted_data
