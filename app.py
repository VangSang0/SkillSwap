import os
from dotenv import load_dotenv
from flask import Flask, abort, render_template, redirect, url_for, request, session
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
        abort(400) # Will change this later, placeholder for now
    user = database_methods.get_user_by_username(username)
    if user is None:
        abort(401) # Will change this later, placeholder for now
    if not bcrypt.check_password_hash(user['hashed_password'], password):
        abort(401) # Will change this later, placeholder for now
    session['user_id'] = user['user_id']
    return redirect(url_for('home_page'))


@app.get('/sign-up')
def sign_up_tab():
    return render_template('sign_up.html')

@app.post('/signing-up')
def signing_up():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    if password != confirm_password:
        abort(400) # Will change this later, placeholder for now
    if not username or not password:
        abort(400) # Will change this later, placeholder for now

    existing_user = database_methods.does_user_exist(username)
    if existing_user is not None:
        abort(400) # Will change this later, placeholder for now
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    database_methods.create_user(username, hashed_password)

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


