from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import sys
import os


# configure Flask using environment variables
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message = 'Please log in to access this page!'
login_manager.login_message_category = 'info'


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    db.init_app(app)
    login_manager.init_app(app)

    from my_fav_emojis.emojis.routes import emojis
    from my_fav_emojis.auth.routes import auth

    app.register_blueprint(auth)
    app.register_blueprint(emojis)

    return app
