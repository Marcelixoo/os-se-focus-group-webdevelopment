# file to configure flask, loaded into our flask application
# using the line: app.config.from_pyfile("config.py") in website.py
from os import environ
import os

# These variables be available to your application to use.
# Things that may be different on different computers, like a path to a file,
# should go in here. This is all available in GitHub, so be careful.

# SECRET_KEY = 'secretkey'
SECRET_KEY = 'you-will-never-guess'
SQLALCHEMY_DATABASE_URI = 'sqlite:///emojis_library.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
MY_PORT = "5000"
SECURITY_PASSWORD_SALT = 'my_precious_two'
