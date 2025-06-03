# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta
import re
import os
from bottle import request, response
from urllib.parse import quote, unquote

# Файл для хранения песен в формате JSON
SONGS_FILE = 'songs.json'

# Список запрещённых слов для проверки на нецензурность
PROFANITY_LIST = [
    "damn", "hell", "shit", "fuck", "bitch", "asshole", "crap", "piss", "dick", "cock",
    "bastard", "slut", "whore", "faggot", "nigger", "chink", "kike", "spic", "retard", "cunt"
]

# Инициализация файла songs.json, если он не существует
def init_songs_file():
    """Создаёт пустой файл songs.json, если он отсутствует."""
    if not os.path.exists(SONGS_FILE):
        with open(SONGS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

# Загрузка песен из файла songs.json
def load_songs():
    """Читает данные песен из файла songs.json."""
    init_songs_file()
    try:
        with open(SONGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Error: songs.json file is corrupted, returning an empty list")
        return []

# Сохранение песен в файл songs.json
def save_songs(songs):
    """Записывает список песен в файл songs.json."""
    try:
        with open(SONGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(songs, f, indent=4, ensure_ascii=False)
    except Exception as e:
        raise ValueError(f"Failed to save songs: {str(e)}")

# Проверка на повторяющиеся символы
def has_repeated_chars(s):
    """Проверяет наличие 4 или более одинаковых символов подряд."""
    pattern = r'(.)\1{3,}'
    return bool(re.search(pattern, s))

# Проверка минимального количества слов
def has_minimum_words(text, min_words=3):
    """Проверяет, что текст содержит минимум указанное количество слов."""
    words = [word for word in text.split() if word]
    return len(words) >= min_words

# Проверка наличия значимых слов
def has_meaningful_words(text):
    """Проверяет наличие хотя бы одного значимого слова (4+ буквы, без повторов)."""
    words = [word for word in text.split() if word]
    for word in words:
        if len(word) >= 4 and re.match(r'^[a-zA-Z]+$', word) and not has_repeated_chars(word):
            return True
    return False

# Проверка наличия эмодзи
def contains_emoji(text):
    """Проверяет наличие эмодзи в тексте."""
    emoji_pattern = r'[\U0001F300-\U0001F9FF\U0001F000-\U0001F02F\U0001F0A0-\U0001F0FF\U0001F680-\U0001F6FF]'
    return bool(re.search(emoji_pattern, text))

# Проверка формата и корректности даты
def is_valid_date(date_str):
    """Проверяет, что дата соответствует формату DD.MM.YYYY и является валидной."""
    pattern = r'^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.\d{4}$'
    if not re.match(pattern, date_str):
        return False
    try:
        datetime.strptime(date_str, '%d.%m.%Y')
        return True
    except ValueError:
        return False

# Проверка диапазона дат
def is_valid_date_range(date_str):
    """Проверяет, что дата не раньше сегодняшнего дня и не позже 10 лет от текущей даты."""
    try:
        input_date = datetime.strptime(date_str, '%d.%m.%Y').date()
        current_date = datetime.now().date()
        max_date = current_date + timedelta(days=365 * 10)  # 10 years
        if input_date < current_date:
            return False, "Date cannot be earlier than today."
        if input_date > max_date:
            return False, "Date cannot be more than 10 years from today."
        return True, ""
    except ValueError:
        return False, "Invalid date."

# Проверка валидности имени автора
def is_valid_author(author):
    """Проверяет, что имя автора соответствует требованиям (3-50 символов, только английский)."""
    pattern = r'^[a-zA-Z][a-zA-Z0-9\s\-_]{1,48}[a-zA-Z0-9]$'
    if not re.match(pattern, author):
        return False
    if re.search(r'[\u0400-\u04FF\u0600-\u06FF\u4E00-\U0001FFFF]', author):
        return False
    if re.match(r'^\d+$', author):
        return False
    if has_repeated_chars(author):
        return False
    if re.search(r'\s{2,}', author):
        return False
    return True

# Проверка валидности описания
def is_valid_description(description):
    """Проверяет, что описание соответствует требованиям (10-1000 символов, только английский, без HTML)."""
    if len(description) < 10 or len(description) > 1000:
        return False
    if description.lower() == request.forms.getunicode('author', '').strip().lower():
        return False  # Description must not match the author name
    html_pattern = (
        r'<(script|style|iframe|object|embed|form|input|button|textarea|meta|link|base|body|html|head)\b'
        r'|<[^>]+(on\w+)=|javascript:'
    )
    if re.search(html_pattern, description, re.IGNORECASE):
        return False
    if re.search(r'[\u0400-\u04FF\u0600-\u06FF\u4E00-\U0001FFFF]', description):
        return False
    if contains_emoji(description):
        return False
    if re.search(r'[\x00-\x08\x0B\x0C\x0E-\x1F]', description):
        return False
    if re.search(r'\s{3,}', description):
        return False
    if not has_minimum_words(description, min_words=3):
        return False
    if not has_meaningful_words(description):
        return False
    pattern = r'^[a-zA-Z0-9\s\-.,!?:;\'"()]+$'
    return bool(re.match(pattern, description))

# Проверка на наличие нецензурных слов
def contains_profanity(text):
    """Проверяет наличие запрещённых слов в тексте."""
    text_lower = text.lower()
    for word in PROFANITY_LIST:
        if re.search(rf'\b{word}\b', text_lower):
            return True
    return False

# Получение данных песен с фильтрацией
def get_songs_data():
    """Получает список песен, ошибки и данные формы с учётом фильтрации."""
    songs = load_songs()
    current_date = datetime.now().date()
    
    # Фильтрация песен с датами до текущего дня
    songs = [song for song in songs if datetime.strptime(song['date'], '%d.%m.%Y').date() >= current_date]
    
    filter_type = request.query.getunicode('filter', 'recent')
    
    try:
        if filter_type == 'recent':
            # Сортировка по ближайшим к текущей дате (сначала самые недавние)
            songs.sort(key=lambda x: (datetime.strptime(x['date'], '%d.%m.%Y').date() - current_date).days)
        elif filter_type == 'older':
            # Сортировка по наиболее далёким от текущей даты (сначала будущие)
            songs.sort(key=lambda x: (datetime.strptime(x['date'], '%d.%m.%Y').date() - current_date).days, reverse=True)
        else:
            # По умолчанию: сортировка по дате, сначала новые
            songs.sort(key=lambda x: datetime.strptime(x['date'], '%d.%m.%Y'), reverse=True)
    except (KeyError, ValueError):
        print("Warning: skipping sorting due to invalid date format")

    errors = request.query.getunicode('errors', '').split('|') if request.query.getunicode('errors') else []
    form_data = {
        'author': unquote(request.query.getunicode('author', '')),
        'description': unquote(request.query.getunicode('description', '')),
        'date': unquote(request.query.getunicode('date', ''))
    }
    return songs, errors, form_data

# Обработка отправки формы с песней
def handle_song_submission():
    """Обрабатывает отправку формы с песней, включая валидацию."""
    author = request.forms.getunicode('author', '').strip()
    description = request.forms.getunicode('description', '').strip()
    date = request.forms.getunicode('date', '').strip()

    errors = []

    # Валидация имени автора
    if not author:
        errors.append("Author/Name field is required.")
    elif not is_valid_author(author):
        errors.append("Author name must be 3-50 characters (letters, numbers, spaces, hyphens, underscores, only English, no repeats or only numbers).")
    elif contains_profanity(author):
        errors.append("Author name contains inappropriate words.")
    elif contains_emoji(author):
        errors.append("Author name cannot contain emojis.")

    # Валидация описания
    if not description:
        errors.append("Description field is required.")
    elif not is_valid_description(description):
        errors.append("Description must be 10-1000 characters, no HTML tags, only English, minimum 3 words including one meaningful word.")
    elif contains_profanity(description):
        errors.append("Description contains inappropriate words.")

    # Валидация даты
    if not date:
        errors.append("Date field is required.")
    elif not is_valid_date(date):
        errors.append("Date must be in DD.MM.YYYY format and valid (e.g., 03.06.2025).")
    else:
        is_valid, error_msg = is_valid_date_range(date)
        if not is_valid:
            errors.append(error_msg)

    # Обработка ошибок
    if errors:
        error_str = quote('|'.join(errors), safe='')
        author = quote(author, safe='')
        description = quote(description, safe='')
        date = quote(date, safe='')
        print(f"Redirecting with errors: {errors}")
        response.status = 302
        response.set_header('Location', f'/actual_new?errors={error_str}&author={author}&description={description}&date={date}')
        return

    # Добавление новой песни
    songs = load_songs()
    songs.append({
        'author': author,
        'description': description,
        'date': date
    })
    try:
        save_songs(songs)
        print("Song successfully saved")
    except ValueError as e:
        errors.append(str(e))
        error_str = quote('|'.join(errors), safe='')
        author = quote(author, safe='')
        description = quote(description, safe='')
        date = quote(date, safe='')
        print(f"Error saving song: {str(e)}")
        response.status = 302
        response.set_header('Location', f'/actual_new?errors={error_str}&author={author}&description={description}&date={date}')
        return

    # Успешное перенаправление
    print("Redirecting to /actual_new")
    response.status = 302
    response.set_header('Location', '/actual_new')