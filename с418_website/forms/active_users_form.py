from bottle import route, run, request, response, template
import json
from datetime import datetime
from forms.valid_phone import is_valid_phone
import re

# Файл, в котором хранятся данные пользователей
DATA_FILE = "users.json"

# Функция для преобразования строки с датой в объект datetime
def parse_date(date_str):
    return datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S")

# Функция загрузки пользователей из файла и сортировка по дате добавления
def load_users():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            users = json.load(f)

        # Сортируем пользователей по add_date
        sorted_users = dict(sorted(users.items(), key=lambda item: parse_date(item[1]["add_date"]), reverse=True))

        return sorted_users
    except:
        # Если файл не найден или повреждён — возвращаем пустой словарь
        return {}

# Функция сохранения пользователей в файл
def save_users(users_dict):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users_dict, f, indent=2, ensure_ascii=False)

# Обработчик POST-запроса на добавление активного пользователя
@route("/active_users", method="POST")
def active_users_post():
    error = ""

    # Получаем данные из формы
    username = request.forms.get("username").strip()
    description = request.forms.get("description").strip()
    date = request.forms.get("date").strip()
    phone = request.forms.get("telephone").strip()

    # Проверка: все поля должны быть заполнены
    if not username or not description or not date or not phone:
        error = "All fields are required."
    # Проверка имени: начинается с буквы и содержит минимум 2 буквы
    elif not re.fullmatch(r'[A-Za-z][^./\\|,)(]{1,}', username):
        error = "The username must begin with a letter, contain at least 2 characters, and not include . / \\ | , ) ("

    # Проверка описания: минимум 3 буквы
    elif len(re.findall(r'[A-Za-z]', description)) < 3:
        error = "The description must contain at least 3 latin letters." 
   
    else:
        try:
            # Проверка формата даты рождения
            birth_date = datetime.strptime(date, "%d.%m.%Y")
            # Проверка, что дата не может быть в будущем
            if birth_date > datetime.now():
                error = "Birthday cannot be in the future."
            # Проверка, что дата рождения не менее 1900
            elif birth_date.year < 1900:
                error = "Birth year cannot be earlier than 1900."
        except ValueError:
            error = "Invalid date or format. Please use dd.mm.yyyy and make sure the date exists."

    # Проверка телефона (после успешной проверки даты)
    if not error and not is_valid_phone(phone):
        error = "Phone number must be in the format +7(xxx)xxx-xx-xx."

    # Если ошибок нет — сохраняем пользователя
    if not error:
        # Загружаем всех пользователей
        users = load_users()

        # Проверка: пользователь с таким именем уже существует
        if username in users:
            error = "The user already exists."
        else:
            # Добавляем нового пользователя с текущей датой и временем
            users[username] = {
                "description": description,
                "birthday": date,
                "telephone": phone,
                "add_date": datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            }

            # Сохраняем изменения
            save_users(users)

            # Успешный ответ
            response.content_type = "application/json"
            return json.dumps({"success": True})

    # Отправляем ошибку
    response.status = 400
    response.content_type = "application/json"
    return json.dumps({"error": error})
