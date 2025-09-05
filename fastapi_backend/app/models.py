from datetime import datetime
from typing import Optional

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    """User model representing application users."""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    notes = db.relationship("Note", backref="owner", lazy=True, cascade="all, delete-orphan")

    # PUBLIC_INTERFACE
    def set_password(self, password: str) -> None:
        """Set (hash) the user's password securely."""
        self.password_hash = generate_password_hash(password)

    # PUBLIC_INTERFACE
    def check_password(self, password: str) -> bool:
        """Verify the user's password."""
        return check_password_hash(self.password_hash, password)


class Note(db.Model):
    """Note model tied to a user."""
    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, default="Untitled")
    content = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # PUBLIC_INTERFACE
    def update(self, title: Optional[str] = None, content: Optional[str] = None) -> None:
        """Update note fields if provided."""
        if title is not None:
            self.title = title
        if content is not None:
            self.content = content
