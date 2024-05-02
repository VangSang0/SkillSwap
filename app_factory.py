import os
from flask import Flask
from flask_bcrypt import Bcrypt

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY')
    bcrypt = Bcrypt(app)
    app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
    return app, bcrypt
