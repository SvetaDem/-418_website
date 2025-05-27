import re

# Регулярное выражение для проверки email
phone_pattern = r"^\+7\(\d{3}\)\d{3}-\d{2}-\d{2}$"


# Функция проверки phone
def is_valid_phone(phone: str) -> bool:
    return bool(re.fullmatch(phone_pattern, phone))