import json
from datetime import datetime
import re
import os
from bottle import request, response
from urllib.parse import quote, unquote

# Файл для хранения статей в формате JSON
ARTICLES_FILE = 'articles.json'

# Расширенный список нецензурных слов на английском для проверки полей
# Список охватывает распространённые оскорбления для англоязычного интерфейса
PROFANITY_LIST = [
    "damn", "hell", "shit", "fuck", "bitch", "asshole", "crap", "piss", "dick", "cock",
    "bastard", "slut", "whore", "faggot", "nigger", "chink", "kike", "spic", "retard", "cunt"
]

# Инициализация файла articles.json, если он не существует
# Создаёт пустой список статей для предотвращения ошибок при первом запуске
def init_articles_file():
    # Проверяет наличие файла в директории
    if not os.path.exists(ARTICLES_FILE):
        # Открывает файл в режиме записи с кодировкой UTF-8
        with open(ARTICLES_FILE, 'w', encoding='utf-8') as f:
            # Записывает пустой список в JSON
            json.dump([], f)

# Загрузка статей из файла articles.json
# Возвращает список статей или пустой список при ошибке
def load_articles():
    # Вызывает инициализацию, если файл отсутствует
    init_articles_file()
    try:
        # Открывает файл в режиме чтения с UTF-8
        with open(ARTICLES_FILE, 'r', encoding='utf-8') as f:
            # Загружает JSON-данные
            return json.load(f)
    except json.JSONDecodeError:
        # Логирует ошибку при повреждении файла
        print("Error: articles.json is corrupted, returning empty list")
        # Возвращает пустой список для продолжения работы
        return []

# Сохранение списка статей в файл articles.json
# Форматирует данные с отступами и поддерживает UTF-8
def save_articles(articles):
    try:
        # Открывает файл в режиме записи с UTF-8
        with open(ARTICLES_FILE, 'w', encoding='utf-8') as f:
            # Сохраняет статьи с отступами для читаемости
            json.dump(articles, f, indent=4, ensure_ascii=False)
    except Exception as e:
        # Вызывает исключение с описанием ошибки
        raise ValueError(f"Failed to save articles: {str(e)}")

# Проверка на повторяющиеся символы (4 и более одинаковых подряд)
# Используется для предотвращения бессмысленных строк (например, "aaaa")
def has_repeated_chars(s):
    # Регулярное выражение ищет 4+ одинаковых символа подряд
    pattern = r'(.)\1{3,}'
    # Возвращает True, если найдено совпадение
    return bool(re.search(pattern, s))

# Проверка на минимальное количество слов в тексте
# Требует минимум 3 слова для обеспечения содержательности
def has_minimum_words(text, min_words=3):
    # Разбивает текст на слова, игнорируя лишние пробелы
    words = [word for word in text.split() if word]
    # Проверяет, достаточно ли слов
    return len(words) >= min_words

# Проверка на наличие эмодзи в строке
# Предотвращает использование Unicode-символов эмодзи
def contains_emoji(text):
    # Паттерн охватывает основные диапазоны эмодзи
    emoji_pattern = r'[\U0001F300-\U0001F9FF\U0001F000-\U0001F02F\U0001F0A0-\U0001F0FF\U0001F680-\U0001F6FF]'
    # Возвращает True, если эмодзи найдены
    return bool(re.search(emoji_pattern, text))

# Проверка на подозрительные домены в URL
# Запрещает локальные адреса и потенциально опасные зоны
def is_suspicious_domain(url):
    # Список паттернов для подозрительных доменов (например, .onion, localhost)
    suspicious_patterns = [
        r'\.onion$', r'\.local$', r'\.localhost$', 
        r'^http://192\.168\.', r'^http://10\.', r'^http://172\.16\.'
    ]
    # Проверяет каждый паттерн
    for pattern in suspicious_patterns:
        if re.search(pattern, url, re.IGNORECASE):
            return True
    return False

