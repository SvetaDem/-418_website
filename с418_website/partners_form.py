from bottle import route, run, request, response, template
import json
from pathlib import Path
import re
import datetime

PARTNERS_FILE = "partners.json"

def load_partners():
    """Loads partners data from a JSON file."""
    if not Path(PARTNERS_FILE).exists():
        return {"partners": []}
    try:
        with open(PARTNERS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"partners": []}

def save_partners(data):
    """Saves partners data to a JSON file."""
    with open(PARTNERS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def validate_phone(phone):
    """Validates phone number format (+XXXXXXXXXXX)."""
    pattern = re.compile(r"^\+\d\d{3}\d{3}\d{4}$")
    return pattern.match(phone) is not None, "Phone must be in format +XXXXXXXXXXX (e.g., +79872009835)"

def validate_email(email):
    """Validates email format (excludes IP addresses in domain)."""
    email_pattern = re.compile(
        r"^(?!\.)(?!.*\.\.)[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]{1,64}"
        r"(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*@"
        r"(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,63}$"
    )
    return email_pattern.match(email) is not None, "Email must be in format example@domain.com"

def validate_date(date_str):
    """Validates date format (DD-MM-YYYY, not later than the current date)."""
    try:
        date = datetime.datetime.strptime(date_str, "%d-%m-%Y")
        today = datetime.datetime.now()
        if date > today:
            return False, "Date cannot be in the future"
        return True, ""
    except ValueError:
        return False, "Date must be in format DD-MM-YYYY"

def get_partners_data():
    """Returns partners data, errors, and form data."""
    errors = []
    form_data = {"name": "", "description": "", "phone": "", "email": "", "date": ""}
    partners = load_partners()["partners"]

    return partners, errors, form_data

def handle_partner_submission():
    """Handles partner form submission."""
    errors = []
    form_data = {
        "name": request.forms.get("name", "").strip(),
        "description": request.forms.get("description", "").strip(),
        "phone": request.forms.get("phone", "").strip(),
        "date": request.forms.get("date", "").strip(),
        "email": request.forms.get("email", "").strip()
    }

    # Validation
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
    if form_data["email"]:
        is_valid_email, email_error = validate_email(form_data["email"])
        if not is_valid_email:
            errors.append(email_error)

    if not errors:
        data = load_partners()
        data["partners"].append({
            "name": form_data["name"],
            "description": form_data["description"],
            "phone": form_data["phone"],
            "date": form_data["date"],
            "email": form_data["email"] if form_data["email"] else None
        })
        data["partners"].sort(key=lambda x: x["date"], reverse=True)
        save_partners(data)
        form_data = {"name": "", "description": "", "phone": "", "date": "", "email": ""}

    return errors, form_data