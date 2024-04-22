# Mainly for decorators and other functions that are not directly related to the DB

from functools import wraps
from flask import session, flash, redirect, url_for

def check_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please sign in to access this page")
            return redirect(url_for('sign_in'))
        return func(*args, **kwargs)
    return wrapper