# Проверка, что дата не находится в будущем
# Сравнивает введённую дату с текущей
def is_future_date(date_str):
    try:
        # Парсит дату в формате DD.MM.YYYY
        input_date = datetime.strptime(date_str, '%d.%m.%Y')
        # Получает текущую дату
        current_date = datetime.now()
        # Возвращает True, если дата в будущем
        return input_date > current_date
    except ValueError:
        # Возвращает False при ошибке парсинга
        return False

# Проверка формата и корректности даты (DD.MM.YYYY)
# Убедиться, что дата валидна и соответствует формату
def is_valid_date(date_str):
    # Паттерн: 01-31 для дня, 01-12 для месяца, 4 цифры для года
    pattern = r'^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.\d{4}$'
    # Проверяет соответствие формату
    if not re.match(pattern, date_str):
        return False
    try:
        # Проверяет реальность даты (например, исключает 31.04)
        datetime.strptime(date_str, '%d.%m.%Y')
        return True
    except ValueError:
        # Возвращает False для невалидных дат
        return False

# Проверка URL на валидность
# Поддерживает http(s), домены, пути и параметры
def is_valid_url(url):
    # Паттерн для строгой проверки URL
    pattern = (
        r'^https?://'  # Требует http или https
        r'(?:[a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+\.'  # Поддомены и домен
        r'(?:[a-zA-Z]{2,63}|xn--[a-zA-Z0-9-]+)'  # Доменная зона или IDN
        r'(?:/[\w\-./?%&=~:@!*\'();]*)*$'  # Путь и параметры
    )
    # Проверяет формат URL
    if not re.match(pattern, url, re.IGNORECASE):
        return False
    # Проверяет максимальную длину URL (2048 символов)
    if len(url) > 2048:
        return False
    return True

# Проверка поля author (3-50 символов, строгие правила)
# Обеспечивает осмысленное имя автора
def is_valid_author(author):
    # Паттерн: начинается с буквы, содержит латиницу, цифры, пробелы, дефисы, подчёркивания
    pattern = r'^[a-zA-Z][a-zA-Z0-9\s-_]{1,48}[a-zA-Z0-9]$'
    # Проверяет формат и длину
    if not re.match(pattern, author):
        return False
    # Запрещает кириллицу, арабский, китайский и другие не-латинские алфавиты
    if re.search(r'[\u0400-\u04FF\u0600-\u06FF\u4E00-\U0001FFFF]', author):
        return False
    # Запрещает строки из только цифр
    if re.match(r'^\d+$', author):
        return False
    # Запрещает повторяющиеся символы (например, "aaaa")
    if has_repeated_chars(author):
        return False
    # Запрещает множественные пробелы
    if re.search(r'\s{2,}', author):
        return False
    return True

# Проверка поля title (5-100 символов, строгие правила)
# Обеспечивает осмысленный заголовок
def is_valid_title(title):
    # Паттерн: начинается с буквы, содержит латиницу, цифры, пробелы, пунктуацию
    pattern = r'^[a-zA-Z][a-zA-Z0-9\s\-.,!?]{3,98}[a-zA-Z0-9.,!?]$'
    # Проверяет формат и длину
    if not re.match(pattern, title):
        return False
    # Запрещает кириллицу и другие не-латинские алфавиты
    if re.search(r'[\u0400-\u04FF\u0600-\u06FF\u4E00-\U0001FFFF]', title):
        return False
    # Запрещает строки из только пунктуации или цифр
    if re.match(r'^[\d\s\-.,!?]+$', title):
        return False
    # Запрещает множественные пробелы или последовательности пунктуации
    if re.search(r'\s{2,}|[-.,!?]{2,}', title):
        return False
    # Требует наличие хотя бы одного слова (2+ буквы)
    if not re.search(r'[a-zA-Z]{2,}', title):
        return False
    return True

