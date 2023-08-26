# External Imports
from flask import Flask, session, redirect, send_from_directory, make_response, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import os

# Import ENVIRONMENT VARIABLES
SITE_NAME = os.environ['SITE_NAME'] if \
    'SITE_NAME' in os.environ else 'Default Site'
FLASK_STATIC = os.environ['FLASK_STATIC'] if \
     'FLASK_STATIC' in os.environ else None
FLASK_TEMPLATE = os.environ['FLASK_TEMPLATE'] if \
    'FLASK_TEMPLATE' in os.environ else None

SETUP_INCOMPLETE = True if not any(SETUP is None for SETUP in \
    (SITE_NAME, FLASK_STATIC, FLASK_TEMPLATE)) else False


if 'FLASK_SECRET_KEY' in os.environ:
    FLASK_SECRET_KEY = os.environ['FLASK_SECRET_KEY']
else:
    # TODO: Generate SECRET_KEY if one does not exist and place it in data folder
    FLASK_SECRET_KEY = None

if 'FLASK_SESSION_COOKIE' in os.environ:
    FLASK_SESSION_COOKIE = os.environ['FLASK_SESSION_COOKIE']
else:
    # TODO: Generate SECRET_KEY if one does not exist and place it in data folder
    FLASK_SESSION_COOKIE = None


if 'FLASK_SQLALCHEMY_TRACK_MODIFICATION' in os.environ:
    FLASK_SQL_ALCHEMY_TRACK_MODIFICATIONS = True if \
        os.environ['FLASK_SQLALCHEMY_TRACK_MODIFICATIONS'] == 'true' else False
else:
    FLASK_SQL_ALCHEMY_TRACK_MODIFICATIONS = False
if 'FLASK_DEBUG' in os.environ:
    FLASK_DBUG = True if \
        os.environ['FLASK_DEBUG'] == 'true' else False
else:
    FLASK_DEBUG = False
if 'FLASK_TESTING' in os.environ:
    FLASK_TESTING = True if \
        os.environ['FLASK_TESTINGS'] == 'true' else False
else:
    FLASK_TESTING = False

DATABASE_URI = os.environ['DATABASE_URL'] if 'DATABASE_URI'\
     in os.environ else 'sqlite:///'+SITE_NAME.replace(" ","_")

# Flask Setup
app = Flask(__name__)

#TODO: Check if setup is complete and try to correct automatically


try:
    app.config.update(
    SECRET_KEY                        = FLASK_SECRET_KEY,
    SESSION_COOKIE_NAME               = FLASK_SESSION_COOKIE,
    STATIC_FOLDER                     = FLASK_STATIC,
    TEMPLATES_FOLDER                  = FLASK_TEMPLATE,
    DEBUG                             = FLASK_DEBUG,
    TESTING                           = FLASK_TESTING,
    SQLALCHEMY_DATABASE_URI           = DATABASE_URI,
    SQLALCHEMY_TRACK_MODIFICATIONS    = FLASK_SQL_ALCHEMY_TRACK_MODIFICATIONS
    )
except:
    pass

# Session Setup
@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)

# Database Setup
db = SQLAlchemy(app)

# Import Blueprints
from app.blueprints import api
app.register_blueprint(api.api)