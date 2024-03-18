import json
from datetime import datetime, timedelta

import requests
from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from werkzeug.security import generate_password_hash

from .common import *
from .models import User, db

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/authorized")
def authorized():
    incoming_data = json.loads(request.data.decode("UTF-8"))
    token = incoming_data["token"]
    auth = requests.get(FBURL + token)
    if auth.status_code == 200:
        r = auth.json()
        id = r["id"]
        avatar = r["picture"]["data"]["url"]
        user = User.query.filter_by(facebook=id).first()
        if user is None:
            new_user = User(
                facebook=id, avatar=avatar
            )  # Assuming your User model can store the Facebook ID and avatar URL
            db.session.add(new_user)
            db.session.commit()
            db.session.refresh(new_user)
            access_token = create_access_token(
                identity=id, expires_delta=timedelta(seconds=incoming_data["expired"])
            )
            return (
                jsonify(
                    access_token=access_token,
                    user_id=new_user.id,
                    message="User added and signed in",
                ),
                201,
            )
        else:
            if user.avatar != avatar:
                user.avatar = avatar
            user.last_seen = datetime.now()
            db.session.commit()
            access_token = create_access_token(
                identity=id, expires_delta=timedelta(seconds=incoming_data["expired"])
            )
            return (
                jsonify(
                    access_token=access_token,
                    user_id=user.id,
                    message="Signed in successfully",
                ),
                200,
            )
    else:
        return jsonify(message="Failed to sign in with Facebook"), 400


@auth_bp.route("/login", methods=["POST"])
def api_login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(user_name=username).first()
    if user and user.check_password(
        password
    ):  # Assuming you have a method like this in your User model
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Invalid username or password"}), 401


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt_identity()["jti"]  # Get the unique identifier for the token
    # Here you would mark the token as revoked in your database or cache
    return jsonify({"message": "Successfully logged out"}), 200


@auth_bp.route("/register", methods=["POST"])
def api_register():
    data = request.get_json()

    # Basic validation (expand according to your needs)
    errors = {}
    if not data.get("username"):
        errors["username"] = "Username is required."
    if not data.get("email"):
        errors["email"] = "Email is required."
    if not data.get("password"):
        errors["password"] = "Password is required."
    if data.get("password") != data.get("password2"):
        errors["password2"] = "Passwords do not match."

    if errors:
        return jsonify({"errors": errors}), 400

    # Check if user already exists
    user_exists = User.query.filter(
        (User.user_name == data["username"]) | (User.email == data["email"])
    ).first()
    if user_exists:
        return (
            jsonify({"message": "User already exists with given username or email."}),
            409,
        )

    # Create new user
    try:
        new_user = User(
            first_name=data["firstname"],
            last_name=data["lastname"],
            user_name=data["username"],
            email=data["email"],
            password_hash=generate_password_hash(data["password"]),
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Registration successful"}), 201
    except Exception as e:
        return jsonify({"message": "Registration failed", "error": str(e)}), 500
