import os, re, random
import psycopg, psycopg2
from psycopg.rows import dict_row
from psycopg2 import sql
from psycopg2.extras import DictCursor
from typing import Any, List
from dotenv import load_dotenv
from flask import Flask, abort, render_template, redirect, url_for, request, session, flash, Blueprint, jsonify
from repositories import database_methods, other_methods
from flask import request, redirect, url_for, flash, session
from app_factory import create_app
from flask_sqlalchemy import SQLAlchemy
# from app import app, db


load_dotenv()
app, bcrypt = create_app()

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

    user_id = session.get('user_id')
    user = database_methods.get_user_information_by_id(user_id)
    post = database_methods.get_posts_by_user_id(user_id)


    return render_template('profile.html', user=user, post=post)

@app.post('/search')
@other_methods.check_user
def search():
    if request.method == 'POST':
        query = request.form.get('query')
        return redirect(url_for('search_users', query=query))
    return render_template('searchbar_page.html')

# Example Flask route using the search_users function
@app.get('/search')
@other_methods.check_user
def search_users():
    query = request.args.get('query', '')
    if query:
        users = database_methods.search_users(query)
        return render_template('searchbar_page.html', users=users, query=query)
    else:
        return render_template('searchbar_page.html', users=[], query=query)



@app.get('/friends-page')
@other_methods.check_user
def friends():
    user_id = session['user_id']
    if 'user_id' not in session:
        return redirect(url_for('sign_in'))
    # Retrieve user's friends from the database
    friends = database_methods.get_user_friends(user_id)
    # Retrieve incoming friend requests
    incoming_requests = database_methods.get_incoming_friend_requests(user_id)
    return render_template('friends_page.html',friends=friends, incoming_requests=incoming_requests)

@app.post('/user-post')
@other_methods.check_user
def user_post():
    post_author_id = database_methods.get_user_by_id(session['user_id'])['user_id']
    post_content = request.form.get('post-content')
    if post_content.strip() == "" or not post_content:
        flash("Please enter post content")
        return redirect(url_for('home_page'))
    post_id = database_methods.add_post(post_author_id, post_content)
    if post_id is None:
        flash("Post not added")
        return redirect(url_for('home_page'))

    return redirect(url_for('home_page'))

@app.get('/posts/<int:post_id>')
@other_methods.check_user
def post(post_id):
    current_user = database_methods.get_user_by_id(session['user_id'])
    post = database_methods.get_post_by_id(post_id)
    comments = database_methods.get_comments_by_post_id(post_id)
    if post is None or not post:
        abort(404)
    post['datetime_post'] = other_methods.format_datetime(post['datetime_post'])
    for comment in comments:
        comment['datetime_posted'] = other_methods.format_datetime(comment['datetime_posted'])
    return render_template('posts.html', post=post, comments=comments, current_user=current_user)


@app.post('/delete-post')
@other_methods.check_user
def delete_post():
    post_id = request.form.get('delete')
    post = database_methods.get_post_by_id(post_id)
    
    if post is None:
        flash('There is no post with that ID')
    if post['post_author_id'] != session['user_id']:
        flash("You are not authorized to delete this post")
        return redirect(url_for('home_page'))
    
    database_methods.delete_post(post_id)
    return redirect(url_for('home_page'))

@app.post('/delete-post-from-myposts')
@other_methods.check_user
def delete_post_from_myposts():
    post_id = request.form.get('delete')
    post = database_methods.get_post_by_id(post_id)
    
    if post is None:
        flash('There is no post with that ID')
        return redirect(url_for('user_posts'))
    if post['post_author_id'] != session['user_id']:
        flash("You are not authorized to delete this post")
        return redirect(url_for('home_page'))
    
    database_methods.delete_post(post_id)
    return redirect(url_for('user_posts'))


@app.get('/edit-post/<int:post_id>')
@other_methods.check_user
def edit_post(post_id):
    user = database_methods.get_user_by_id(session['user_id'])
    post = database_methods.get_post_by_id(post_id)
    if post is None:
        flash("There is no post with that ID")
        return redirect(url_for('home_page'))
    if post['post_author_id'] != session['user_id']:
        flash("You are not authorized to edit this post")
        return redirect(url_for('home_page'))
    post['datetime_post'] = other_methods.format_datetime(post['datetime_post'])
    return render_template('edit_post.html', user=user, post=post)

@app.post('/edit-post')
@other_methods.check_user
def edit_post_submit():
    post_content = request.form.get('post-content')
    post_id = request.form.get('post_id')
    if post_content.strip() == "" or not post_content:
        flash("Please enter post content")
        return redirect(url_for('edit_post', post_id=post_id))
    post = database_methods.get_post_by_id(post_id)
    if post is None:
        flash("There is no post with that ID")
        return redirect(url_for('home_page'))
    if post['post_author_id'] != session['user_id']:
        flash("You are not authorized to edit this post")
        return redirect(url_for('home_page'))
    database_methods.edit_post(post_id, post_content)
    return redirect(url_for('home_page'))

@app.get('/users-posts')
@other_methods.check_user
def user_posts():
    user_id = session['user_id']
    user = database_methods.get_user_by_id(user_id)
    user_posts = database_methods.get_posts_by_user_id(user_id)
    for post in user_posts:
        post['datetime_post'] = other_methods.format_datetime(post['datetime_post'])
    return render_template('users_posts.html', user=user, user_posts=user_posts)

