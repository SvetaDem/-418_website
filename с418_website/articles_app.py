import json
from datetime import datetime
import re
import os
from bottle import request, response
from urllib.parse import quote, unquote

# ���� ��� �������� ������ � ������� JSON
ARTICLES_FILE = 'articles.json'

# ����������� ������ ����������� ���� �� ���������� ��� �������� �����
# ������ ���������� ��������������� ����������� ��� ������������� ����������
PROFANITY_LIST = [
    "damn", "hell", "shit", "fuck", "bitch", "asshole", "crap", "piss", "dick", "cock",
    "bastard", "slut", "whore", "faggot", "nigger", "chink", "kike", "spic", "retard", "cunt"
]

# ������������� ����� articles.json, ���� �� �� ����������
# ������ ������ ������ ������ ��� �������������� ������ ��� ������ �������
def init_articles_file():
    # ��������� ������� ����� � ����������
    if not os.path.exists(ARTICLES_FILE):
        # ��������� ���� � ������ ������ � ���������� UTF-8
        with open(ARTICLES_FILE, 'w', encoding='utf-8') as f:
            # ���������� ������ ������ � JSON
            json.dump([], f)

# �������� ������ �� ����� articles.json
# ���������� ������ ������ ��� ������ ������ ��� ������
def load_articles():
    # �������� �������������, ���� ���� �����������
    init_articles_file()
    try:
        # ��������� ���� � ������ ������ � UTF-8
        with open(ARTICLES_FILE, 'r', encoding='utf-8') as f:
            # ��������� JSON-������
            return json.load(f)
    except json.JSONDecodeError:
        # �������� ������ ��� ����������� �����
        print("Error: articles.json is corrupted, returning empty list")
        # ���������� ������ ������ ��� ����������� ������
        return []

# ���������� ������ ������ � ���� articles.json
# ����������� ������ � ��������� � ������������ UTF-8
def save_articles(articles):
    try:
        # ��������� ���� � ������ ������ � UTF-8
        with open(ARTICLES_FILE, 'w', encoding='utf-8') as f:
            # ��������� ������ � ��������� ��� ����������
            json.dump(articles, f, indent=4, ensure_ascii=False)
    except Exception as e:
        # �������� ���������� � ��������� ������
        raise ValueError(f"Failed to save articles: {str(e)}")

# �������� �� ������������� ������� (4 � ����� ���������� ������)
# ������������ ��� �������������� ������������� ����� (��������, "aaaa")
def has_repeated_chars(s):
    # ���������� ��������� ���� 4+ ���������� ������� ������
    pattern = r'(.)\1{3,}'
    # ���������� True, ���� ������� ����������
    return bool(re.search(pattern, s))

# �������� �� ����������� ���������� ���� � ������
# ������� ������� 3 ����� ��� ����������� ����������������
def has_minimum_words(text, min_words=3):
    # ��������� ����� �� �����, ��������� ������ �������
    words = [word for word in text.split() if word]
    # ���������, ���������� �� ����
    return len(words) >= min_words

# �������� �� ������� ������ � ������
# ������������� ������������� Unicode-�������� ������
def contains_emoji(text):
    # ������� ���������� �������� ��������� ������
    emoji_pattern = r'[\U0001F300-\U0001F9FF\U0001F000-\U0001F02F\U0001F0A0-\U0001F0FF\U0001F680-\U0001F6FF]'
    # ���������� True, ���� ������ �������
    return bool(re.search(emoji_pattern, text))

# �������� �� �������������� ������ � URL
# ��������� ��������� ������ � ������������ ������� ����
def is_suspicious_domain(url):
    # ������ ��������� ��� �������������� ������� (��������, .onion, localhost)
    suspicious_patterns = [
        r'\.onion$', r'\.local$', r'\.localhost$', 
        r'^http://192\.168\.', r'^http://10\.', r'^http://172\.16\.'
    ]
    # ��������� ������ �������
    for pattern in suspicious_patterns:
        if re.search(pattern, url, re.IGNORECASE):
            return True
    return False

# ��������, ��� ���� �� ��������� � �������
# ���������� �������� ���� � �������
def is_future_date(date_str):
    try:
        # ������ ���� � ������� DD.MM.YYYY
        input_date = datetime.strptime(date_str, '%d.%m.%Y')
        # �������� ������� ����
        current_date = datetime.now()
        # ���������� True, ���� ���� � �������
        return input_date > current_date
    except ValueError:
        # ���������� False ��� ������ ��������
        return False

# �������� ������� � ������������ ���� (DD.MM.YYYY)
# ���������, ��� ���� ������� � ������������� �������
def is_valid_date(date_str):
    # �������: 01-31 ��� ���, 01-12 ��� ������, 4 ����� ��� ����
    pattern = r'^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.\d{4}$'
    # ��������� ������������ �������
    if not re.match(pattern, date_str):
        return False
    try:
        # ��������� ���������� ���� (��������, ��������� 31.04)
        datetime.strptime(date_str, '%d.%m.%Y')
        return True
    except ValueError:
        # ���������� False ��� ���������� ���
        return False

