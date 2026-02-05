from src.processing import filter_by_state, sort_by_date
from src.widget import get_date, mask_account_card


def main():
    processing_operations = [
        {"id": 414288290, "state": "EXECUTED", "date": "2019-07-03T18:35:29.051309"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 142264268, "state": "EXECUTED", "date": "2019-04-04T23:20:05.206878"},
    ]

    try:
        # Маскировка номера карты
        card = "Visa Platinum 7000792289606361"
        masked_card = mask_account_card(card)

        print("=" * 70)
        print("ДЕМОНСТРАЦИЯ МОДУЛЯ WIDGET")
        print("=" * 70)

        print(f"Исходная карта: {card}")
        print(f"Замаскированная карта: {masked_card}")

        print()

        # Маскировка номера счета
        account = "Счет 73654108430135874305"
        masked_account = mask_account_card(account)

        print(f"Исходный счет: {account}")
        print(f"Замаскированный счет: {masked_account}")

        print()

        # Преобразует дату из ISO-формата в формат ДД.ММ.ГГГГ
        date_iso = "2026-01-21T02:26:18.671407"
        date_formated = get_date(date_iso)

        print(f"Дата ISO: {date_iso}")
        print(f"Дата отформатирована: {date_formated}")

        print()

        print("=" * 70)
        print("ДЕМОНСТРАЦИЯ МОДУЛЯ PROCESSING")
        print("=" * 70)

        print("Фильтрация операций по статусу")
        print("-" * 70)

        # Фильтрация выполненных операций
        executed_ops = filter_by_state(processing_operations, state="EXECUTED")
        print(f"Всего операций: {len(processing_operations)}")
        print(f"Выполненных операций (EXECUTED): {len(executed_ops)}")
        print("Список выполненных операций:")
        for op in executed_ops:
            formatted_date = get_date(op["date"])
            print(f"  • ID: {op['id']}, Дата: {formatted_date}, Статус: {op['state']}")

        # Сортировка по возрастанию (сначала старые)
        sorted_asc = sort_by_date(processing_operations, reverse=False)
        print("Сортировка по возрастанию (от старых к новым):")
        for op in sorted_asc:
            formatted_date = get_date(op["date"])
            print(f"  • Дата: {formatted_date}, ID: {op['id']}, Статус: {op['state']}")

        print()

    except ValueError as e:
        print(f"Ошибка: {e}")


if __name__ == '__main__':
    main()
