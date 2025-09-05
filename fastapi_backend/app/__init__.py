from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from flask_migrate import Migrate

from .config import DefaultConfig
from .models import db
from .routes.health import blp as health_blp
from .routes.auth import blp as auth_blp
from .routes.notes import blp as notes_blp


# Create and configure the Flask application
app = Flask(__name__)
app.url_map.strict_slashes = False

# Load configuration
app.config.from_object(DefaultConfig)

# CORS
CORS(app, resources={r"/*": {"origins": app.config.get("CORS_ORIGINS", "*")}})

# API Docs (OpenAPI) configuration via flask-smorest
app.config["API_TITLE"] = "Notes Flask API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/docs"
app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

# Initialize extensions
api = Api(app)
app.config["API_SPEC_OPTIONS"] = {
    "x-tagGroups": [
        {"name": "Core", "tags": ["Healt Check", "Auth"]},
        {"name": "Notes", "tags": ["Notes"]},
    ]
}
db.init_app(app)
migrate = Migrate(app, db)

# Register blueprints
api.register_blueprint(health_blp)
api.register_blueprint(auth_blp)
api.register_blueprint(notes_blp)

# Ensure database tables are created for SQLite use
with app.app_context():
    db.create_all()
