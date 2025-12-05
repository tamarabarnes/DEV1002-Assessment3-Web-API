
# Recipe API – Flask + PostgreSQL

- A RESTful API built with Flask, PostgreSQL, and SQLAlchemy, allowing users to manage recipes, authors, user accounts, and saved recipes.
- It supports full CRUD operations across all major resources and demonstrates relational database modelling, data validation, ORM usage, password hashing, and cloud deployment.


# Table of Contents

- Project Overview
- Tech Stack
- Features
- ERD Diagram
- Database Schema
- Database Choice: Why PostgreSQL?
- Installation and Setup
- Running the Application
- API Endpoints
- Example Requests
- Validation Rules
- Testing Checklist
- Future Improvements
- Deployment
- Live Endpoints
- Deployment Notes

# Project Overview

This REST API allows users to:

* Create accounts (with securely hashed passwords)
* Save, rate, and annotate their favourite recipes
* Manage authors who created the recipes
* View, update, and delete recipes
* Retrieve saved recipes by user

- A relational PostgreSQL database is used, enforcing data integrity through foreign keys, composite keys, and validation rules.
The API follows REST best practices with correct HTTP methods and HTTP status codes.

# Tech Stack

| Component          | Technology |
| ------------------ | ---------- |
| Backend Framework  | Flask      |
| Database           | PostgreSQL |
| ORM                | SQLAlchemy |
| Password Hashing   | Werkzeug   |
| API Testing Client | Insomnia   |
| Language           | Python 3   |
| Deployment         | Render     |


# Features

###  Users CRUD

- Create, read, update, delete users
- Passwords stored hashed (never in plain-text)

### Authors CRUD

* Add and manage recipe authors
* Optional social media link
* Safe updates and deletions

### Recipes CRUD

- Store recipe details
- Validate difficulty level (`easy`, `medium`, `hard`)
- `cook_time` stored as an SQL `INTERVAL`
- Strict foreign key linking to authors

### Saved Recipes System

- Users can save recipes with:
  - Personal rating (1–5)
  - Personal notes
  - Timestamp (`saved_at`)
- Composite key (`user_id`, `recipe_id`) prevents duplicates
- Full validation and safe deletion

### Clean Architecture

- Routes organised via Blueprints
- Centralised DB initialisation (`database.py`)
- ORM models defined clearly in `models.py`

# ERD Diagram

![ERD Diagram for Recipe API Server](<DEV1002-Recipe-API-Server-ERD.png>)

# Key Relationships:

- One Author → Many Recipes
- One User → Many Saved Recipes
- One Recipe → Many Saved Recipes
- `user_saved_recipes` = junction table with composite primary key

---

# Database Schema

### Users

| Column          | Type         | Constraints      |
| --------------- | ------------ | ---------------- |
| user_id         | SERIAL       | PK               |
| first_name      | VARCHAR(100) | NOT NULL         |
| last_name       | VARCHAR(100) | NOT NULL         |
| email           | VARCHAR(255) | UNIQUE, NOT NULL |
| hashed_password | VARCHAR(255) | NOT NULL         |

---

### Author

| Column            | Type         | Constraints |
| ----------------- | ------------ | ----------- |
| author_id         | SERIAL       | PK          |
| first_name        | VARCHAR(100) | NOT NULL    |
| last_name         | VARCHAR(100) | NOT NULL    |
| social_media_link | TEXT         | NULL        |

---

### Recipes

| Column           | Type         | Constraints  |
| ---------------- | ------------ | ------------ |
| recipe_id        | SERIAL       | PK           |
| title            | VARCHAR(100) | NOT NULL     |
| method           | TEXT         | NOT NULL     |
| cook_time        | INTERVAL     | NOT NULL     |
| difficulty_level | VARCHAR(20)  | CHECK (…)    |
| category         | VARCHAR(50)  | NULL         |
| cuisine          | VARCHAR(50)  | NULL         |
| author_id        | INTEGER      | FK → authors |

---

### user_saved_recipes (Junction Table)

| Column    | Type      | Constraints   |
| --------- | --------- | ------------- |
| user_id   | INTEGER   | PK, FK        |
| recipe_id | INTEGER   | PK, FK        |
| saved_at  | TIMESTAMP | DEFAULT now() |
| rating    | INTEGER   | CHECK (1–5)   |
| notes     | TEXT      | NULL          |

---

# Database Choice: Why PostgreSQL?

PostgreSQL was chosen because it is a highly reliable, ACID-compliant relational database that supports strong data consistency—important for this API, which depends on relationships between users, recipes, authors, and saved recipes.

Compared to MongoDB (a NoSQL database):

| PostgreSQL                         | MongoDB                                 |
| ---------------------------------- | --------------------------------------- |
| Relational (tables & foreign keys) | Document-oriented (JSON-like BSON)      |
| Strong schema, strict structure    | Flexible schema                         |
| Enforces relationships             | No foreign keys                         |
| Excellent for complex joins        | Excellent for dynamic/unstructured data |

