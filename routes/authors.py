from flask import Blueprint, request
from database import db
from models import Author

authors_bp = Blueprint("authors", __name__, url_prefix="/authors")


# GET all authors
@authors_bp.get("/")
def get_authors():
    authors = Author.query.all()
    result = []

    for a in authors:
        result.append({
            "author_id": a.author_id,
            "first_name": a.first_name,
            "last_name": a.last_name,
            "social_media_link": a.social_media_link
        })

    return result, 200

# GET single author by ID
@authors_bp.get("/<int:author_id>")
def get_author(author_id):

    author = Author.query.get(author_id)

    if not author:
        return {"error": "Author not found"}, 404

    return {
        "author_id": author.author_id,
        "first_name": author.first_name,
        "last_name": author.last_name,
        "social_media_link": author.social_media_link
    }, 200


# CREATE a new author (POST)
@authors_bp.post("/")
def create_author():

    data = request.get_json()

    # Validation
    required_fields = ["first_name", "last_name"]
    for field in required_fields:
        if field not in data:
            return {"error": f"Missing field: {field}"}, 400

    new_author = Author(
        first_name=data["first_name"],
        last_name=data["last_name"],
        social_media_link=data.get("social_media_link")  # optional
    )

    db.session.add(new_author)
    db.session.commit()

    return {
        "message": "Author created successfully",
        "author_id": new_author.author_id
    }, 201


# UPDATE author (PUT)
@authors_bp.put("/<int:author_id>")
def update_author(author_id):
    author = Author.query.get(author_id)

    if not author:
        return {"error": "Author not found"}, 404

    data = request.get_json()

    author.first_name = data.get("first_name", author.first_name)
    author.last_name = data.get("last_name", author.last_name)
    author.social_media_link = data.get("social_media_link", author.social_media_link)

    db.session.commit()

    return {
        "message": "Author updated successfully",
        "author_id": author.author_id,
        "first_name": author.first_name,
        "last_name": author.last_name,
        "social_media_link": author.social_media_link
    }, 200


# DELETE author
@authors_bp.delete("/<int:author_id>")
def delete_author(author_id):
    author = Author.query.get(author_id)

    if not author:
        return {"error": "Author not found"}, 404

    db.session.delete(author)
    db.session.commit()

    return {"message": "Author deleted successfully"}, 200
