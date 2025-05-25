import json
from datetime import datetime
import re
import os
from bottle import request, response
from urllib.parse import quote, unquote

# ���� ��� �������� ������
ARTICLES_FILE = 'articles.json'

# ������ ����������� ���� ��� ��������
PROFANITY_LIST = ["damn", "hell", "shit", "fuck"]

# ������������� ����� articles.json, ���� �� �� ����������
def init_articles_file():
    if not os.path.exists(ARTICLES_FILE):
        with open(ARTICLES_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

# �������� ������ �� �����
def load_articles():
    init_articles_file()
    try:
        with open(ARTICLES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Error: articles.json is corrupted, returning empty list")
        return []

# ���������� ������ � ����
def save_articles(articles):
    try:
        with open(ARTICLES_FILE, 'w', encoding='utf-8') as f:
            json.dump(articles, f, indent=2, ensure_ascii=False)
    except Exception as e:
        raise ValueError(f"Failed to save articles: {str(e)}")

# �������� ������� ���� (DD.MM.YYYY) � � ������������
def is_valid_date(date_str):
    pattern = r'^\d{2}\.\d{2}\.\d{4}$'
    if not re.match(pattern, date_str):
        return False
    try:
        datetime.strptime(date_str, '%d.%m.%Y')
        return True
    except ValueError:
        return False

# �������� URL (������������ http(s), ��������� ���������� � ������� �����)
def is_valid_url(url):
    pattern = r'^(https?://)([a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(/[\w\-./?%&=~:]*)*$'
    return bool(re.match(pattern, url))

# �������� ������ (3-50 ��������, ������ ��������, �����, �������, ������, �������������)
def is_valid_author(author):
    pattern = r'^[a-zA-Z0-9\s-]{3,50}$'
    if not re.match(pattern, author):
        return False
    # �������� �� ���������� ���������
    if re.search(r'[\u0400-\u04FF]', author):
        return False
    return True

# �������� ��������� (5-100 ��������, ������ ��������, �����, �������, ������, ����������)
def is_valid_title(title):
    pattern = r'^[a-zA-Z0-9\s\-.,!?]{5,100}$'
    if not re.match(pattern, title):
        return False
    # �������� �� ���������� ���������
    if re.search(r'[\u0400-\u04FF]', title):
        return False
    return True

# �������� ������ (10-1000 ��������, ��� HTML-�����, ��� ���������)
def is_valid_text(text):
    if len(text) < 10 or len(text) > 1000:
        return False
    html_pattern = r'<(script|style|iframe|object|embed|form|input|button|textarea)\b'
    if re.search(html_pattern, text, re.IGNORECASE):
        return False
    # �������� �� ���������� ���������
    if re.search(r'[\u0400-\u04FF]', text):
        return False
    return True

# �������� �� ������� ����������� ����
def contains_profanity(text):
    text_lower = text.lower()
    for word in PROFANITY_LIST:
        if word in text_lower:
            return True
    return False

# ��������� ������ ��� �������� ������
def get_articles_data():
    articles = load_articles()
    # ���������� ������ �� ���� (����� ������)
    try:
        articles.sort(key=lambda x: datetime.strptime(x['date'], '%d.%m.%Y'), reverse=True)
    except (KeyError, ValueError):
        print("Warning: Skipping sorting due to invalid date format")
    errors = request.query.getunicode('errors', '').split('|') if request.query.getunicode('errors') else []
    form_data = {
        'author': unquote(request.query.getunicode('author', '')),
        'title': unquote(request.query.getunicode('title', '')),
        'text': unquote(request.query.getunicode('text', '')),
        'date': unquote(request.query.getunicode('date', '')),
        'link': unquote(request.query.getunicode('link', ''))
    }
    return articles, errors, form_data

# ��������� �������� �����
def handle_article_submission():
    author = request.forms.getunicode('author', '').strip()
    title = request.forms.getunicode('title', '').strip()
    text = request.forms.getunicode('text', '').strip()
    date = request.forms.getunicode('date', '').strip()
    link = request.forms.getunicode('link', '').strip()

    errors = []
    # ��������� ������
    if not author:
        errors.append("Author is required.")
    elif not is_valid_author(author):
        errors.append("Author must be 3-50 characters (letters, digits, spaces, hyphens, underscores, English only).")
    elif contains_profanity(author):
        errors.append("Author contains inappropriate language.")

    # ��������� ���������
    if not title:
        errors.append("Title is required.")
    elif not is_valid_title(title):
        errors.append("Title must be 5-100 characters (letters, digits, spaces, hyphens, punctuation, English only).")
    elif contains_profanity(title):
        errors.append("Title contains inappropriate language.")

    # ��������� ������
    if not text:
        errors.append("Text is required.")
    elif not is_valid_text(text):
        errors.append("Text must be 10-1000 characters, contain no HTML tags, and use English characters only.")
    elif contains_profanity(text):
        errors.append("Text contains inappropriate language.")

    # ��������� ����
    if not date:
        errors.append("Date is required.")
    elif not is_valid_date(date):
        errors.append("Date must be in DD.MM.YYYY format and valid.")

    # ��������� ������
    if not link:
        errors.append("Link is required.")
    elif not is_valid_url(link):
        errors.append("Link must be a valid URL (e.g., https://example.com).")
    else:
        # �������� �� ������������ ������
        articles = load_articles()
        for article in articles:
            if article.get('link') == link:
                errors.append("This link has already been used for another article.")
                break

    if errors:
        # �������� � �������� � ����������� ������ �����
        error_str = quote('|'.join(errors), safe='')
        author = quote(author, safe='')
        title = quote(title, safe='')
        text = quote(text, safe='')
        date = quote(date, safe='')
        link = quote(link, safe='')
        print(f"Redirecting with errors: {errors}")
        response.status = 302
        response.set_header('Location', f'/articles?errors={error_str}&author={author}&title={title}&text={text}&date={date}&link={link}')
        return

    # ���������� ����� ������
    articles.append({
        'author': author,
        'title': title,
        'text': text,
        'date': date,
        'link': link
    })
    try:
        save_articles(articles)
        print("Article saved successfully")
    except ValueError as e:
        errors.append(str(e))
        error_str = quote('|'.join(errors), safe='')
        author = quote(author, safe='')
        title = quote(title, safe='')
        text = quote(text, safe='')
        date = quote(date, safe='')
        link = quote(link, safe='')
        print(f"Error saving article: {str(e)}")
        response.status = 302
        response.set_header('Location', f'/articles?errors={error_str}&author={author}&title={title}&text={text}&date={date}&link={link}')
        return

    # �������� ����� �������� ��������
    print("Redirecting to /articles")
    response.status = 302
    response.set_header('Location', '/articles')