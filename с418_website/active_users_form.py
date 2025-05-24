from bottle import route, run, request, response, template
import json
from datetime import datetime
from valid_phone import is_valid_phone
import re

DATA_FILE = "users.json"

def parse_date(date_str):
    return datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S")

def load_users():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            users = json.load(f)

        # Сортируем пользователей по add_date
        sorted_users = dict(sorted(users.items(), key=lambda item: parse_date(item[1]["add_date"]), reverse=True))

        return sorted_users
    except:
        return {}

def save_users(users_dict):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users_dict, f, indent=2, ensure_ascii=False)

@route("/active_users", method="POST")
def active_users_post():
    error = ""
    username = request.forms.get("username").strip()
    description = request.forms.get("description").strip()
    date = request.forms.get("date").strip()
    phone = request.forms.get("telephone").strip()

    if not username or not description or not date or not phone:
        error = "All fields are required."
    else:
        try:
            datetime.strptime(date, "%d.%m.%Y")
        except ValueError:
            error = "The date should be in the format dd.mm.yyyy."

        # Проверка имени — минимум 2 буквы
        if len(re.findall(r'[A-Za-z]', username)) < 2:
            error = "The username must contain at least 2 letters."

        # Проверка формата даты
        if not error:
            try:
                datetime.strptime(date, "%d.%m.%Y")
            except ValueError:
                error = "The date should be in the format dd.mm.yyyy."

        # Проверка описания — минимум 3 буквы
        if not error and len(re.findall(r'[A-Za-zА-Яа-я]', description)) < 3:
            error = "The description must contain at least 3 letters."

        # Проверка телефона
        if not error and not is_valid_phone(phone):
            error = "Phone number must be in the format +7(xxxx)xxx-xx-xx."

    if not error:
        users = load_users()
        if username in users:
            error = "The user already exists."
        else:
            users[username] = {
                "description": description,
                "birthday": date,
                "telephone": phone,
                "add_date": datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            }
           
            save_users(users)
            response.content_type = "application/json"
            return json.dumps({"success": True})

    response.status = 400
    response.content_type = "application/json"
    return json.dumps({"error": error})

