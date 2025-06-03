import json
from datetime import datetime, timedelta
import re
import os
from bottle import request, response
from urllib.parse import quote, unquote

# File for storing songs in JSON format
SONGS_FILE = 'songs.json'

# List of profane words for validation
PROFANITY_LIST = [
    "damn", "hell", "shit", "fuck", "bitch", "asshole", "crap", "piss", "dick", "cock",
    "bastard", "slut", "whore", "faggot", "nigger", "chink", "kike", "spic", "retard", "cunt"
]

def init_songs_file():
    """Initialize songs.json if it doesn't exist."""
    if not os.path.exists(SONGS_FILE):
        with open(SONGS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

def load_songs():
    """Load songs from songs.json."""
    init_songs_file()
    try:
        with open(SONGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Error: songs.json is corrupted, returning empty list")
        return []

def save_songs(songs):
    """Save songs to songs.json."""
    try:
        with open(SONGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(songs, f, indent=4, ensure_ascii=False)
    except Exception as e:
        raise ValueError(f"Failed to save songs: {str(e)}")

def has_repeated_chars(s):
    """Check for 4 or more repeated characters."""
    pattern = r'(.)\1{3,}'
    return bool(re.search(pattern, s))

def has_minimum_words(text, min_words=3):
    """Check for minimum number of words."""
    words = [word for word in text.split() if word]
    return len(words) >= min_words

def has_meaningful_words(text):
    """Check for at least one meaningful word (4+ letters, no repeats)."""
    words = [word for word in text.split() if word]
    for word in words:
        if len(word) >= 4 and re.match(r'^[a-zA-Z]+$', word) and not has_repeated_chars(word):
            return True
    return False

def contains_emoji(text):
    """Check for emojis in text."""
    emoji_pattern = r'[\U0001F300-\U0001F9FF\U0001F000-\U0001F02F\U0001F0A0-\U0001F0FF\U0001F680-\U0001F6FF]'
    return bool(re.search(emoji_pattern, text))

def is_valid_date(date_str):
    """Validate date format and correctness (DD.MM.YYYY)."""
    pattern = r'^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.\d{4}$'
    if not re.match(pattern, date_str):
        return False
    try:
        datetime.strptime(date_str, '%d.%m.%Y')
        return True
    except ValueError:
        return False

def is_valid_date_range(date_str):
    """Check if date is not before today and not more than 10 years from today."""
    try:
        input_date = datetime.strptime(date_str, '%d.%m.%Y').date()
        current_date = datetime.now().date()
        max_date = current_date + timedelta(days=365 * 10)  # 10 years
        if input_date < current_date:
            return False, "Date cannot be before today."
        if input_date > max_date:
            return False, "Date cannot be more than 10 years from today."
        return True, ""
    except ValueError:
        return False, "Invalid date."

def is_valid_author(author):
    """Validate author/name field (3-50 characters, English only)."""
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

def is_valid_description(description):
    """Validate description field (10-1000 characters, English only)."""
    if len(description) < 10 or len(description) > 1000:
        return False
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

def contains_profanity(text):
    """Check for profanity in text."""
    text_lower = text.lower()
    for word in PROFANITY_LIST:
        if re.search(rf'\b{word}\b', text_lower):
            return True
    return False

def get_songs_data():
    """Retrieve songs, errors, and form data with filtering."""
    songs = load_songs()
    current_date = datetime.now().date()
    
    # Filter out songs with dates before today
    songs = [song for song in songs if datetime.strptime(song['date'], '%d.%m.%Y').date() >= current_date]
    
    filter_type = request.query.getunicode('filter', 'recent')
    
    try:
        if filter_type == 'recent':
            # Sort by closest to current date (most recent first)
            songs.sort(key=lambda x: (datetime.strptime(x['date'], '%d.%m.%Y').date() - current_date).days)
        elif filter_type == 'older':
            # Sort by furthest from current date (future dates first)
            songs.sort(key=lambda x: (datetime.strptime(x['date'], '%d.%m.%Y').date() - current_date).days, reverse=True)
        else:
            # Default: sort by date, newest first
            songs.sort(key=lambda x: datetime.strptime(x['date'], '%d.%m.%Y'), reverse=True)
    except (KeyError, ValueError):
        print("Warning: Skipping sorting due to invalid date format")

    errors = request.query.getunicode('errors', '').split('|') if request.query.getunicode('errors') else []
    form_data = {
        'author': unquote(request.query.getunicode('author', '')),
        'description': unquote(request.query.getunicode('description', '')),
        'date': unquote(request.query.getunicode('date', ''))
    }
    return songs, errors, form_data

def handle_song_submission():
    """Handle song form submission with validation."""
    author = request.forms.getunicode('author', '').strip()
    description = request.forms.getunicode('description', '').strip()
    date = request.forms.getunicode('date', '').strip()

    errors = []

    # Validate author/name
    if not author:
        errors.append("Author/Name is required.")
    elif not is_valid_author(author):
        errors.append("Author/Name must be 3-50 characters (letters, digits, spaces, hyphens, underscores, English only, no repeated chars or only digits).")
    elif contains_profanity(author):
        errors.append("Author/Name contains inappropriate language.")
    elif contains_emoji(author):
        errors.append("Author/Name cannot contain emojis.")

    # Validate description
    if not description:
        errors.append("Description is required.")
    elif not is_valid_description(description):
        errors.append("Description must be 10-1000 characters, no HTML tags, English only, at least 3 words including one meaningful word.")
    elif contains_profanity(description):
        errors.append("Description contains inappropriate language.")

    # Validate date
    if not date:
        errors.append("Date is required.")
    elif not is_valid_date(date):
        errors.append("Date must be in DD.MM.YYYY format and valid (e.g., 03.06.2025).")
    else:
        is_valid, error_msg = is_valid_date_range(date)
        if not is_valid:
            errors.append(error_msg)

    # Handle errors
    if errors:
        error_str = quote('|'.join(errors), safe='')
        author = quote(author, safe='')
        description = quote(description, safe='')
        date = quote(date, safe='')
        print(f"Redirecting with errors: {errors}")
        response.status = 302
        response.set_header('Location', f'/actual_new?errors={error_str}&author={author}&description={description}&date={date}')
        return

    # Add new song
    songs = load_songs()
    songs.append({
        'author': author,
        'description': description,
        'date': date
    })
    try:
        save_songs(songs)
        print("Song saved successfully")
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

    # Successful redirect
    print("Redirecting to /actual_new")
    response.status = 302
    response.set_header('Location', '/actual_new')