# Проверка поля text (10-1000 символов, строгие правила)
# Обеспечивает безопасный и осмысленный текст
def is_valid_text(text):
    # Проверяет минимальную и максимальную длину
    if len(text) < 10 or len(text) > 1000:
        return False
    # Запрещает опасные HTML-теги и атрибуты
    html_pattern = (
        r'<(script|style|iframe|object|embed|form|input|button|textarea|meta|link|base|body|html|head)\b'
        r'|<[^>]+(on\w+)=|javascript:'
    )
    if re.search(html_pattern, text, re.IGNORECASE):
        return False
    # Запрещает кириллицу и другие не-латинские алфавиты
    if re.search(r'[\u0400-\u04FF\u0600-\u06FF\u4E00-\U0001FFFF]', text):
        return False
    # Запрещает эмодзи
    if contains_emoji(text):
        return False
    # Запрещает управляющие символы ASCII (кроме \n, \r, \t)
    if re.search(r'[\x00-\x08\x0B\x0C\x0E-\x1F]', text):
        return False
    # Запрещает длинные последовательности пробелов
    if re.search(r'\s{3,}', text):
        return False
    # Требует минимум 3 слова
    if not has_minimum_words(text, min_words=3):
        return False
    # Паттерн: только латиница, цифры, пробелы, допустимая пунктуация
    pattern = r'^[a-zA-Z0-9\s\-.,!?:;\'"()]+$'
    if not re.match(pattern, text):
        return False
    return True

# Проверка на наличие нецензурных слов
# Ищет целые слова из PROFANITY_LIST
def contains_profanity(text):
    # Приводит текст к нижнему регистру для сравнения
    text_lower = text.lower()
    # Проверяет каждое слово из списка
    for word in PROFANITY_LIST:
        # Использует \b для поиска целых слов
        if re.search(rf'\b{word}\b', text_lower):
            return True
    return False

# Получение данных для страницы статей
# Подготовка статей, ошибок и данных формы
def get_articles_data():
    # Загружает статьи из файла
    articles = load_articles()
    # Сортирует статьи по дате (новые сверху)
    try:
        articles.sort(key=lambda x: datetime.strptime(x['date'], '%d.%m.%Y'), reverse=True)
    except (KeyError, ValueError):
        # Логирует предупреждение при ошибке сортировки
        print("Warning: Skipping sorting due to invalid date format")
    # Извлекает ошибки из URL-параметров
    errors = request.query.getunicode('errors', '').split('|') if request.query.getunicode('errors') else []
    # Извлекает и декодирует данные формы
    form_data = {
        'author': unquote(request.query.getunicode('author', '')),
        'title': unquote(request.query.getunicode('title', '')),
        'text': unquote(request.query.getunicode('text', '')),
        'date': unquote(request.query.getunicode('date', '')),
        'link': unquote(request.query.getunicode('link', ''))
    }
    return articles, errors, form_data

