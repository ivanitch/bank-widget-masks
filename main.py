from src.decorators import log
from src.external_api import convert_transaction_amount
from src.generators import card_number_generator, filter_by_currency, transaction_descriptions
from src.processing import filter_by_state, sort_by_date
from src.utils import get_transactions_from_json
from src.widget import get_date, mask_account_card


def main() -> None:
    processing_operations = [
        {"id": 414288290, "state": "EXECUTED", "date": "2019-07-03T18:35:29.051309"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 142264268, "state": "EXECUTED", "date": "2019-04-04T23:20:05.206878"},
    ]

    generator_transactions = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]

    print("=" * 70)
    print("МОДУЛЬ WIDGET")
    print("=" * 70)

    card = "Visa Platinum 7000792289606361"
    print(f"Исходная карта:        {card}")
    print(f"Замаскированная карта: {mask_account_card(card)}")

    account = "Счет 73654108430135874305"
    print(f"Исходный счет:         {account}")
    print(f"Замаскированный счет:  {mask_account_card(account)}")

    date_iso = "2026-01-21T02:26:18.671407"
    print(f"Дата ISO:              {date_iso}")
    print(f"Дата отформатирована:  {get_date(date_iso)}")

    print()
    print("=" * 70)
    print("МОДУЛЬ PROCESSING")
    print("=" * 70)

    executed_ops = filter_by_state(processing_operations, state="EXECUTED")
    print(f"Всего операций: {len(processing_operations)}, выполненных (EXECUTED): {len(executed_ops)}")

    print("\nСортировка по возрастанию:")
    for op in sort_by_date(processing_operations, reverse=False):
        print(f"  Дата: {get_date(op['date'])}, ID: {op['id']}, Статус: {op['state']}")

    print()
    print("=" * 70)
    print("МОДУЛЬ GENERATORS")
    print("=" * 70)

    usd_list = list(filter_by_currency(generator_transactions, "USD"))
    print(f"USD-транзакций: {len(usd_list)}")
    for t in usd_list:
        print(f"  ID: {t['id']}, Сумма: {t['operationAmount']['amount']} USD")

    print("\nОписания транзакций:")
    for i, desc in enumerate(transaction_descriptions(generator_transactions), 1):
        print(f"  {i}. {desc}")

    print("\nНомера карт (1-5):")
    for card_num in card_number_generator(1, 5):
        print(f"  {card_num}")

    print()
    print("=" * 70)
    print("МОДУЛЬ DECORATORS")
    print("=" * 70)

    @log()
    def transfer_money(amount: float, from_account: str, to_account: str) -> str:
        return f"Переведено {amount} руб. с {from_account} на {to_account}"

    @log(filename="operations.log")
    def calculate_commission(amount: float, rate: float = 0.01) -> float:
        return amount * rate

    @log()
    def risky_operation(value: float) -> float:
        if value == 0:
            raise ValueError("Значение не может быть нулевым")
        return 100 / value

    print("Логирование в консоль:")
    result = transfer_money(1000, "Счет1", "Счет2")
    print(f"  Результат: {result}")

    print("\nЛогирование в файл (logs/operations.log):")
    commission = calculate_commission(5000, 0.015)
    print(f"  Комиссия: {commission} руб.")

    print("\nУспешный вызов risky_operation(10):")
    print(f"  Результат: {risky_operation(10)}")

    print("\nВызов risky_operation(0) с ошибкой:")
    try:
        risky_operation(0)
    except ValueError as e:
        print(f"  Поймана ошибка: {e}")

    print()
    print("=" * 70)
    print("МОДУЛЬ UTILS")
    print("=" * 70)

    transactions = get_transactions_from_json("data/operations.json")
    print(f"Загружено транзакций из data/operations.json: {len(transactions)}")
    for t in transactions:
        print(
            f"  ID: {t['id']}, Дата: {get_date(t['date'])}, "
            f"Сумма: {t['operationAmount']['amount']} {t['operationAmount']['currency']['code']}, "
            f"Статус: {t['state']}"
        )

    print()
    print("=" * 70)
    print("МОДУЛЬ EXTERNAL_API")
    print("=" * 70)

    rub_t = next(
        (t for t in transactions if t["operationAmount"]["currency"]["code"] == "RUB"), None
    )
    usd_t = next(
        (t for t in transactions if t["operationAmount"]["currency"]["code"] == "USD"), None
    )

    if rub_t:
        rub_amount = convert_transaction_amount(rub_t)
        print(
            f"RUB ID {rub_t['id']}: {rub_t['operationAmount']['amount']} RUB "
            f"-> {rub_amount:.2f} руб. (конвертация не нужна)"
        )

    if usd_t:
        usd_amount = convert_transaction_amount(usd_t)
        print(
            f"USD ID {usd_t['id']}: {usd_t['operationAmount']['amount']} USD "
            f"-> {usd_amount:.2f} руб."
        )

    print()
    print("=" * 70)
    print("Демонстрация завершена")
    print("=" * 70)


if __name__ == "__main__":
    main()
