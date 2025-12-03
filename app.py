from flask import Flask
from database import init_db
from routes.authors import authors_bp
from routes.recipes import recipes_bp
from routes.users import users_bp
from routes.saved_recipes import saved_recipes_bp

app = Flask(__name__)

# CONNECT DATABASE
init_db(app)

# REGISTER BLUEPRINTS
app.register_blueprint(authors_bp)
app.register_blueprint(recipes_bp)
app.register_blueprint(users_bp)
app.register_blueprint(saved_recipes_bp)

@app.get("/")
def home():
    return {"message": "API is running and connected to PostgreSQL!"}

if __name__ == "__main__":
    app.run(debug=True)

