from flask import Blueprint, abort, render_template
from flask_login import current_user
from jinja2 import TemplateNotFound

from app.models import Fiction

recommendation = Blueprint("recommendation", __name__, template_folder="templates")


@recommendation.route("/suggested_authors", defaults={"page": "index"})
@recommendation.route("/recommend/author/")
def show():
    try:
        top_authors = current_user.get_recommend_authors()
        return render_template(
            "authors.html",
            authors=top_authors,
            top_authors=top_authors,
            title="All Authors",
        )
    except TemplateNotFound:
        abort(404)


@recommendation.route("/fictions/recommend/")
def fiction_with_recommendation():
    try:
        if current_user.is_authenticated:
            suggested_fictions = current_user.get_recommend_fictions()
        else:
            suggested_fictions = []
        fictions = Fiction.query.filter_by(status="public")
        return render_template(
            "fictions/list_fiction.html",
            fictions=fictions,
            suggested_fictions=suggested_fictions,
        )
    except TemplateNotFound:
        abort(404)
