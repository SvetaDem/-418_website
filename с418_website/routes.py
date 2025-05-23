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
    return template('songs')

@route('/biography')
@view('biography')
def biography():
    """Renders the biography page."""
    return dict(
        title='Biography C418',
        message='Information about composer C418.',
        year=datetime.now().year
    )

@route('/activeUsers')
@view('activeUsers')
def contact():
    """Renders the contact page."""
    return dict(
        title='ActiveUsers',
        message='Your contact page.',
        year=datetime.now().year
    )