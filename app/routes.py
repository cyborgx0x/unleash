import json
from datetime import datetime, timedelta

import requests
from flask import jsonify, request, session
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
)


from app import app, db


from .auth import auth_bp
from .author_api import AuthorsAPI, SpecificAuthorAPI
from .chapter_api import ChaptersAPI, SpecificChapterAPI
from .common import *
from .fiction_api import FictionsAPI, SpecificFictionAPI

allowed_origins = [
    "http://localhost:5173",
    "http://localhost",
    "https://unleash.asia",
    "http://localhost:5000",
]
CORS(app, resources={r"/*": {"origins": allowed_origins}})

app.config["JWT_SECRET_KEY"] = "your_jwt_secret_key"
jwt = JWTManager(app)
app.register_blueprint(auth_bp)

app.add_url_rule(
    "/chapters", view_func=ChaptersAPI.as_view("chapters_api"), methods=["GET", "POST"]
)
app.add_url_rule(
    "/chapters/<int:chapter_id>/",
    view_func=SpecificChapterAPI.as_view("specific_chapter_api"),
)
app.add_url_rule(
    "/fictions", view_func=FictionsAPI.as_view("fictions_api"), methods=["GET", "POST"]
)
app.add_url_rule(
    "/fictions/<int:fiction_id>/",
    view_func=SpecificFictionAPI.as_view("specific_fiction_api"),
)
app.add_url_rule(
    "/authors", view_func=AuthorsAPI.as_view("authors_api"), methods=["GET", "POST"]
)
app.add_url_rule(
    "/authors/<int:author_id>/",
    view_func=SpecificAuthorAPI.as_view("specific_author_api"),
)
