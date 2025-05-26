import re
import datetime
from bottle import request
from pathlib import Path
import json

PARTNERS_FILE = "partners.json"

def load_partners():
    """Loads partners data from a JSON file."""
    if not Path(PARTNERS_FILE).exists():
        return {"partners": []}
    try:
        with open(PARTNERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"partners": []}

def save_partners(data):
    """Saves partners data to a JSON file."""
    with open(PARTNERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def validate_phone(phone):
    """Validates phone number format (+7XXXXXXXXXXX)."""
    pattern = re.compile(r"^\+\d{12}$")
    return pattern.match(phone) is not None, "Phone must be in format +7XXXXXXXXXXX (e.g., +71234567890)"

def validate_date(date_str):
    """Validates date format (DD-MM-YYYY, not later than the current date, not earlier than 01-01-2000)."""
    try:
        date = datetime.datetime.strptime(date_str, "%d-%m-%Y")
        today = datetime.datetime.now()
        min_date = datetime.datetime.strptime("01-01-2000", "%d-%m-%Y")
        
        if date > today:
            return False, "Date cannot be in the future"
        if date < min_date:
            return False, "Date cannot be earlier than 01-01-2000"
        return True, ""
    except ValueError:
        return False, "Date must be in format DD-MM-YYYY (e.g., 20-05-2025)"


def validate_email(email):
    """Validates email format."""
    email_pattern = re.compile(
        r"^(?!\.)(?!.*\.\.)[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]{1,64}"
        r"(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*@"
        r"(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,63}$"
    )
    return email_pattern.match(email) is not None, "Email must be in format example@domain.com (no IP addresses)"

def validate_name(name):
    """Validates company name length (2 to 50 characters)."""
    if len(name) < 2:
        return False, "Company name must be at least 2 characters long"
    if len(name) > 50:
        return False, "Company name must not exceed 50 characters"
    return True, ""

def validate_description(description):
    """Validates description length (3 to 200 characters)."""
    if len(description) < 3:
        return False, "Description must be at least 3 characters long"
    if len(description) > 200:
        return False, "Description must not exceed 200 characters"
    return True, ""

def get_partners_data():
    """Returns partners data, errors, form data, and context variables."""
    errors = []
    form_data = {"name": "", "description": "", "phone": "", "email": "", "date": ""}
    partners = load_partners()["partners"]
    total_partners = len(partners) if partners else 0
    return partners, errors, form_data, total_partners

def handle_partner_submission():
    """Handles partner form submission and returns context variables."""
    errors = []
    success_message = ""
    form_data = {
        "name": request.forms.get("name", "").strip(),
        "description": request.forms.get("description", "").strip(),
        "phone": request.forms.get("phone", "").strip(),
        "email": request.forms.get("email", "").strip(),
        "date": request.forms.get("date", "").strip()
    }

    # Validation
    if not form_data["name"]:
        errors.append("Company name is required")
    else:
        is_valid_name, name_error = validate_name(form_data["name"])
        if not is_valid_name:
            errors.append(name_error)
        partners = load_partners()["partners"]
        if any(partner["name"].lower() == form_data["name"].lower() for partner in partners):
            errors.append("A partner with this name already exists")

    if not form_data["description"]:
        errors.append("Description is required")
    else:
        is_valid_desc, desc_error = validate_description(form_data["description"])
        if not is_valid_desc:
            errors.append(desc_error)

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
            "email": form_data["email"] if form_data["email"] else None,
            "date": form_data["date"]
        })
        data["partners"].sort(key=lambda x: x["date"], reverse=True)
        save_partners(data)
        success_message = "Partner added successfully!"
        form_data = {"name": "", "description": "", "phone": "", "date": "", "email": ""}

    return errors, form_data, success_message