from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.get('/')
def home():
    return render_template('index.html')

