from unittest.mock import MagicMock, patch

from src.decorators import log
from src.external_api import convert_transaction_amount
from src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)
from src.processing import filter_by_state, sort_by_date
from src.utils import get_transactions_from_json
from src.widget import get_date, mask_account_card


def main():
    # Тестовые данные для processing
    processing_operations = [
        {"id": 414288290, "state": "EXECUTED", "date": "2019-07-03T18:35:29.051309"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 142264268, "state": "EXECUTED", "date": "2019-04-04T23:20:05.206878"},
    ]

    # Тестовые данные для generators (с валютами)
    generator_transactions = [
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
    ]

    try:
        print("=" * 70)
        print("ДЕМОНСТРАЦИЯ МОДУЛЯ WIDGET")
        print("=" * 70)
        print()

        card = "Visa Platinum 7000792289606361"
        masked_card = mask_account_card(card)
        print(f"Исходная карта:        {card}")
        print(f"Замаскированная карта: {masked_card}")
        print()

        account = "Счет 73654108430135874305"
        masked_account = mask_account_card(account)
        print(f"Исходный счет:         {account}")
        print(f"Замаскированный счет:  {masked_account}")
        print()

        date_iso = "2026-01-21T02:26:18.671407"
        date_formatted = get_date(date_iso)
        print(f"Дата ISO:              {date_iso}")
        print(f"Дата отформатирована:  {date_formatted}")
        print()

        print("=" * 70)
        print("ДЕМОНСТРАЦИЯ МОДУЛЯ PROCESSING")
        print("=" * 70)
        print()
        print("📋 Фильтрация операций по статусу")
        print("-" * 70)

        executed_ops = filter_by_state(processing_operations, state="EXECUTED")
        print(f"Всего операций: {len(processing_operations)}")
        print(f"Выполненных операций (EXECUTED): {len(executed_ops)}")
        print()
        print("Список выполненных операций:")
        for op in executed_ops:
            formatted_date = get_date(op["date"])
            print(f"  • ID: {op['id']}, Дата: {formatted_date}, Статус: {op['state']}")
        print()

        print("📅 Сортировка операций по дате")
        print("-" * 70)
        sorted_asc = sort_by_date(processing_operations, reverse=False)
        print("Сортировка по возрастанию (от старых к новым):")
        for op in sorted_asc:
            formatted_date = get_date(op["date"])
            print(f"  • Дата: {formatted_date}, ID: {op['id']}, Статус: {op['state']}")
        print()

        print("=" * 70)
        print("ДЕМОНСТРАЦИЯ МОДУЛЯ GENERATORS")
        print("=" * 70)
        print()
        print("💱 Фильтрация транзакций по валюте (USD)")
        print("-" * 70)

        usd_transactions = filter_by_currency(generator_transactions, "USD")
        usd_list = list(usd_transactions)
        print(f"Найдено USD-транзакций: {len(usd_list)}")
        for t in usd_list:
            amount = t["operationAmount"]["amount"]
            currency = t["operationAmount"]["currency"]["code"]
            print(f"  • ID: {t['id']}, Сумма: {amount} {currency}")
        print()

        print("📝 Генератор описаний транзакций")
        print("-" * 70)
        descriptions = transaction_descriptions(generator_transactions)
        print("Описания операций:")
        for i, desc in enumerate(descriptions, 1):
            print(f"  {i}. {desc}")
        print()

        print("💳 Генератор номеров банковских карт (1-5)")
        print("-" * 70)
        for card_num in card_number_generator(1, 5):
            print(f"  {card_num}")
        print()

        print("=" * 70)
        print("ДЕМОНСТРАЦИЯ МОДУЛЯ DECORATORS")
        print("=" * 70)
        print()

        @log()
        def transfer_money(amount, from_account, to_account):
            """Перевод денег между счетами (логирование в консоль)."""
            return f"Переведено {amount} руб. с {from_account} на {to_account}"

        @log(filename="operations.log")
        def calculate_commission(amount, rate=0.01):
            """Расчёт комиссии (логирование в файл)."""
            return amount * rate

        @log()
        def risky_operation(value):
            """Операция с возможной ошибкой."""
            if value == 0:
                raise ValueError("Значение не может быть нулевым")
            return 100 / value

        print("📝 Логирование в консоль")
        print("-" * 70)
        print("Вызов функции transfer_money(1000, 'Счет1', 'Счет2'):")
        result = transfer_money(1000, "Счет1", "Счет2")
        print(f"Результат: {result}")
        print()

        print("📁 Логирование в файл (operations.log)")
        print("-" * 70)
        print("Вызов функции calculate_commission(5000, 0.015):")
        commission = calculate_commission(5000, 0.015)
        print(f"Комиссия: {commission} руб.")
        print("(Логи записаны в /log/operations.log)")
        print()

        print("⚠️ Логирование ошибки")
        print("-" * 70)
        print("Вызов функции risky_operation(10) — успешно:")
        result_ok = risky_operation(10)
        print(f"Результат: {result_ok}")
        print()

        print("Вызов функции risky_operation(0) — с ошибкой:")
        try:
            risky_operation(0)
        except ValueError as e:
            print(f"Поймана ошибка: {e}")
        print()

        # ---------------------------------------------------------------
        print("=" * 70)
        print("ДЕМОНСТРАЦИЯ МОДУЛЯ UTILS")
        print("=" * 70)
        print()
        print("📂 Чтение транзакций из JSON-файла")
        print("-" * 70)

        transactions = get_transactions_from_json("data/operations.json")
        print(f"Загружено транзакций из data/operations.json: {len(transactions)}")
        for t in transactions:
            amount = t["operationAmount"]["amount"]
            code = t["operationAmount"]["currency"]["code"]
            date = get_date(t["date"])
            print(f"  • ID: {t['id']}, Дата: {date}, Сумма: {amount} {code}, Статус: {t['state']}")
        print()

        # ---------------------------------------------------------------
        print("=" * 70)
        print("ДЕМОНСТРАЦИЯ МОДУЛЯ EXTERNAL_API")
        print("=" * 70)
        print()
        print("💱 Конвертация суммы транзакции в рубли")
        print("-" * 70)

        # Ищем транзакции по валюте, не полагаясь на порядок в файле
        rub_t = next(
            (t for t in transactions if t["operationAmount"]["currency"]["code"] == "RUB"),
            None,
        )
        usd_t = next(
            (t for t in transactions if t["operationAmount"]["currency"]["code"] == "USD"),
            None,
        )

        if rub_t:
            rub_amount = convert_transaction_amount(rub_t)
            print(
                f"RUB-транзакция ID {rub_t['id']}: "
                f"{rub_t['operationAmount']['amount']} RUB → {rub_amount:.2f} руб. "
                f"(конвертация не нужна)"
            )
        else:
            print("RUB-транзакций в файле не найдено")
        print()

        # USD/EUR конвертация с мок-ответом API
        if usd_t:
            original_amount = float(usd_t["operationAmount"]["amount"])
            mocked_rub_result = round(original_amount * 91.5, 2)  # условный курс для демо

            mock_api_response = MagicMock()
            mock_api_response.json.return_value = {"success": True, "result": mocked_rub_result}
            mock_api_response.raise_for_status = MagicMock()

            with patch("src.external_api.requests.get", return_value=mock_api_response):
                with patch("src.external_api.EXCHANGE_RATES_API_KEY", "demo_key"):
                    usd_amount = convert_transaction_amount(usd_t)

            print(
                f"USD-транзакция ID {usd_t['id']}: "
                f"{usd_t['operationAmount']['amount']} USD → {usd_amount:,.2f} руб. "
                f"(мок API, курс ~91.5)"
            )
        else:
            print("USD-транзакций в файле не найдено")
        print()

        print("=" * 70)
        print("✅ Демонстрация завершена")
        print("=" * 70)

    except ValueError as e:
        print(f"❌ Ошибка: {e}")
    except Exception as e:
        print(f"❌ Непредвиденная ошибка: {e}")

if __name__ == "__main__":
    main()
