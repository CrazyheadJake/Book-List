from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mongoengine import MongoEngine

db = SQLAlchemy()
DB_NAME = "database.db"
mongo_db = MongoEngine()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("../settings.py")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    # app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://jakesboo_books:eDbeQisxc9hgetSNeJLA@server/jakesboo_books"
    db.init_app(app)

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .mongo_models import User, BookEntry
    # create_database(app)
    mongo_db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.objects(id=id).first()

    return app


def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Created Database!")
