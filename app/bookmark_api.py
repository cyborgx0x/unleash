from flask import jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Bookmark, User, Chapter, db  # Make sure to import Chapter if needed for validation

class BookmarkAPI(MethodView):
    @jwt_required()
    def get(self, chapter_id):
        username = get_jwt_identity()
        
        user = User.query.filter_by(user_name=username).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        bookmark = Bookmark.query.filter_by(user_id=user.id, chapter_id=chapter_id).first()
        
        is_bookmarked = bookmark is not None
        return jsonify({"isBookmarked": is_bookmarked})

    @jwt_required()
    def post(self, chapter_id):
        username = get_jwt_identity()
        
        # Fetch the user based on username
        user = User.query.filter_by(user_name=username).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Validate chapter_id
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return jsonify({"error": "Chapter not found"}), 404
        
        # Check if the bookmark already exists
        existing_bookmark = Bookmark.query.filter_by(user_id=user.id, chapter_id=chapter_id).first()
        if existing_bookmark:
            return jsonify({"error": "Bookmark already exists"}), 400

        # Create a new bookmark
        new_bookmark = Bookmark(user_id=user.id, chapter_id=chapter_id)
        db.session.add(new_bookmark)
        try:
            db.session.commit()
            return jsonify({"message": "Bookmark added successfully", "isBookmarked": True}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Could not add bookmark"}), 500
