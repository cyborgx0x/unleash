from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


from app.extensions import db, login
from app.recommendation.main import recommendation

from .configuration import Config

load_dotenv()


def register_extensions(app):
    db.init_app(app)
    login.init_app(app)
    login.login_view = "login"
    migrate = Migrate(app, db)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(recommendation)

    register_extensions(app)

    return app


app = create_app(Config)

from app import models, routes
