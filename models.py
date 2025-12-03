from database import db
from datetime import datetime
from sqlalchemy import CheckConstraint


# AUTHOR TABLE

class Author(db.Model):
    __tablename__ = "author"   

    author_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    social_media_link = db.Column(db.Text, nullable=True)

    recipes = db.relationship("Recipe", back_populates="author")



# USER TABLE

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)

    saved_recipes = db.relationship(
        "UserSavedRecipes", back_populates="user", cascade="all, delete"
    )

# RECIPE TABLE
class Recipe(db.Model):
    __tablename__ = "recipes"

    recipe_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    method = db.Column(db.Text, nullable=False)
    cook_time = db.Column(db.Interval, nullable=False)
    difficulty_level = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(50))
    cuisine = db.Column(db.String(50))

    __table_args__ = (
        CheckConstraint(
            "difficulty_level IN ('easy', 'medium', 'hard')",
            name="check_difficulty"
        ),
    )

    author_id = db.Column(db.Integer, db.ForeignKey("author.author_id"), nullable=False)

    author = db.relationship("Author", back_populates="recipes")

    saved_by = db.relationship("UserSavedRecipes", back_populates="recipe")


# USER SAVED RECIPES (JUNCTION)

class UserSavedRecipes(db.Model):
    __tablename__ = "user_saved_recipes"

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.recipe_id"), primary_key=True)
    saved_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    rating = db.Column(db.Integer)    # 1–5, optional
    notes = db.Column(db.Text)        # optional

    user = db.relationship("User", back_populates="saved_recipes")
    recipe = db.relationship("Recipe", back_populates="saved_by")

