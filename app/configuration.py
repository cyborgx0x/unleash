import os

from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

DB_USERNAME = os.environ.get("DB_USERNAME", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "123456")
DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_TABLE = os.environ.get("DB_TABLE", "unleash")

if DB_USERNAME == "root":
    q = "sqlite:///unleash.db"
else:
    q = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_TABLE}"


class Config(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///unleash.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
