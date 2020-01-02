# -*- coding: utf-8 -*-

"""User account class decorators."""

import functools

from typing import Callable
from flask import current_app, flash, redirect, session, url_for


def requires_login(f: Callable) -> Callable:
    """Insists a user be logged in to view a page."""
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('email'):
            flash('You must be logged in to view this page', 'danger')
            return redirect(url_for('users.login'))
        return f(*args, **kwargs)
    return decorated_function

def requires_admin(f: Callable) -> Callable:
    """Insists an administrator be logged in to view a page."""
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('email') != current_app.config.get('ADMIN', ''):
            flash('You must be an administrator to view this page.', 'danger')
            return redirect(url_for('users.login'))
        return f(*args, **kwargs)
    return decorated_function
