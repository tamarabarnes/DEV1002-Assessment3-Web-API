from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

db = SQLAlchemy()

def init_db(app: Flask):
    # Try to read DATABASE_URL from environment (Render uses this)
    DATABASE_URL = os.environ.get("DATABASE_URL")

    # Fallback for local development (your local Postgres)
    if not DATABASE_URL:
        DATABASE_URL = "postgresql://postgres:Sashimi123!@localhost:5432/recipe_api"

    # Fix the postgres:// prefix that Render uses
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    # Configure SQLAlchemy
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialise DB
    db.init_app(app)

    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

# Import models AFTER db is created to avoid circular import
from models import Author, User, Recipe, UserSavedRecipes

