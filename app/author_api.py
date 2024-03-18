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

        # Extract page and page_size from query parameters
        page = request.args.get("page", 1, type=int)
        page_size = request.args.get("page_size", 10, type=int)

        # Check if an 'ids' query parameter is provided for fetching specific authors by IDs
        if "ids" in request.args:
            ids_str = request.args.get("ids")
            try:
                ids = [int(id) for id in ids_str.split(",")]
                query = query.filter(Author.id.in_(ids))
            except ValueError:
                return jsonify({"error": "Invalid ID format"}), 400

        # Partial name matching
        elif "name" in request.args:
            name_search = "%{}%".format(request.args.get("name"))
            query = query.filter(Author.name.like(name_search))

        # Sorting logic
        sort_by = request.args.get("sort_by", "id")  # Default sorting is by 'id'
        order = request.args.get("order", "asc").lower()

        if sort_by in ["id", "name", "view", "fiction_count"]:
            query = (
                query.order_by(getattr(Author, sort_by).desc())
                if order == "desc"
                else query.order_by(getattr(Author, sort_by))
            )

        # Apply pagination
        pagination = query.paginate(page=page, per_page=page_size, error_out=False)
        authors = [author.serialize() for author in pagination.items]

        # Return paginated results along with pagination metadata
        return jsonify(
            {
                "authors": authors,
                "total": pagination.total,
                "pages": pagination.pages,
                "page": page,
                "per_page": page_size,
            }
        )

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