@app.post('/comment')
@other_methods.check_user
def make_comment():
    post_id = request.form.get('post_id')
    comment_content = request.form.get('comment-content')
    author_id = session['user_id']
    if comment_content.strip() == "" or not comment_content:
        flash("Please enter comment content")
        return redirect(url_for('post', post_id=post_id))
    comment_id = database_methods.add_comment(author_id, post_id, comment_content)
    if comment_id is None:
        flash("Comment not added")
        return redirect(url_for('post', post_id=post_id))
    return redirect(url_for('post', post_id=post_id))

@app.post('/delete-comment')
@other_methods.check_user
def delete_comment():
    post_id = request.form.get('post_id')
    comment_id = request.form.get('delete')
    comment = database_methods.get_comment_by_id(comment_id)
    if comment is None:
        flash('There is no comment with that ID')
        return redirect(url_for('post', post_id=post_id))
    if comment['comment_author_id'] != session['user_id']:
        flash("You are not authorized to delete this comment")
        return redirect(url_for('post', post_id=post_id))
    database_methods.delete_comment(comment_id)
    return redirect(url_for('post', post_id=post_id))

@app.get('/edit-comment/<int:post_id>/<int:comment_id>')
@other_methods.check_user
def edit_comment(post_id, comment_id):
    current_user = database_methods.get_user_by_id(session['user_id'])
    current_comment = database_methods.get_comment_by_id(comment_id)
    post = database_methods.get_post_by_id(post_id)
    # if post is None:
    #     return redirect(url_for('error_page'))
    if current_comment is None:
        flash("There is no comment with that ID")
        return redirect(url_for('post', post_id=post_id))
    if current_comment['comment_author_id'] != session['user_id']:
        flash("You are not authorized to edit this comment")
        return redirect(url_for('post', post_id=post_id))
    return render_template('edit_comment.html', current_user=current_user , post=post, current_comment=current_comment, post_id=post_id)

@app.post('/confirm-edit-comment')
def confirm_edit_comment():
    comment_id = request.form.get('comment_id')
    post_id = request.form.get('post_id')
    comment_content = request.form.get('comment-content')
    if comment_content.strip() == "" or not comment_content:
        flash("Please enter comment content")
        return redirect(url_for('edit_comment', post_id=post_id, comment_id=comment_id))
    comment = database_methods.get_comment_by_id(comment_id)
    if comment['comment_author_id'] != session['user_id']:
        flash("You are not authorized to edit this comment")
        return redirect(url_for('post', post_id=post_id))
    database_methods.edit_comment(comment_id, comment_content)
    return redirect(url_for('post', post_id=post_id))

@app.post('/toggle-like')
@other_methods.check_user  # Assuming this decorator checks if the user is logged in
def toggle_like():
    data = request.get_json()
    post_id = data.get('post_id')

    if not post_id:
        # For AJAX, you should return a JSON response
        return jsonify(success=False, message="Invalid post"), 400

    user_id = session['user_id']  # Get the user ID from the session

    try:
        # Perform the like toggle and get the new like count
        new_like_count, operation = database_methods.toggle_like(user_id, int(post_id))

        # Prevent negative like count
        if new_like_count < 0:
            new_like_count = 0
            database_methods.set_like_count(post_id, new_like_count)

        return jsonify(success=True, likeCount=new_like_count, operation=operation)

    except Exception as e:
        # Log the exception for debugging
        app.logger.error('Error while toggling like: %s', str(e))
        return jsonify(success=False, message="An error occurred while toggling the like."), 500


@app.get('/settings-page') #settings(nicole)
@other_methods.check_user
def settings():
   user_id = session['user_id']
   user_info = database_methods.get_user_by_id(user_id)
   if user_info is None:
       flash("User not found")
       return redirect(url_for('sign_in'))
   return render_template('settings_page.html', user_info=user_info)


@app.post('/save-settings')
@other_methods.check_user
def save_settings():
   user_id = session.get('user_id')
   if user_id is None:
       abort(401) 


  
   email = request.form.get('email')
   first_name = request.form.get('first-name')
   last_name = request.form.get('last-name')
   new_username = request.form.get('new-username')
   current_password = request.form.get('current-password')
   new_password = request.form.get('new-password')
   confirm_new_password = request.form.get('confirm-new-password')


  
   try:
       if new_username:
           database_methods.update_username(user_id, new_username)
           flash("Username updated successfully!", "success")
      
       if current_password and new_password and confirm_new_password:
           user_info = database_methods.get_user_by_id(user_id)
           if bcrypt.check_password_hash(user_info['hashed_password'], current_password):
               if new_password == confirm_new_password:
                   hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
                   database_methods.update_password(user_id, hashed_password)
                   flash("Password updated successfully!", "success")
               else:
                   flash("New passwords do not match", "error")
           else:
               flash("Current password is incorrect", "error")
      
       database_methods.update_user_settings(user_id, email, first_name, last_name)
       flash("Settings saved successfully!", "success")
   except Exception as e:
       flash(f"An error occurred: {str(e)}", "error")
       app.logger.error("Error occurred while saving settings: %s", str(e))


   return redirect(url_for('settings'))

# @app.post('/search')
# @other_methods.check_user
# def search():
#     if request.method == 'POST':
#         query = request.form.get('query')
#         return redirect(url_for('search_users', query=query))
#     return render_template('searchbar_page.html')

# # Example Flask route using the search_users function
# @app.get('/search')
# @other_methods.check_user
# def search_users():
#     query = request.args.get('query', '')
#     if query:
#         users = database_methods.search_users(query)
#         return render_template('searchbar_page.html', users=users, query=query)
#     else:
#         return render_template('searchbar_page.html', users=[], query=query)


