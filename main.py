import sys

from src.file_reader import get_transactions_from_csv, get_transactions_from_excel
from src.processing import filter_by_state, sort_by_date
from src.search import process_bank_search
from src.utils import get_transactions_from_json
from src.widget import get_date, mask_account_card

VALID_STATUSES = ("EXECUTED", "CANCELED", "PENDING")

# Кодировка stdin: пробуем utf-8, fallback на cp1251 (Windows/кириллица)
_STDIN_ENCODING = "utf-8"


def _detect_encoding() -> str:
    """Определяет рабочую кодировку stdin один раз при старте."""
    enc = getattr(sys.stdin, "encoding", None) or ""
    if enc.lower().replace("-", "") in ("cp1251", "cp866", "windows1251"):
        return enc
    return "utf-8"


_STDIN_ENCODING = _detect_encoding()


def _input(prompt: str = "") -> str:
    """
    Читает строку из stdin.buffer и декодирует с автоопределением кодировки.
    Если utf-8 не работает — пробует cp1251.
    """
    sys.stdout.write(prompt)
    sys.stdout.flush()
    raw = sys.stdin.buffer.readline().rstrip(b"\r\n")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("cp1251")


def _get_transaction_currency(t: dict) -> str:
    if "operationAmount" in t:
        return t["operationAmount"]["currency"]["code"]
    return t.get("currency_code", "")


def _get_transaction_amount(t: dict) -> str:
    if "operationAmount" in t:
        return t["operationAmount"]["amount"]
    return str(t.get("amount", ""))


def _format_transaction(t: dict) -> str:
    date = get_date(t.get("date", ""))
    description = t.get("description", "")
    from_acc = t.get("from", "")
    to_acc = t.get("to", "")
    amount = _get_transaction_amount(t)
    currency = _get_transaction_currency(t)

    lines = [f"{date} {description}"]

    if from_acc and to_acc:
        lines.append(f"{mask_account_card(from_acc)} -> {mask_account_card(to_acc)}")
    elif to_acc:
        lines.append(mask_account_card(to_acc))

    lines.append(f"Сумма: {amount} {currency}")
    return "\n".join(lines)


def main() -> None:
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    while True:
        choice = _input("\nПользователь: ").strip()
        if choice == "1":
            print("\nДля обработки выбран JSON-файл.")
            transactions = get_transactions_from_json("data/operations.json")
            break
        elif choice == "2":
            print("\nДля обработки выбран CSV-файл.")
            transactions = get_transactions_from_csv("data/transactions.csv")
            break
        elif choice == "3":
            print("\nДля обработки выбран XLSX-файл.")
            transactions = get_transactions_from_excel("data/transactions.xlsx")
            break
        else:
            print(f'Неверный выбор "{choice}". Введите 1, 2 или 3.')

    # Фильтрация по статусу
    print(
        "\nВведите статус, по которому необходимо выполнить фильтрацию.\n"
        f"Доступные для фильтровки статусы: {', '.join(VALID_STATUSES)}"
    )
    while True:
        status_input = _input("\nПользователь: ").strip().upper()
        if status_input in VALID_STATUSES:
            print(f'\nОперации отфильтрованы по статусу "{status_input}"')
            transactions = filter_by_state(transactions, state=status_input)
            break
        else:
            print(f'Статус операции "{status_input}" недоступен.')
            print(
                "\nВведите статус, по которому необходимо выполнить фильтрацию.\n"
                f"Доступные для фильтровки статусы: {', '.join(VALID_STATUSES)}"
            )

    # Сортировка по дате
    print("\nОтсортировать операции по дате? Да/Нет")
    sort_answer = _input("Пользователь: ").strip().lower()
    if sort_answer == "да":
        print("\nОтсортировать по возрастанию или по убыванию? (1 - по возрастанию / 2 - по убыванию)")
        while True:
            order_answer = _input("Пользователь: ").strip()
            if order_answer == "1":
                reverse = False
                break
            elif order_answer == "2":
                reverse = True
                break
            else:
                print("Введите 1 (по возрастанию) или 2 (по убыванию).")
        transactions = sort_by_date(transactions, reverse=reverse)

    # Фильтрация по рублям
    print("\nВыводить только рублевые транзакции? Да/Нет")
    rub_answer = _input("Пользователь: ").strip().lower()
    if rub_answer == "да":
        transactions = [t for t in transactions if _get_transaction_currency(t) == "RUB"]

    # Фильтрация по слову в описании
    print("\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет")
    search_answer = _input("Пользователь: ").strip().lower()
    if search_answer == "да":
        search_word = _input("Введите слово для поиска: ").strip()
        transactions = process_bank_search(transactions, search_word)

    # Вывод результата
    print("\nРаспечатываю итоговый список транзакций...")

    if not transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"\nВсего банковских операций в выборке: {len(transactions)}\n")
    for t in transactions:
        print(_format_transaction(t))
        print()


if __name__ == "__main__":
    main()
