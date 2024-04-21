from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


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

    return redirect(url_for('home_page'))


@app.get('/sign-up')
def sign_up_tab():

    return render_template('sign_up.html')

@app.post('/signing-up')
def signing_up():

    return redirect(url_for('sign_in'))





@app.get('/home-page')
def home_page():

    return render_template('home_page.html', posts=posts)


@app.get('/profile-page')
def profile():

    return render_template('profile.html')

@app.get('/friends-page')
def friends():

    return render_template('friends_page.html')



@app.post('/user-post')
def user_post():
    post_content = request.form.get('post-content')
    print(post_content)

    #Place holder for the post just because we haven't approved user authentication
    post = {
        'author' : 'John Doe',
        'title' : 'User Post',
        'content' : post_content,
        'date_posted' : 'July 4, 2024'
    }
    posts.append(post)
    return redirect(url_for('home_page'))