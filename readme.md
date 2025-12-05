
# Recipe API – Flask + PostgreSQL

A RESTful API built with Flask, PostgreSQL and SQLalchemy, allowing users to save, rate, and manage recipes. The system includes full CRUD functionality for:

1. Users
2. Authors
3. Recipes
4. User Saved Recipes 

This project demonstrates backend API development using relational database modeling, blueprints, ORM models, validation, and password hashing.

# Table of Contents
- Project Overview
- Tech Stack 
- Features
- ERD Diagram
- Database Schema 
- Installation and Setup
- Running the Application
- API Endpoints 
-- Users
-- Authors
-- Recipes
-- Users Saved Recipes 
- Example Requests 
- Validation Rules
- Additional Notes
- Testing Checklist
- Future Improvements 

# Project Overview

This REST API allows users to:

- Create accounts (with secure hashed passwords)
- Save and rate recipes
- Manage authors and their recipes
- View recipes, filter by user, and attach personal notes

A relational PostgreSQL database is used with properly enforced foreign keys and a composite primary key junction table.

This API follows REST best practices with correct HTTP methods and status codes.

# Tech Stack

| Component          | Technology |
| ------------------ | ---------- |
| Backend Framework  | Flask      |
| Database           | PostgreSQL |
| ORM                | SQLAlchemy |
| Password Hashing   | Werkzeug   |
| API Client Testing | Insomnia   |
| Language           | Python 3   |

# Features

###  Users CRUD

- Create, read, update, delete users
- Password hashing (never storing raw passwords)

### Authors CRUD

- Add cookbook authors
- Update/delete them safely
- View all authors

### Recipes CRUD

- Store recipe details
- Enforce difficulty constraint (`easy`, `medium`, `hard`)
- `cook_time` stored as INTERVAL
- Linked to authors

### Saved Recipes System

- Users can save recipes
- Add recipe rating (between 1–5) and notes (e.g. original recipe was too salty, add half salt next time)
- Delete saved recipes
- Composite primary key ensures no duplicates
- Fully validated

### Data Validation

- Required fields checks
- Rating validation
- Unique email constraint
- Difficulty level constraint
- Validation for foreign keys

### Clean Code Architecture

- Blueprints for modular routes
- Models in separate file
- Central database initialization file (`database.py`)

# ERD Diagram

![ERD Diagram for Recipe API Server](<DEV1002-Recipe-API-Server-ERD.png>)

### Entities:

- Users
- Authors
- Recipes
- User_Saved_Recipes (junction table)

## Relationships:

- One Author ->  Many Recipes
- One User -> Many Saved Recipes
- One Recipe -> Many Saved Recipes
- User_Saved_Recipes has a composite primary key (user_id, recipe_id)
- `rating` and `notes` belong to a saved recipe

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

| Column           | Type         | Constraints              |
| ---------------- | ------------ | ------------------------ |
| recipe_id        | SERIAL       | PK                       |
| title            | VARCHAR(100) | NOT NULL                 |
| method           | TEXT         | NOT NULL                 |
| cook_time        | INTERVAL     | NOT NULL                 |
| difficulty_level | VARCHAR(20)  | CHECK (easy/medium/hard) |
| category         | VARCHAR(50)  | NULL                     |
| cuisine          | VARCHAR(50)  | NULL                     |
| author_id        | INTEGER      | FK → authors             |

---

### user_saved_recipes

| Column    | Type      | Constraints   |
| --------- | --------- | ------------- |
| user_id   | INTEGER   | PK, FK        |
| recipe_id | INTEGER   | PK, FK        |
| saved_at  | TIMESTAMP | DEFAULT now() |
| rating    | INTEGER   | CHECK (1–5)   |
| notes     | TEXT      | NULL          |

---

# Installation and Setup

## 1. Clone the repository

```bash
git clone <your-repo-url>
cd your-project-folder
```

## 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Create PostgreSQL database

Inside psql:

```sql
CREATE DATABASE recipe_api;
```

## 5. Configure database in `database.py`

Example:

```python
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:<password>@localhost:5432/recipe_api"
```

## 6. Initialise tables

Run:

```bash
python3 app.py
```

Flask + SQLAlchemy will create models automatically.

---

# Running the Application

Run:

```bash
python3 app.py
```

Your API runs at:

```
http://localhost:5000
```

---

# API Endpoints

## USERS

| Method | Endpoint    | Description    |
| ------ | ----------- | -------------- |
| GET    | /users/     | Get all users  |
| GET    | /users/<id> | Get user by ID |
| POST   | /users/     | Create user    |
| PUT    | /users/<id> | Update user    |
| DELETE | /users/<id> | Delete user    |

---