# Обработка отправки формы
# Валидирует данные и сохраняет статью
def handle_article_submission():
    # Извлекает данные формы с поддержкой UTF-8
    author = request.forms.getunicode('author', '').strip()
    title = request.forms.getunicode('title', '').strip()
    text = request.forms.getunicode('text', '').strip()
    date = request.forms.getunicode('date', '').strip()
    link = request.forms.getunicode('link', '').strip()

    # Список для хранения ошибок валидации
    errors = []

    # Валидация автора
    # Проверяет, заполнено ли поле
    if not author:
        errors.append("Author is required.")
    # Проверяет формат, символы и другие ограничения
    elif not is_valid_author(author):
        errors.append("Author must be 3-50 characters (letters, digits, spaces, hyphens, underscores, English only, no repeated chars or only digits).")
    # Проверяет наличие нецензурных слов
    elif contains_profanity(author):
        errors.append("Author contains inappropriate language.")
    # Проверяет наличие эмодзи
    elif contains_emoji(author):
        errors.append("Author cannot contain emojis.")

    # Валидация заголовка
    # Проверяет, заполнено ли поле
    if not title:
        errors.append("Title is required.")
    # Проверяет формат, символы и другие ограничения
    elif not is_valid_title(title):
        errors.append("Title must be 5-100 characters (letters, digits, spaces, hyphens, punctuation, English only, at least one word).")
    # Проверяет наличие нецензурных слов
    elif contains_profanity(title):
        errors.append("Title contains inappropriate language.")
    # Проверяет наличие эмодзи
    elif contains_emoji(title):
        errors.append("Title cannot contain emojis.")

    # Валидация текста
    # Проверяет, заполнено ли поле
    if not text:
        errors.append("Text is required.")
    # Проверяет формат, символы и другие ограничения
    elif not is_valid_text(text):
        errors.append("Text must be 10-1000 characters, no HTML tags, English only, at least 3 words, no emojis or control chars.")
    # Проверяет наличие нецензурных слов
    elif contains_profanity(text):
        errors.append("Text contains inappropriate language.")

    # Валидация даты
    # Проверяет, заполнено ли поле
    if not date:
        errors.append("Date is required.")
    # Проверяет формат и реальность даты
    elif not is_valid_date(date):
        errors.append("Date must be in DD.MM.YYYY format and valid (e.g., 01.01.2025).")
    # Проверяет, не находится ли дата в будущем
    elif is_future_date(date):
        errors.append("Date cannot be in the future.")

    # Валидация ссылки
    # Проверяет, заполнено ли поле
    if not link:
        errors.append("Link is required.")
    # Проверяет формат URL
    elif not is_valid_url(link):
        errors.append("Link must be a valid URL (e.g., https://example.com).")
    # Проверяет подозрительные домены
    elif is_suspicious_domain(link):
        errors.append("Link cannot point to local or suspicious domains.")
    else:
        # Проверяет уникальность ссылки
        articles = load_articles()
        for article in articles:
            if article.get('link') == link:
                errors.append("This link has already been used for another article.")
                break

    # Если есть ошибки, перенаправляет с сохранением данных
    if errors:
        # Кодирует ошибки и данные формы для URL
        error_str = quote('|'.join(errors), safe='')
        author = quote(author, safe='')
        title = quote(title, safe='')
        text = quote(text, safe='')
        date = quote(date, safe='')
        link = quote(link, safe='')
        # Логирует ошибки для отладки
        print(f"Redirecting with errors: {errors}")
        # Устанавливает статус редиректа
        response.status = 302
        # Перенаправляет на страницу с ошибками
        response.set_header('Location', f'/articles?errors={error_str}&author={author}&title={title}&text={text}&date={date}&link={link}')
        return

    # Добавление новой статьи в список
    articles.append({
        'author': author,
        'title': title,
        'text': text,
        'date': date,
        'link': link
    })
    try:
        # Сохраняет статьи в файл
        save_articles(articles)
        # Логирует успешное сохранение
        print("Article saved successfully")
    except ValueError as e:
        # Добавляет ошибку сохранения
        errors.append(str(e))
        # Кодирует данные для редиректа
        error_str = quote('|'.join(errors), safe='')
        author = quote(author, safe='')
        title = quote(title, safe='')
        text = quote(text, safe='')
        date = quote(date, safe='')
        link = quote(link, safe='')
        # Логирует ошибку сохранения
        print(f"Error saving article: {str(e)}")
        # Устанавливает статус редиректа
        response.status = 302
        # Перенаправляет с ошибкой
        response.set_header('Location', f'/articles?errors={error_str}&author={author}&title={title}&text={text}&date={date}&link={link}')
        return

    # Успешный редирект после добавления статьи
    # Логирует перенаправление
    print("Redirecting to /articles")
    # Устанавливает статус редиректа
    response.status = 302
    # Перенаправляет на страницу статей
    response.set_header('Location', '/articles')