# �������� URL �� ����������
# ������������ http(s), ������, ���� � ���������
def is_valid_url(url):
    # ������� ��� ������� �������� URL
    pattern = (
        r'^https?://'  # ������� http ��� https
        r'(?:[a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+\.'  # ��������� � �����
        r'(?:[a-zA-Z]{2,63}|xn--[a-zA-Z0-9-]+)'  # �������� ���� ��� IDN
        r'(?:/[\w\-./?%&=~:@!*\'();]*)*$'  # ���� � ���������
    )
    # ��������� ������ URL
    if not re.match(pattern, url, re.IGNORECASE):
        return False
    # ��������� ������������ ����� URL (2048 ��������)
    if len(url) > 2048:
        return False
    return True

# �������� ���� author (3-50 ��������, ������� �������)
# ������������ ����������� ��� ������
def is_valid_author(author):
    # �������: ���������� � �����, �������� ��������, �����, �������, ������, �������������
    pattern = r'^[a-zA-Z][a-zA-Z0-9\s-_]{1,48}[a-zA-Z0-9]$'
    # ��������� ������ � �����
    if not re.match(pattern, author):
        return False
    # ��������� ���������, ��������, ��������� � ������ ��-��������� ��������
    if re.search(r'[\u0400-\u04FF\u0600-\u06FF\u4E00-\U0001FFFF]', author):
        return False
    # ��������� ������ �� ������ ����
    if re.match(r'^\d+$', author):
        return False
    # ��������� ������������� ������� (��������, "aaaa")
    if has_repeated_chars(author):
        return False
    # ��������� ������������� �������
    if re.search(r'\s{2,}', author):
        return False
    return True

# �������� ���� title (5-100 ��������, ������� �������)
# ������������ ����������� ���������
def is_valid_title(title):
    # �������: ���������� � �����, �������� ��������, �����, �������, ����������
    pattern = r'^[a-zA-Z][a-zA-Z0-9\s\-.,!?]{3,98}[a-zA-Z0-9.,!?]$'
    # ��������� ������ � �����
    if not re.match(pattern, title):
        return False
    # ��������� ��������� � ������ ��-��������� ��������
    if re.search(r'[\u0400-\u04FF\u0600-\u06FF\u4E00-\U0001FFFF]', title):
        return False
    # ��������� ������ �� ������ ���������� ��� ����
    if re.match(r'^[\d\s\-.,!?]+$', title):
        return False
    # ��������� ������������� ������� ��� ������������������ ����������
    if re.search(r'\s{2,}|[-.,!?]{2,}', title):
        return False
    # ������� ������� ���� �� ������ ����� (2+ �����)
    if not re.search(r'[a-zA-Z]{2,}', title):
        return False
    return True

# �������� ���� text (10-1000 ��������, ������� �������)
# ������������ ���������� � ����������� �����
def is_valid_text(text):
    # ��������� ����������� � ������������ �����
    if len(text) < 10 or len(text) > 1000:
        return False
    # ��������� ������� HTML-���� � ��������
    html_pattern = (
        r'<(script|style|iframe|object|embed|form|input|button|textarea|meta|link|base|body|html|head)\b'
        r'|<[^>]+(on\w+)=|javascript:'
    )
    if re.search(html_pattern, text, re.IGNORECASE):
        return False
    # ��������� ��������� � ������ ��-��������� ��������
    if re.search(r'[\u0400-\u04FF\u0600-\u06FF\u4E00-\U0001FFFF]', text):
        return False
    # ��������� ������
    if contains_emoji(text):
        return False
    # ��������� ����������� ������� ASCII (����� \n, \r, \t)
    if re.search(r'[\x00-\x08\x0B\x0C\x0E-\x1F]', text):
        return False
    # ��������� ������� ������������������ ��������
    if re.search(r'\s{3,}', text):
        return False
    # ������� ������� 3 �����
    if not has_minimum_words(text, min_words=3):
        return False
    # �������: ������ ��������, �����, �������, ���������� ����������
    pattern = r'^[a-zA-Z0-9\s\-.,!?:;\'"()]+$'
    if not re.match(pattern, text):
        return False
    return True

# �������� �� ������� ����������� ����
# ���� ����� ����� �� PROFANITY_LIST
def contains_profanity(text):
    # �������� ����� � ������� �������� ��� ���������
    text_lower = text.lower()
    # ��������� ������ ����� �� ������
    for word in PROFANITY_LIST:
        # ���������� \b ��� ������ ����� ����
        if re.search(rf'\b{word}\b', text_lower):
            return True
    return False

# ��������� ������ ��� �������� ������
# ���������� ������, ������ � ������ �����
def get_articles_data():
    # ��������� ������ �� �����
    articles = load_articles()
    # ��������� ������ �� ���� (����� ������)
    try:
        articles.sort(key=lambda x: datetime.strptime(x['date'], '%d.%m.%Y'), reverse=True)
    except (KeyError, ValueError):
        # �������� �������������� ��� ������ ����������
        print("Warning: Skipping sorting due to invalid date format")
    # ��������� ������ �� URL-����������
    errors = request.query.getunicode('errors', '').split('|') if request.query.getunicode('errors') else []
    # ��������� � ���������� ������ �����
    form_data = {
        'author': unquote(request.query.getunicode('author', '')),
        'title': unquote(request.query.getunicode('title', '')),
        'text': unquote(request.query.getunicode('text', '')),
        'date': unquote(request.query.getunicode('date', '')),
        'link': unquote(request.query.getunicode('link', ''))
    }
    return articles, errors, form_data

