from flask import jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from app.models import Fiction, db


class FictionsAPI(MethodView):
    @jwt_required()  # Require JWT for all methods
    def dispatch_request(self, *args, **kwargs):
        return super(FictionsAPI, self).dispatch_request(*args, **kwargs)

    def get(self):
        # Existing filter and sorting logic remains unchanged

        # Default filter is status="public"
        filter_args = {"status": "public"}

        # Update filter_args based on provided query parameters
        for key in ["status", "tag"]:
            if key in request.args:
                filter_args[key] = request.args.get(key)

        # Query the database with filters
        query = Fiction.query.filter_by(**filter_args)

        # Sorting logic remains unchanged
        sort_by = request.args.get("sort_by", "id")  # Default sorting is by 'id'
        order = request.args.get("order", "asc").lower()  # Default order is ascending

        if sort_by in ["id", "name", "publish_year", "view"]:
            if order == "desc":
                query = query.order_by(getattr(Fiction, sort_by).desc())
            else:
                query = query.order_by(getattr(Fiction, sort_by))

        # Change here: Use serialize method to include author details
        fictions = [fiction.serialize() for fiction in query.all()]

        return jsonify(fictions)

    def post(self):
        # Parse the JSON data from the request
        data = request.json

        # Simple validation (ensure to implement more robust validation for production)
        if not data or "name" not in data or "status" not in data:
            return jsonify({"error": "Missing required fields"}), 400

        # Create a new Fiction instance
        new_fiction = Fiction(
            name=data.get("name"),
            desc=data.get("desc", ""),
            cover=data.get("cover", ""),
            tag=data.get("tag", ""),
            publish_year=data.get("publish_year", 0),
            status=data.get("status"),
            view=data.get("view", 0),
            # Add other fields as necessary
        )

        # Add to session and commit to database
        db.session.add(new_fiction)
        db.session.commit()

        # Return the newly created fiction, using its serialize method to format the response
        return jsonify(new_fiction.serialize()), 201


class SpecificFictionAPI(MethodView):
    @jwt_required()  # Require JWT for all methods
    def dispatch_request(self, *args, **kwargs):
        return super(SpecificFictionAPI, self).dispatch_request(*args, **kwargs)

    def get(self, fiction_id):
        fiction = Fiction.query.filter_by(id=fiction_id).first_or_404()
        fiction.update_view()

        return jsonify(
            fiction.serialize(),  # Assuming you have a serialize method for your model
        )

    def post(self, fiction_id):

        pass