## AUTHORS

| Method | Endpoint      | Description     |
| ------ | ------------- | --------------- |
| GET    | /authors/     | Get all authors |
| GET    | /authors/<id> | Get author      |
| POST   | /authors/     | Create author   |
| PUT    | /authors/<id> | Update author   |
| DELETE | /authors/<id> | Delete author   |

---

## RECIPES

| Method | Endpoint      | Description     |
| ------ | ------------- | --------------- |
| GET    | /recipes/     | Get all recipes |
| GET    | /recipes/<id> | Get recipe      |
| POST   | /recipes/     | Create recipe   |
| PUT    | /recipes/<id> | Update recipe   |
| DELETE | /recipes/<id> | Delete recipe   |

---

## SAVED RECIPES

| Method | Endpoint              | Description              |
| ------ | --------------------- | ------------------------ |
| GET    | /saved/user/<user_id> | Get user's saved recipes |
| POST   | /saved/               | Save a recipe            |
| DELETE | /saved/               | Remove saved recipe      |

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

# Validation Rules

### Users

* Email must be unique
* Password stored hashed
* Required: first_name, last_name, email, password

### Recipes

* difficulty_level must be: `easy`, `medium`, `hard`
* cook_time must be an integer (minutes)
* author must exist

### Saved Recipes

* Cannot save the same recipe twice
* rating must be between 1–5
* notes optional

---

# Testing Checklist

### USERS

* [ ] POST /users
* [ ] GET /users
* [ ] GET /users/<id>
* [ ] PUT /users/<id>
* [ ] DELETE /users/<id>

### AUTHORS

* [ ] POST /authors
* [ ] GET /authors
* [ ] PUT /authors/<id>
* [ ] DELETE /authors/<id>

### RECIPES

* [ ] POST /recipes
* [ ] GET /recipes
* [ ] GET /recipes/<id>
* [ ] PUT /recipes/<id>
* [ ] DELETE /recipes/<id>

### SAVED

* [ ] POST /saved
* [ ] GET /saved/user/<id>
* [ ] DELETE /saved


# Future Improvements

- Add authentication (JWT tokens)
- Add categories/tags for recipes
- Add search filters
- Add pagination
- Add image uploads

---

# Final Notes / Summary

This project demonstrates full-stack backend development using Flask, SQLAlchemy, and PostgreSQL with proper relational design, validation, and structured API endpoints.
It adheres to REST principles and shows understanding of database modeling, foreign keys, and CRUD operations.

# Deployment 

## URL

```
https://dev1002-assessment3-web-api.onrender.com
```

Expected response:

```json
{ "message": "API is running and connected to PostgreSQL!" }
```

---

# Available Endpoints (Live)

### Authors

| Method | Endpoint               | Description               |
| ------ | ---------------------- | ------------------------- |
| GET    | `/authors/`            | Get all authors           |
| GET    | `/authors/<author_id>` | Get an author by ID       |
| POST   | `/authors/`            | Create a new author       |
| PUT    | `/authors/<author_id>` | Update an existing author |
| DELETE | `/authors/<author_id>` | Delete an author          |

---

### Recipes

| Method | Endpoint               | Description         |
| ------ | ---------------------- | ------------------- |
| GET    | `/recipes/`            | Get all recipes     |
| GET    | `/recipes/<recipe_id>` | Get a recipe by ID  |
| POST   | `/recipes/`            | Create a new recipe |
| PUT    | `/recipes/<recipe_id>` | Update a recipe     |
| DELETE | `/recipes/<recipe_id>` | Delete a recipe     |

---

### Users

| Method | Endpoint           | Description                         |
| ------ | ------------------ | ----------------------------------- |
| GET    | `/users/`          | Get all users                       |
| GET    | `/users/<user_id>` | Get a user by ID                    |
| POST   | `/users/`          | Create a new user (password hashed) |
| PUT    | `/users/<user_id>` | Update user details                 |
| DELETE | `/users/<user_id>` | Delete a user                       |


### User Saved Recipes

| Method | Endpoint                | Description                      |
| ------ | ----------------------- | -------------------------------- |
| GET    | `/saved/user/<user_id>` | Get all saved recipes for a user |
| POST   | `/saved/`               | Save a recipe for a user         |
| DELETE | `/saved/`               | Remove a saved recipe            |

# Deployment Notes

- This project uses Render Web Service + Render PostgreSQL for deployment.
- Environment variables are used to provide a secure `DATABASE_URL`.
- SQLAlchemy models reflect the schema defined in the ERD (included in README).
- Application uses Flask, Flask-SQLAlchemy, psycopg2, Gunicorn, and python-dotenv.
- Passwords are securely hashed. 

