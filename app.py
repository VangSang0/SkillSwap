import os, re
import random
from dotenv import load_dotenv
from flask import Flask, abort, render_template, redirect, url_for, request, session, flash
from repositories import database_methods, other_methods
from flask_bcrypt import Bcrypt


load_dotenv()
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key= os.getenv('SECRET_KEY')




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
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')

    # Validation section
    if not username or not password or not user_email or not confirm_password or not first_name or not last_name:
        flash("Please enter all required fields")
        return redirect(url_for('sign_up_tab'))  

    elif ' ' in username or ' ' in password:
        flash("Username or Password cannot contain spaces")
        return redirect(url_for('sign_up_tab'))  

    elif len(username) < 4:
        flash("Username must be at least 4 characters long")
        return redirect(url_for('sign_up_tab'))  

    elif len(password) < 8:
        flash("Password must be at least 8 characters long")
        return redirect(url_for('sign_up_tab'))  

    elif not re.search(r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*_])", password):
        flash("Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character (!, @, #, $, %, ^, &, *, _)")
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
    new_user = database_methods.create_user(first_name, last_name, user_email, username, hashed_password)

    flash(f"Account created successfully {new_user['username']}! Please sign in to continue.")


    return redirect(url_for('sign_in'))


@app.get('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been successfully logged out!")
    return redirect(url_for('sign_in'))


@app.get('/home-page')
@other_methods.check_user # This is a decorator that checks if the user is signed in
def home_page():
    all_posts = database_methods.get_all_posts()
    random.shuffle(all_posts)
    for post in all_posts:
        post['datetime_post'] = other_methods.format_datetime(post['datetime_post'])
    
    current_user = database_methods.get_user_by_id(session['user_id'])

    return render_template('home_page.html', all_posts=all_posts, current_user=current_user)


@app.get('/profile-page')
@other_methods.check_user
def profile():
    if 'user_id' not in session:
        return redirect(url_for('sign_in'))
    return render_template('profile.html')

@app.get('/friends-page')
@other_methods.check_user
def friends():
    if 'user_id' not in session:
        return redirect(url_for('sign_in'))
    return render_template('friends_page.html')



@app.post('/user-post')
@other_methods.check_user
def user_post():
    post_author_id = database_methods.get_user_by_id(session['user_id'])['user_id']
    print(post_author_id)
    post_content = request.form.get('post-content')
    print(post_content)
    post_id = database_methods.add_post(post_author_id, post_content)
    if post_id is None:
        print("Post not added")

    return redirect(url_for('home_page'))

@app.get('/posts/<int:post_id>')
@other_methods.check_user
def post(post_id):
    post = database_methods.get_post_by_id(post_id)
    if post is None:
        abort(404)
    post['datetime_post'] = other_methods.format_datetime(post['datetime_post'])
    return render_template('posts.html', post=post)


@app.post('/delete-post')
@other_methods.check_user
def delete_post():
    post_id = request.form.get('delete')
    post = database_methods.get_post_by_id(post_id)
    
    print(post_id)
    print(post)
    if post is None:
        flash('There is no post with that ID')
    if post['post_author_id'] != session['user_id']:
        flash("You are not authorized to delete this post")
        return redirect(url_for('home_page'))
    
    database_methods.delete_post(post_id)
    return redirect(url_for('home_page'))


@app.get('/edit-post/<int:post_id>')
@other_methods.check_user
def edit_post(post_id):
    post = database_methods.get_post_by_id(post_id)
    if post is None:
        abort(404)
    if post['post_author_id'] != session['user_id']:
        abort(403)
    return render_template('edit_post.html', post=post)

@app.get('/user-posts')
@other_methods.check_user
def user_posts():
    user_id = session['user_id']
    user = database_methods.get_user_by_id(user_id)
    user_posts = database_methods.get_posts_by_user_id(user_id)
    for post in user_posts:
        post['datetime_post'] = other_methods.format_datetime(post['datetime_post'])
    return render_template('users_posts.html', user=user, user_posts=user_posts)

@app.get('/settings-page')
@other_methods.check_user
def settings():
    return render_template('settings_page.html')