# Why PostgreSQL fits this project:

* Clear, enforced relationships between tables
* Guaranteed referential integrity
* Support for constraints (unique emails, difficulty checks, composite keys)
* Strong SQL capabilities

MongoDB is better for evolving, unstructured data, but this project requires consistent, relational modelling — making PostgreSQL the ideal fit.


# Installation and Setup**

## 1. Clone the repository

```bash
git clone <your-repo-url>
cd your-project-folder
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Create PostgreSQL database

```sql
CREATE DATABASE recipe_api;
```

## 5. Configure database in `.env` or `database.py`

Example:

```
DATABASE_URL=postgresql://postgres:<password>@localhost:5432/recipe_api
```

## 6. Initialise tables

```bash
python3 app.py
```

---

# Running the Application

```bash
python3 app.py
```

API accessible at:

```
http://localhost:5000
```

---

# API Endpoints

## USERS

| Method | Endpoint      | Description    |
| ------ | ------------- | -------------- |
| GET    | `/users/`     | Get all users  |
| GET    | `/users/<id>` | Get user by ID |
| POST   | `/users/`     | Create user    |
| PUT    | `/users/<id>` | Update user    |
| DELETE | `/users/<id>` | Delete user    |

---

## AUTHORS

| Method | Endpoint        | Description     |
| ------ | --------------- | --------------- |
| GET    | `/authors/`     | Get all authors |
| GET    | `/authors/<id>` | Get author      |
| POST   | `/authors/`     | Create author   |
| PUT    | `/authors/<id>` | Update author   |
| DELETE | `/authors/<id>` | Delete author   |

---

## RECIPES

| Method | Endpoint        | Description     |
| ------ | --------------- | --------------- |
| GET    | `/recipes/`     | Get all recipes |
| GET    | `/recipes/<id>` | Get recipe      |
| POST   | `/recipes/`     | Create recipe   |
| PUT    | `/recipes/<id>` | Update recipe   |
| DELETE | `/recipes/<id>` | Delete recipe   |

---

## SAVED RECIPES

| Method | Endpoint           | Description         |
| ------ | ------------------ | ------------------- |
| GET    | `/saved/user/<id>` | Get saved recipes   |
| POST   | `/saved/`          | Save recipe         |
| DELETE | `/saved/`          | Remove saved recipe |

---

# Example Requests

### Create a User

```json
{
  "first_name": "Tamara",
  "last_name": "Barnes",
  "email": "tamara@example.com",
  "password": "Password123!"
}
```

### Save a Recipe

```json
{
  "user_id": 2,
  "recipe_id": 1,
  "rating": 5,
  "notes": "Reduce chilli by half next time."
}
```

---

# Validation Rules

### Users

- Email must be **unique**
- Password stored **hashed**
- Required fields: first_name, last_name, email, password

### Recipes

- Difficulty must be: `easy`, `medium`, `hard`
- cook_time must be an integer (minutes)
- author_id must exist

### Saved Recipes

- Recipe cannot be saved twice
- Rating 1–5
- Notes optional

---

# Testing Checklist

### USERS

-  [x] POST /users
-  [x] GET /users
-  [x] GET /users/<id>
-  [x] PUT /users/<id>
-  [x] DELETE /users/<id>

### AUTHORS

- [x] POST /authors
- [x] GET /authors
- [x] PUT /authors/<id>
- [x] DELETE /authors/<id>

### RECIPES

- [x] POST /recipes
- [x] GET /recipes
- [x] GET /recipes/<id>
- [x] PUT /recipes/<id>
- [x] DELETE /recipes/<id>

### SAVED RECIPES

- [x] POST /saved
- [x] GET /saved/user/<id>
- [x] DELETE /saved

---

# Future Improvements

- Add JWT authentication
- Add filters or search (e.g., cuisine, difficulty)
- Add pagination
- Add image uploads
- Add admin roles
- Add separate ingredients table

---

# Deployment

Your API is deployed using **Render Web Service + Render PostgreSQL**.

### Live Base URL

```
https://dev1002-assessment3-web-api.onrender.com
```

### Health Check

```
{ "message": "API is running and connected to PostgreSQL!" }
```

---

# Live Endpoints

(These mirror the local endpoints and are fully functional.)

- `GET https://dev1002-assessment3-web-api.onrender.com/authors/`
- `POST https://dev1002-assessment3-web-api.onrender.com/users/`
- etc.

---

# Deployment Notes

- Uses Render's **Internal Database URL** via environment variables
- Gunicorn is used as the production WSGI server
- SQLAlchemy auto-creates tables if they do not exist
- `.gitignore` excludes venv and cached files
- All dependencies listed in `requirements.txt`
- Passwords are hashed using Werkzeug’s secure hashing

---

# Final Summary

This project demonstrates full backend development with:

- Flask routing
- ORM models
- SQL relational design
- Password hashing
- Input validation
- CRUD operations
- Deployment to a production server
- Clear documentation
