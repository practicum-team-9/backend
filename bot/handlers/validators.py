import re
from datetime import datetime


def validate_phone_format(phone: str) -> bool:
    """Валидация телефона."""
    if not phone or not phone.strip():
        return False
    phone = phone.strip()
    return bool(re.match(r'^[78]\d{10}$', phone))


def validate_email_format(email: str) -> bool:
    """Валидация email."""
    if not email or not email.strip():
        return False
    email = email.strip()
    return bool(
        re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
    )


def validate_date_format(date: str) -> bool:
    """Валидация формата даты."""
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False
