from flask import Blueprint, request
from database import db
from models import Recipe, Author
from sqlalchemy import text
from datetime import timedelta

recipes_bp = Blueprint("recipes", __name__, url_prefix="/recipes")

# GET all recipes
@recipes_bp.get("/")
def get_recipes():
    recipes = Recipe.query.all()
    result = []

    for r in recipes:
        result.append({
            "recipe_id": r.recipe_id,
            "title": r.title,
            "method": r.method,
            "cook_time": str(r.cook_time),
            "difficulty_level": r.difficulty_level,
            "category": r.category,
            "cuisine": r.cuisine,
            "author_id": r.author_id
        })

    return result, 200


# GET recipe by ID
@recipes_bp.get("/<int:recipe_id>")
def get_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)

    if not recipe:
        return {"error": "Recipe not found"}, 404

    return {
        "recipe_id": recipe.recipe_id,
        "title": recipe.title,
        "method": recipe.method,
        "cook_time": str(recipe.cook_time),
        "difficulty_level": recipe.difficulty_level,
        "category": recipe.category,
        "cuisine": recipe.cuisine,
        "author_id": recipe.author_id
    }, 200


# CREATE recipe (POST)
@recipes_bp.post("/")
def create_recipe():
    data = request.get_json()

    required = ["title", "method", "cook_time", "difficulty_level", "author_id"]
    for field in required:
        if field not in data:
            return {"error": f"Missing field: {field}"}, 400

    # VALIDATE difficulty level
    if data["difficulty_level"] not in ["easy", "medium", "hard"]:
        return {"error": "difficulty_level must be: easy, medium, or hard"}, 400

    # VALIDATE author exists
    author = Author.query.get(data["author_id"])
    if not author:
        return {"error": "Author does not exist"}, 400

    # Convert cook_time (expecting minutes as integer)
    try:
        cook_time_minutes = int(data["cook_time"])
    except (TypeError, ValueError):
        return {"error": "cook_time must be an integer number of minutes"}, 400

    new_recipe = Recipe(
        title=data["title"],
        method=data["method"],
        cook_time=timedelta(minutes=cook_time_minutes),
        difficulty_level=data["difficulty_level"],
        category=data.get("category"),
        cuisine=data.get("cuisine"),
        author_id=data["author_id"]
    )

    db.session.add(new_recipe)
    db.session.commit()

    return {
        "message": "Recipe created successfully",
        "recipe_id": new_recipe.recipe_id
    }, 201


# UPDATE recipe (PUT)
@recipes_bp.put("/<int:recipe_id>")
def update_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)

    if not recipe:
        return {"error": "Recipe not found"}, 404

    data = request.get_json() or {}

    # Optional updates
    if "title" in data:
        recipe.title = data["title"]

    if "method" in data:
        recipe.method = data["method"]

    if "cook_time" in data:
        try:
            cook_time_minutes = int(data["cook_time"])
            recipe.cook_time = timedelta(minutes=cook_time_minutes)
        except (TypeError, ValueError):
            return {"error": "cook_time must be an integer number of minutes"}, 400

    if "difficulty_level" in data:
        if data["difficulty_level"] not in ["easy", "medium", "hard"]:
            return {"error": "difficulty_level must be: easy, medium, or hard"}, 400
        recipe.difficulty_level = data["difficulty_level"]

    if "category" in data:
        recipe.category = data["category"]

    if "cuisine" in data:
        recipe.cuisine = data["cuisine"]

    if "author_id" in data:
        author = Author.query.get(data["author_id"])
        if not author:
            return {"error": "Author does not exist"}, 400
        recipe.author_id = data["author_id"]

    db.session.commit()

    return {"message": "Recipe updated successfully"}, 200


# DELETE recipe
@recipes_bp.delete("/<int:recipe_id>")
def delete_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)

    if not recipe:
        return {"error": "Recipe not found"}, 404

    db.session.delete(recipe)
    db.session.commit()

    return {"message": "Recipe deleted successfully"}, 200