# ��������� �������� �����
# ���������� ������ � ��������� ������
def handle_article_submission():
    # ��������� ������ ����� � ���������� UTF-8
    author = request.forms.getunicode('author', '').strip()
    title = request.forms.getunicode('title', '').strip()
    text = request.forms.getunicode('text', '').strip()
    date = request.forms.getunicode('date', '').strip()
    link = request.forms.getunicode('link', '').strip()

    # ������ ��� �������� ������ ���������
    errors = []

    # ��������� ������
    # ���������, ��������� �� ����
    if not author:
        errors.append("Author is required.")
    # ��������� ������, ������� � ������ �����������
    elif not is_valid_author(author):
        errors.append("Author must be 3-50 characters (letters, digits, spaces, hyphens, underscores, English only, no repeated chars or only digits).")
    # ��������� ������� ����������� ����
    elif contains_profanity(author):
        errors.append("Author contains inappropriate language.")
    # ��������� ������� ������
    elif contains_emoji(author):
        errors.append("Author cannot contain emojis.")

    # ��������� ���������
    # ���������, ��������� �� ����
    if not title:
        errors.append("Title is required.")
    # ��������� ������, ������� � ������ �����������
    elif not is_valid_title(title):
        errors.append("Title must be 5-100 characters (letters, digits, spaces, hyphens, punctuation, English only, at least one word).")
    # ��������� ������� ����������� ����
    elif contains_profanity(title):
        errors.append("Title contains inappropriate language.")
    # ��������� ������� ������
    elif contains_emoji(title):
        errors.append("Title cannot contain emojis.")

    # ��������� ������
    # ���������, ��������� �� ����
    if not text:
        errors.append("Text is required.")
    # ��������� ������, ������� � ������ �����������
    elif not is_valid_text(text):
        errors.append("Text must be 10-1000 characters, no HTML tags, English only, at least 3 words, no emojis or control chars.")
    # ��������� ������� ����������� ����
    elif contains_profanity(text):
        errors.append("Text contains inappropriate language.")

    # ��������� ����
    # ���������, ��������� �� ����
    if not date:
        errors.append("Date is required.")
    # ��������� ������ � ���������� ����
    elif not is_valid_date(date):
        errors.append("Date must be in DD.MM.YYYY format and valid (e.g., 01.01.2025).")
    # ���������, �� ��������� �� ���� � �������
    elif is_future_date(date):
        errors.append("Date cannot be in the future.")

    # ��������� ������
    # ���������, ��������� �� ����
    if not link:
        errors.append("Link is required.")
    # ��������� ������ URL
    elif not is_valid_url(link):
        errors.append("Link must be a valid URL (e.g., https://example.com).")
    # ��������� �������������� ������
    elif is_suspicious_domain(link):
        errors.append("Link cannot point to local or suspicious domains.")
    else:
        # ��������� ������������ ������
        articles = load_articles()
        for article in articles:
            if article.get('link') == link:
                errors.append("This link has already been used for another article.")
                break

    # ���� ���� ������, �������������� � ����������� ������
    if errors:
        # �������� ������ � ������ ����� ��� URL
        error_str = quote('|'.join(errors), safe='')
        author = quote(author, safe='')
        title = quote(title, safe='')
        text = quote(text, safe='')
        date = quote(date, safe='')
        link = quote(link, safe='')
        # �������� ������ ��� �������
        print(f"Redirecting with errors: {errors}")
        # ������������� ������ ���������
        response.status = 302
        # �������������� �� �������� � ��������
        response.set_header('Location', f'/articles?errors={error_str}&author={author}&title={title}&text={text}&date={date}&link={link}')
        return

    # ���������� ����� ������ � ������
    articles.append({
        'author': author,
        'title': title,
        'text': text,
        'date': date,
        'link': link
    })
    try:
        # ��������� ������ � ����
        save_articles(articles)
        # �������� �������� ����������
        print("Article saved successfully")
    except ValueError as e:
        # ��������� ������ ����������
        errors.append(str(e))
        # �������� ������ ��� ���������
        error_str = quote('|'.join(errors), safe='')
        author = quote(author, safe='')
        title = quote(title, safe='')
        text = quote(text, safe='')
        date = quote(date, safe='')
        link = quote(link, safe='')
        # �������� ������ ����������
        print(f"Error saving article: {str(e)}")
        # ������������� ������ ���������
        response.status = 302
        # �������������� � �������
        response.set_header('Location', f'/articles?errors={error_str}&author={author}&title={title}&text={text}&date={date}&link={link}')
        return

    # �������� �������� ����� ���������� ������
    # �������� ���������������
    print("Redirecting to /articles")
    # ������������� ������ ���������
    response.status = 302
    # �������������� �� �������� ������
    response.set_header('Location', '/articles')