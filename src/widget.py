from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(payment_info: str) -> str:
    """
    Маскирует номер карты или счёта в строке описания платежа.

    Входные строки и ожидаемый результат:
    "Visa Platinum 7000792289606361"     → "Visa Platinum 7000 79** **** 6361"
    "Maestro 7000792289606361"           → "Maestro 7000 79** **** 6361"
    "Счет 73654108430135874305"          → "Счет **4305"
    """
    parts = payment_info.strip().split(" ")
    if len(parts) < 2:
        raise ValueError(f"Некорректный формат строки {payment_info}")

    # Последняя часть — это номер (карты или счёта)
    number = parts[-1]

    # Всё до номера — описание (может быть несколько слов)
    description = " ".join(parts[:-1])

    if description.lower() == "счет":
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{description} {masked_number}"


def get_date(date_str: str) -> str:
    """
    Преобразует дату из ISO-формата в формат ДД.ММ.ГГГГ

    Пример:
        "2024-03-11T02:26:18.671407" → "11.03.2024"

    Поддерживает как полные ISO-строки (с временем), так и просто дату "2024-03-11".
    """
    try:
        # datetime.fromisoformat понимает и "2024-03-11", и полную строку с временем
        dt = datetime.fromisoformat(date_str)
        return dt.strftime("%d.%m.%Y")
    except ValueError as e:
        raise ValueError(f"Некорректный формат даты: {date_str}") from e
