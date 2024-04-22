# Mainly for decorators and other functions that are not directly related to the DB

from functools import wraps
from flask import session, flash, redirect, url_for
from datetime import datetime

def check_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please sign in to access this page")
            return redirect(url_for('sign_in'))
        return func(*args, **kwargs)
    return wrapper


def format_datetime(datetime_obj: str) -> str:
    time_diff = datetime_obj - datetime.now() 

    intervals = [
        ('years', 31536000),
        ('months', 2592000),
        ('days', 86400),
        ('hours', 3600),
        ('minutes', 60),
        ('seconds', 1)
    ]
    for unit, seconds in intervals:
        delta = time_diff.total_seconds() // seconds
        if delta > 0:
            if delta == 1:
                return f'{int(delta)} {unit} ago'
            else:
                return f'{int(delta)} {unit} ago'
    return 'just now'