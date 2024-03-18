from flask import jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from sqlalchemy import or_

from app.models import Author, db


class AuthorsAPI(MethodView):
    @jwt_required()  # Require JWT for all methods
    def dispatch_request(self, *args, **kwargs):
        return super(AuthorsAPI, self).dispatch_request(*args, **kwargs)

    def get(self):
        query = Author.query  # Start with all authors

        # If a 'name' query parameter is provided, use 'like' for partial matching
        if "name" in request.args:
            name_search = "%{}%".format(request.args.get("name"))
            query = query.filter(Author.name.like(name_search))

        # Example sorting logic (adjust as needed, e.g., by 'name', 'view', etc.)
        sort_by = request.args.get("sort_by", "id")  # Default sorting is by 'id'
        order = request.args.get("order", "asc").lower()

        if sort_by in ["id", "name", "view", "fiction_count"]:
            query = (
                query.order_by(getattr(Author, sort_by).desc())
                if order == "desc"
                else query.order_by(getattr(Author, sort_by))
            )

        authors = [author.serialize() for author in query.all()]

        return jsonify(authors)

    def post(self):
        data = request.json

        # Validation (example, adjust as needed)
        if not data or "name" not in data:
            return jsonify({"error": "Missing required fields"}), 400

        # Create a new Author instance (adjust fields as necessary)
        new_author = Author(
            name=data.get("name"),
            birth_year=data.get("birth_year", None),
            author_page=data.get("author_page", ""),
            about=data.get("about", ""),
            email=data.get("email", ""),
            img=data.get("img", ""),
            fiction_count=data.get("fiction_count", 0),
            # Add or adjust other fields as necessary
        )

        db.session.add(new_author)
        db.session.commit()

        return jsonify(new_author.serialize()), 201


class SpecificAuthorAPI(MethodView):
    @jwt_required()  # Require JWT for all methods
    def dispatch_request(self, *args, **kwargs):
        return super(SpecificAuthorAPI, self).dispatch_request(*args, **kwargs)

    def get(self, author_id):
        author = Author.query.filter_by(id=author_id).first_or_404()
        return jsonify(author.serialize())

    # Implement POST method for specific author operations if necessary
    def post(self, author_id):
        pass
