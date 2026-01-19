from src.masks import get_mask_card_number, get_mask_account

# Маскировка номера карты
card = "7000792289606361"
masked_card = get_mask_card_number(card)
print(masked_card)  # Вывод: 7000 79** **** 6361


# Маскировка номера счета
account = "73654108430135874305"
masked_account = get_mask_account(account)
print(masked_account)  # Вывод: **4305
