from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

friend_list = [
    {"name": "Sophia Page", "occupation": "Software Engineer", "distance": "500m away"},
    {"name": "Emma Johnson", "occupation": "Model at Fashion", "distance": "800m away"},
    {"name": "Nora Wilson", "occupation": "Writer at Newspaper", "distance": "2.5km away"},
]

@app.get('/')
def home():
    return render_template('index.html')

@app.get('/friends')
def friends():
    return render_template('friendsPage.html', friend_list=friend_list)
