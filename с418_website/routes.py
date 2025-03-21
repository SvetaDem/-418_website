"""
Routes and views for the bottle application.
"""

from bottle import route, view, template
from datetime import datetime


@route('/')
@route('/home')
@view('index')
def home():
    """Renders the home page."""
    return dict(
        year=datetime.now().year
    )

@route('/contact')
@view('contact')
def contact():
    """Renders the contact page."""
    return dict(
        title='Contact',
        message='Your contact page.',
        year=datetime.now().year
    )

@route('/about')
@view('about')
def about():
    """Renders the about page."""
    return dict(
        title='About',
        message='Your application description page.',
        year=datetime.now().year
    )

@route('/songs')
@view('songs')
def songs():
    """Renders the songs page."""
    return dict(
        title='C418 Songs',
        message='List of C418 Songs in Minecraft.',
        year=datetime.now().year
    )

@route('/biography')
@view('biography')
def biography():
    """Renders the biography page."""
    return dict(
        title='Biography C418',
        message='Information about composer C418.',
        year=datetime.now().year
    )

@route('/music_tabs')
@view('music_tabs')
def music_tab():
    """Renders the music_tab page."""
    return dict(
        title='Tabs for C418`s music',
        message='Tabs for selected music by the C418.',
        year=datetime.now().year
    )