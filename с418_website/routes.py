"""
Routes and views for the bottle application.
"""

from bottle import route, view, template, request, redirect
from datetime import datetime
import actual_new_logic
import json
import os
import re

def context(**kwargs):
    """Create context dictionary with common data."""
    return dict(year=datetime.now().year, request=request, **kwargs)

@route('/')
@route('/home')
@view('index')
def home():
    """Render the home page."""
    return context(
        title='Home'
    )

@route('/contact')
@view('contact')
def contact():
    """Render the contact page."""
    return context(
        title='Contact',
        message='Your contact page.'
    )

@route('/about')
@view('about')
def about():
    """Render the about page."""
    return context(
        title='About',
        message='Your application description page.'
    )

@route('/songs')
@view('songs')
def songs():
    """Render the songs page."""
    return context(
        title='C418 Songs',
        message='List of C418 Songs in Minecraft.'
    )

@route('/biography')
@view('biography')
def biography():
    """Render the biography page."""
    return context(
        title='Biography C418',
        message='Information about composer C418.'
    )

@route('/music_tabs')
@view('music_tabs')
def music_tab():
    """Render the music tabs page."""
    return context(
        title='Tabs for C418`s music',
        message='Tabs for selected music by the C418.'
    )

@route('/actual_new')
@view('actual_new')
def actual_new():
    """Render the latest songs page."""
    songs, errors, form_data = actual_new_logic.get_songs_data()
    return dict(
        title='Latest C418 Songs',
        message='List of latest C418 songs.',
        year=datetime.now().year,
        songs=songs,
        errors=errors,
        form_data=form_data
    )

@route('/add_song', method='POST')
def add_song():
    """Handle song form submission."""
    actual_new_logic.handle_song_submission()