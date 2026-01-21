from src.widget import get_date, mask_account_card

try:
    # Маскировка номера карты
    card = "Visa Platinum 7000792289606361"
    masked_card = mask_account_card(card)
    print(masked_card)  # Вывод: Visa Platinum 7000 79** **** 6361

    # Маскировка номера счета
    account = "Счет 73654108430135874305"
    masked_account = mask_account_card(account)
    print(masked_account)  # Вывод: Счет **4305

    # Преобразует дату из ISO-формата в формат ДД.ММ.ГГГГ
    date_iso = "2026-01-21T02:26:18.671407"
    date_formated = get_date(date_iso)
    print(date_formated)

except ValueError as e:
    print(f"Ошибка: {e}")
