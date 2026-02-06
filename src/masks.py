"""
Модуль для маскировки конфиденциальных банковских данных.

Содержит функции для безопасного отображения номеров банковских карт
и счетов, скрывая часть цифр для защиты конфиденциальной информации.
"""


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты, оставляя видимыми первые 6 и последние 4 цифры.

    Функция принимает номер карты в виде строки цифр и возвращает замаскированный номер
    в формате: XXXX XX** **** XXXX, где X - видимые цифры, * - скрытые цифры.

    Аргументы:
        card_number (str): Номер банковской карты (16 цифр без пробелов).
                           Пример: "7000792289606361"

    Возвращает:
        str: Замаскированный номер карты в формате "XXXX XX** **** XXXX".
             Пример: "7000 79** **** 6361"

    Пример:
        >>> get_mask_card_number("7000792289606361")
    """
    str_cart_number = str(card_number)
    clean_number = str_cart_number.replace(" ", "")

    if not clean_number or not str(clean_number):
        raise ValueError("Номер карты отсутствует или пуст")

    if len(clean_number) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")

    if not clean_number.isdigit():
        raise ValueError("Номер карты должен содержать только цифры")

    first_block = clean_number[:4]  # Первые 4 цифры: "7000"
    second_partial = clean_number[4:6]  # Следующие 2 цифры: "79"
    last_block = clean_number[-4:]  # Последние 4 цифры: "6361"

    return f"{first_block} {second_partial}** **** {last_block}"


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета, оставляя видимыми только последние 4 цифры.

    Функция принимает номер счета в виде строки цифр и возвращает замаскированный номер
    в формате: **XXXX, где X - последние 4 видимые цифры, * - скрытые цифры.

    Аргументы:
        account_number (str): Номер банковского счета (обычно 20 цифр).
                              Пример: "73654108430135874305"

    Возвращает:
        str: Замаскированный номер счета в формате "**XXXX".
             Пример: "**4305"

    Примеры:
        >>> get_mask_account("73654108430135874305")

    Примечания:
        - Функция работает с номерами счетов любой длины >= 4 цифр
        - Всегда скрывает все цифры, кроме последних 4
        - Две звездочки показывают наличие скрытых цифр
    """
    str_account_number = str(account_number)
    clean_number = str_account_number.replace(" ", "")

    if not clean_number or not str(clean_number):
        raise ValueError("Номер счета отсутствует или пуст")

    if len(clean_number) < 4:
        raise ValueError("Номер счета должен содержать минимум 4 цифры")

    if not clean_number.isdigit():
        raise ValueError("Номер счета должен содержать только цифры")

    # Извлекаем последние 4 цифры
    last_four = clean_number[-4:]

    return f"**{last_four}"
