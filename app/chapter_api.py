from flask import jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from app.models import Chapter, db  # Adjust the import path as needed


class ChaptersAPI(MethodView):
    @jwt_required()  # Require JWT for all methods
    def dispatch_request(self, *args, **kwargs):
        return super(ChaptersAPI, self).dispatch_request(*args, **kwargs)

    def get(self, fiction_id=None):
        # If a fiction_id is provided, filter chapters by that ID; otherwise, fetch all chapters
        if fiction_id:
            chapters = Chapter.query.filter_by(fiction=fiction_id).all()
        else:
            chapters = Chapter.query.all()
        return jsonify([chapter.serialize() for chapter in chapters])

    def post(self):
        data = request.json
        if (
            not data
            or "name" not in data
            or "content" not in data
            or "fiction_id" not in data
        ):
            return jsonify({"error": "Missing required fields"}), 400

        new_chapter = Chapter(
            name=data.get("name"),
            content=data.get("content"),
            view_count=data.get("view_count", 0),
            fiction=data.get("fiction_id"),
            chapter_order=data.get("chapter_order", 1),
            # Add other fields as necessary
        )

        db.session.add(new_chapter)
        db.session.commit()

        return jsonify(new_chapter.serialize()), 201


class SpecificChapterAPI(MethodView):
    @jwt_required()  # Require JWT for all methods
    def dispatch_request(self, *args, **kwargs):
        return super(SpecificChapterAPI, self).dispatch_request(*args, **kwargs)

    def get(self, chapter_id):
        chapter = Chapter.query.filter_by(id=chapter_id).first_or_404()
        if not chapter:
            return jsonify(chapter={}, fiction=[], chapters=[])

        fiction = chapter.fiction_r
        chapters = Chapter.query.filter_by(fiction=fiction.id).all()
        return jsonify(
            chapter=chapter.serialize(),
            fiction=fiction.serialize(),
            chapters=[chapter.serialize() for chapter in chapters],
        )

    # Add POST logic if needed for specific chapters


# Ensure to implement a serialize method in the Chapter model similar to previous models
