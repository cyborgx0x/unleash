from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from flask_login import current_user

recommendation = Blueprint("recommendation", __name__, template_folder="templates")


@recommendation.route("/suggested_authors", defaults={"page": "index"})
@recommendation.route("/recommend/author/")
def show():
    try:
        
        top_authors = current_user.get_recommend_authors()
        return render_template(
            "authors.html", authors=top_authors, top_authors=top_authors, title="All Authors"
        )
    except TemplateNotFound:
        abort(404)
