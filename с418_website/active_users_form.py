from bottle import route, run, request, response, template
import json
from datetime import datetime

DATA_FILE = "users.json"

def load_users():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            users = json.load(f)
    except:
        users = {}

    users_list = [
        {
            "username": username,
            **info
        } for username, info in users.items()
    ]

    users_list.sort(
        key=lambda x: datetime.strptime(x["add_date"], "%d.%m.%Y %H:%M:%S"),
        reverse=True
    )
    return users_list

def save_users(users_dict):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users_dict, f, indent=2)

@route("/active_users", method="POST")
def active_users():
    error = ""
    username = request.forms.get("username").strip()
    description = request.forms.get("description").strip()
    date = request.forms.get("date").strip()
    phone = request.forms.get("telephone").strip()

    if not username or not description or not date:
        error = "All fields are required."
    else:
        try:
            datetime.strptime(date, "%d.%m.%Y")
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
                response.content_type = 'application/json'
                return json.dumps({"success": True})
        except ValueError:
            error = "The date should be in the format dd.mm.yyyy."

    response.status = 400
    response.content_type = 'application/json'
    return json.dumps({"error": error})

@route("/active_users", method="GET")
def active_users_get():
    users = load_users()

    users_list = [
        {
            "username": username,
            **info
        } for username, info in users.items()
    ]

    users_list.sort(
        key=lambda x: datetime.strptime(x["add_date"], "%d.%m.%Y %H:%M:%S"),
        reverse=True
    )

    return template("active_users", users=users_list, title="Active Users", year=datetime.now().year)
