import json
from pathlib import Path
import re
import datetime

PARTNERS_FILE = "partners.json"

def load_partners():
    """Загружает данные партнёров из JSON файла."""
    if not Path(PARTNERS_FILE).exists():
        return {"partners": []}
    try:
        with open(PARTNERS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"partners": []}

def save_partners(data):
    """Сохраняет данные партнёров в JSON файл."""
    with open(PARTNERS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def validate_phone(phone):
    """Валидация телефона (+X-XXX-XXX-XXXX)."""
    pattern = re.compile(r"^\+\d-\d{3}-\d{3}-\d{4}$")
    return pattern.match(phone) is not None, "Phone must be in format +X-XXX-XXX-XXXX (e.g., +1-123-456-7890)"

def validate_date(date_str):
    """Валидация даты (YYYY-MM-DD, не позднее текущей даты)."""
    try:
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        today = datetime.datetime.now()
        if date > today:
            return False, "Date cannot be in the future"
        return True, ""
    except ValueError:
        return False, "Date must be in format YYYY-MM-DD"

def get_partners_data():
    """Возвращает данные партнёров, ошибки и данные формы."""
    errors = []
    form_data = {"name": "", "description": "", "phone": "", "date": ""}
    partners = load_partners()["partners"]

    return partners, errors, form_data

def handle_partner_submission():
    """Обработка отправки формы партнёра."""
    errors = []
    form_data = {
        "name": request.forms.get("name", "").strip(),
        "description": request.forms.get("description", "").strip(),
        "phone": request.forms.get("phone", "").strip(),
        "date": request.forms.get("date", "").strip()
    }

    # Валидация
    if not form_data["name"]:
        errors.append("Company name is required")
    if not form_data["description"]:
        errors.append("Description is required")
    if not form_data["phone"]:
        errors.append("Phone is required")
    else:
        is_valid_phone, phone_error = validate_phone(form_data["phone"])
        if not is_valid_phone:
            errors.append(phone_error)
    if not form_data["date"]:
        errors.append("Date is required")
    else:
        is_valid_date, date_error = validate_date(form_data["date"])
        if not is_valid_date:
            errors.append(date_error)

    if not errors:
        data = load_partners()
        data["partners"].append({
            "name": form_data["name"],
            "description": form_data["description"],
            "phone": form_data["phone"],
            "date": form_data["date"]
        })
        data["partners"].sort(key=lambda x: x["date"], reverse=True)
        save_partners(data)
        form_data = {"name": "", "description": "", "phone": "", "date": ""}

    return errors, form_data