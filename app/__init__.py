from .configuration import Config
from flask import Flask

from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flaskext.markdown import Markdown
from dotenv import load_dotenv
from app.recommendation import recommendation
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(recommendation)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
login = LoginManager(app)
login.login_view = 'login'
Markdown(app)


from app import models, routes
