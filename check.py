from src.widget import mask_account_card, get_date

print(mask_account_card("Maestro 1596837868705199"))  # Maestro 1596 83** **** 5199
print(mask_account_card("Счет 64686473678894779589"))  # Счет **9589
print(mask_account_card("Visa Classic 6831982476737658"))  # Visa Classic 6831 98** **** 7658
print(mask_account_card("Просто строка"))  # Некорректный ввод
print(get_date("2024-03-11T02:26:18.671407"))  # 11.03.2024
