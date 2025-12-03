from flask import Blueprint, request
from database import db
from models import User
from werkzeug.security import generate_password_hash

users_bp = Blueprint("users", __name__, url_prefix="/users")

# GET all users
@users_bp.get("/")
def get_users():
    users = User.query.all()
    results = []

    for u in users:
        results.append({
            "user_id": u.user_id,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "email": u.email
        })

    return results, 200


# -------------------------
# GET user by ID
# -------------------------
@users_bp.get("/<int:user_id>")
def get_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return {"error": "User not found"}, 404

    return {
        "user_id": user.user_id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email
    }, 200

# CREATE user (POST)
@users_bp.post("/")
def create_user():
    data = request.get_json()

    required = ["first_name", "last_name", "email", "password"]
    for field in required:
        if field not in data:
            return {"error": f"Missing field: {field}"}, 400

    # Check if email already exists
    existing = User.query.filter_by(email=data["email"]).first()
    if existing:
        return {"error": "Email already exists"}, 400

    hashed_pw = generate_password_hash(data["password"])

    new_user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        hashed_password=hashed_pw
    )

    db.session.add(new_user)
    db.session.commit()

    return {
        "message": "User created successfully",
        "user_id": new_user.user_id
    }, 201


# -------------------------
# UPDATE user
# -------------------------
@users_bp.put("/<int:user_id>")
def update_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return {"error": "User not found"}, 404

    data = request.get_json() or {}

    if "first_name" in data:
        user.first_name = data["first_name"]

    if "last_name" in data:
        user.last_name = data["last_name"]

    if "email" in data:
        # Check for new email conflict
        existing = User.query.filter_by(email=data["email"]).first()
        if existing and existing.user_id != user.user_id:
            return {"error": "Email already exists"}, 400
        user.email = data["email"]

    if "password" in data:
        user.hashed_password = generate_password_hash(data["password"])

    db.session.commit()

    return {"message": "User updated successfully"}, 200


# -------------------------
# DELETE user
# -------------------------
@users_bp.delete("/<int:user_id>")
def delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return {"error": "User not found"}, 404

    db.session.delete(user)
    db.session.commit()

    return {"message": "User deleted successfully"}, 200
