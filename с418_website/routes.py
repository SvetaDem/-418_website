"""
Routes and views for the bottle application.
"""

from bottle import route, view, template, request
from datetime import datetime
from articles_app import get_articles_data, handle_article_submission
from forms.active_users_form import load_users

def context(**kwargs):
    return dict(year=datetime.now().year, request=request, **kwargs)

@route('/')
@route('/home')
@view('index')
def home():
    """Renders the home page."""
    return context(
        title='Home'
    )

@route('/contact')
@view('contact')
def contact():
    """Renders the contact page."""
    return context(
        title='Contact',
        message='Your contact page.'
    )

@route('/about')
@view('about')
def about():
    """Renders the about page."""
    return context(
        title='About',
        message='Your application description page.'
    )

@route('/songs')
@view('songs')
def songs():
    """Renders the songs page."""
    return context(
        title='C418 Songs',
        message='List of C418 Songs in Minecraft.'
    )

@route('/biography')
@view('biography')
def biography():
    """Renders the biography page."""
    return context(
        title='Biography C418',
        message='Information about composer C418.'
    )

@route('/articles')
@view('articles')
def articles():
    """Renders the articles page."""
    # Get articles, errors, and form data from articles_app
    articles, errors, form_data = get_articles_data()
    return context(
        title='Useful Articles about C418',
        message='Read and share articles about composer C418.',
        articles=articles,
        errors=errors,
        form_data=form_data
    )

@route('/add_article', method='POST')
def add_article():
    """Handles article submission."""
    handle_article_submission()

@route('/music_tabs')
@view('music_tabs')
def music_tab():
    """Renders the music_tab page."""
    return context(
        title='Tabs for C418`s music',
        message='Tabs for selected music by the C418.',
        year=datetime.now().year
    )

@route('/active_users')
@view('active_users')
def active_users():
    """Renders the active users page."""
    return context(
        title='Active users',
        message='List of active users.',
        users=load_users(),
        error=None
    )
