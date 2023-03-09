from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path, mkdir
from flask_login import LoginManager
import random

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)

    UPLOAD_FOLDER = 'uploads'
    if not path.exists(UPLOAD_FOLDER):
        mkdir(UPLOAD_FOLDER)

    ALLOWED_EXTENSIONS = {'mp3'}

    app.config['SECRET_KEY'] = 'dubbed-curled-renewable'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    from .models import User, Upload

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) # Function automatically searches for primary ID

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app = app)
        print('Created Database!')