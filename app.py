from flask import Flask, render_template, redirect, url_for

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
def sign_up():
    return render_template('sign_up.html')

@app.get('/home')
def home():

    return render_template('index.html', posts=posts)


@app.get('/profile')
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)
