import os
from dotenv import load_dotenv
from flask import Flask, abort, render_template, redirect, url_for, request, session, flash
from repositories import database_methods
from flask_bcrypt import Bcrypt


load_dotenv()
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key= os.getenv('SECRET_KEY')


# Dummy Data
posts = [
    {

        'author' : 'Sangy Vangy',
        'title' : 'Post 1',
        'content' : 'This is for test purposes only',
        'date_posted' : 'July 3, 2024'

    },
    {

        'author' : 'John Doe',
        'title' : 'Happy Independence Day!',
        'content' : 'Today we are outside prepping for the fireworks show but I was wondering if there was a way to make this into a program. Any thoughts?',
        'date_posted' : 'July 4, 2024'

    },
]

@app.get('/')
def sign_in():

    return render_template('sign_in.html')

@app.post('/signing-in')
def signing_in():
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        flash("Please enter the required fields")
        return redirect(url_for('sign_in'))
    user = database_methods.get_user_by_username(username)
    if user is None:
        flash("Invalid username or password")
        return redirect(url_for('sign_in'))
    if not bcrypt.check_password_hash(user['hashed_password'], password):
        flash("Invalid username or password")
        return redirect(url_for('sign_in'))
    session['user_id'] = user['user_id']
    return redirect(url_for('home_page'))


@app.get('/sign-up')
def sign_up_tab():
    return render_template('sign_up.html')

@app.post('/signing-up')
def signing_up():

    user_email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')

    # Validation section
    if not username or not password or not user_email:
        flash("Please enter the required fields")
    elif password.__contains__(' ') or username.__contains__(' '):
        flash("Username or Password cannot contain spaces")
        return redirect(url_for('sign_up_tab'))
    elif len(username) < 4:
        flash("Username must be at least 4 characters long")
        return redirect(url_for('sign_up_tab'))
    elif len(password) < 8:
        flash("Password must be at least 8 characters long")
        return redirect(url_for('sign_up_tab'))
    elif password.islower() or password.isupper():
        flash("Password must contain at least one uppercase and one lowercase letter")
        return redirect(url_for('sign_up_tab'))
    elif password.isalpha():
        flash("Password must contain at least one number")
        return redirect(url_for('sign_up_tab'))
    elif password.isnumeric():
        flash("Password must contain at least one letter")
        return redirect(url_for('sign_up_tab'))
    elif not any(char in password for char in '!@#$%^&*_'):
        flash("Password must contain at least one special character (!, @, #, $, %, ^, &, *, _)")
        return redirect(url_for('sign_up_tab'))
    elif password != confirm_password:
        flash("Passwords do not match, please try again")
        return redirect(url_for('sign_up_tab'))

    existing_email = database_methods.does_email_exist(user_email)
    if existing_email:
        flash("Email already exists, You may already have an account")
        return redirect(url_for('sign_up_tab'))
    existing_username = database_methods.does_user_exist(username)
    if existing_username:
        flash("Username already exists, please try another")
        return redirect(url_for('sign_up_tab'))

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = database_methods.create_user(user_email, username, hashed_password)
    flash(f"Account created successfully {new_user['username']}! Please sign in to continue.")

    return redirect(url_for('sign_in'))





@app.get('/home-page')
def home_page():
    if 'user_id' not in session:
        return redirect(url_for('sign_in'))
    return render_template('home_page.html', posts=posts)


@app.get('/profile-page')
def profile():

    return render_template('profile.html')

@app.get('/friends-page')
def friends():

    return render_template('friends_page.html')


