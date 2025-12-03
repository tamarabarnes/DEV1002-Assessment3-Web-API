from flask import Blueprint, request
from database import db
from models import UserSavedRecipes, User, Recipe
from datetime import datetime

saved_recipes_bp = Blueprint("saved_recipes", __name__, url_prefix="/saved")


# GET all saved recipes for a user
@saved_recipes_bp.get("/user/<int:user_id>")
def get_saved_recipes(user_id):
    user = User.query.get(user_id)

    if not user:
        return {"error": "User not found"}, 404

    saved_list = []

    for saved in user.saved_recipes:
        saved_list.append({
            "user_id": saved.user_id,
            "recipe_id": saved.recipe_id,
            "saved_at": saved.saved_at.isoformat(),
            "recipe_title": saved.recipe.title,
            "recipe_cuisine": saved.recipe.cuisine,
            "rating": saved.rating,
            "notes": saved.notes
        })

    return saved_list, 200


# SAVE a recipe for a user (POST)
@saved_recipes_bp.post("/")
def save_recipe():
    data = request.get_json()

    required = ["user_id", "recipe_id"]
    for field in required:
        if field not in data:
            return {"error": f"Missing field: {field}"}, 400

    user = User.query.get(data["user_id"])
    if not user:
        return {"error": "User does not exist"}, 404

    recipe = Recipe.query.get(data["recipe_id"])
    if not recipe:
        return {"error": "Recipe does not exist"}, 404

    # Check if already saved
    existing = UserSavedRecipes.query.get((data["user_id"], data["recipe_id"]))
    if existing:
        return {"error": "Recipe already saved"}, 400

    # Optional rating validation (1–5)
    rating = data.get("rating")
    if rating is not None:
        try:
            rating = int(rating)
        except (TypeError, ValueError):
            return {"error": "rating must be an integer between 1 and 5"}, 400
        if rating < 1 or rating > 5:
            return {"error": "rating must be between 1 and 5"}, 400

    new_saved = UserSavedRecipes(
        user_id=data["user_id"],
        recipe_id=data["recipe_id"],
        saved_at=datetime.utcnow(),
        rating=rating,               # validated or None
        notes=data.get("notes")      # optional
    )

    db.session.add(new_saved)
    db.session.commit()

    return {"message": "Recipe saved successfully"}, 201


# DELETE a saved recipe
@saved_recipes_bp.delete("/")
def delete_saved_recipe():
    data = request.get_json()

    required = ["user_id", "recipe_id"]
    for field in required:
        if field not in data:
            return {"error": f"Missing field: {field}"}, 400

    saved = UserSavedRecipes.query.get((data["user_id"], data["recipe_id"]))

    if not saved:
        return {"error": "Saved recipe not found"}, 404

    db.session.delete(saved)
    db.session.commit()

    return {"message": "Saved recipe removed"}, 200

