import json
from datetime import datetime
import re
import os
from bottle import request, response
from urllib.parse import quote

# ���� ��� �������� ������
ARTICLES_FILE = 'articles.json'

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

# �������� ������ (3-50 ��������, �����, �����, �������, ������, �������������)
def is_valid_author(author):
    pattern = r'^[\w\s-]{3,50}$'
    return bool(re.match(pattern, author))

# �������� ��������� (5-100 ��������, �����, �����, �������, ������, ����������)
def is_valid_title(title):
    pattern = r'^[\w\s\-.,!?]{5,100}$'
    return bool(re.match(pattern, title))

# �������� ������ (10-1000 ��������, ��� HTML-�����)
def is_valid_text(text):
    if len(text) < 10 or len(text) > 1000:
        return False
    html_pattern = r'<(script|style|iframe|object|embed|form|input|button|textarea)\b'
    return not bool(re.search(html_pattern, text, re.IGNORECASE))

# ��������� ������ ��� �������� ������
def get_articles_data():
    articles = load_articles()
    # ���������� ������ �� ���� (����� ������)
    try:
        articles.sort(key=lambda x: datetime.strptime(x['date'], '%d.%m.%Y'), reverse=True)
    except (KeyError, ValueError):
        print("Warning: Skipping sorting due to invalid date format")
    errors = request.query.get('errors', '').split('|') if request.query.get('errors') else []
    form_data = {
        'author': request.query.get('author', ''),
        'title': request.query.get('title', ''),
        'text': request.query.get('text', ''),
        'date': request.query.get('date', ''),
        'link': request.query.get('link', '')
    }
    return articles, errors, form_data

# ��������� �������� �����
def handle_article_submission():
    author = request.forms.get('author', '').strip()
    title = request.forms.get('title', '').strip()
    text = request.forms.get('text', '').strip()
    date = request.forms.get('date', '').strip()
    link = request.forms.get('link', '').strip()

    errors = []
    # ��������� ������
    if not author:
        errors.append("Author is required.")
    elif not is_valid_author(author):
        errors.append("Author must be 3-50 characters (letters, digits, spaces, hyphens, underscores).")

    # ��������� ���������
    if not title:
        errors.append("Title is required.")
    elif not is_valid_title(title):
        errors.append("Title must be 5-100 characters (letters, digits, spaces, hyphens, punctuation).")

    # ��������� ������
    if not text:
        errors.append("Text is required.")
    elif not is_valid_text(text):
        errors.append("Text must be 10-1000 characters and contain no HTML tags.")

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
        error_str = quote('|'.join(errors))
        author = quote(author)
        title = quote(title)
        text = quote(text)
        date = quote(date)
        link = quote(link)
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
        error_str = quote('|'.join(errors))
        author = quote(author)
        title = quote(title)
        text = quote(text)
        date = quote(date)
        link = quote(link)
        print(f"Error saving article: {str(e)}")
        response.status = 302
        response.set_header('Location', f'/articles?errors={error_str}&author={author}&title={title}&text={text}&date={date}&link={link}')
        return

    # �������� ����� �������� ��������
    print("Redirecting to /articles")
    response.status = 302
    response.set_header('Location', '/articles')