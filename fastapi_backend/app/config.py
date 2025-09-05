import os
from datetime import timedelta


class Config:
    """Base configuration for the Flask app."""
    # PUBLIC_INTERFACE
    def init_app(self, app):
        """This is a public function that applies configuration to the Flask app."""
        pass


class DefaultConfig(Config):
    """Default configuration using environment variables."""
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "change-me-in-production")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///notes.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True

    # JWT settings
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me-too")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_EXPIRES_MIN = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_MIN", "60"))
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRES_MIN)

    # CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
