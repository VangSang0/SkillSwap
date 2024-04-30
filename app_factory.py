import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY')
    bcrypt = Bcrypt(app)
    db = SQLAlchemy(app)
    
    return app, bcrypt, db

app, bcrypt, db = create_app()