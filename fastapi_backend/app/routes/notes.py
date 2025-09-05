from flask import request
from flask_smorest import Blueprint, abort
from flask.views import MethodView

from ..auth import jwt_required
from ..models import db, Note
from ..schemas import NoteSchema, NoteCreateRequest, NoteUpdateRequest, ErrorSchema

blp = Blueprint(
    "Notes",
    "notes",
    url_prefix="/notes",
    description="Manage personal notes. All endpoints require JWT Bearer token.",
)


@blp.route("")
class NotesCollection(MethodView):
    @jwt_required
    @blp.response(200, NoteSchema(many=True))
    def get(self):
        """List all notes for the authenticated user."""
        user_id = request.user_id
        notes = Note.query.filter_by(owner_id=user_id).order_by(Note.updated_at.desc()).all()
        return notes

    @jwt_required
    @blp.arguments(NoteCreateRequest, location="json")
    @blp.response(201, NoteSchema)
    @blp.alt_response(400, ErrorSchema)
    def post(self, payload):
        """Create a new note for the authenticated user."""
        user_id = request.user_id
        title = payload.get("title")
        content = payload.get("content")

        note = Note(title=title, content=content, owner_id=user_id)
        db.session.add(note)
        db.session.commit()
        return note


@blp.route("/<int:note_id>")
class NoteItem(MethodView):
    @jwt_required
    @blp.response(200, NoteSchema)
    @blp.alt_response(404, ErrorSchema)
    def get(self, note_id: int):
        """Retrieve a single note by id (must belong to the user)."""
        user_id = request.user_id
        note = Note.query.filter_by(id=note_id, owner_id=user_id).first()
        if not note:
            abort(404, message="Note not found")
        return note

    @jwt_required
    @blp.arguments(NoteUpdateRequest, location="json")
    @blp.response(200, NoteSchema)
    @blp.alt_response(404, ErrorSchema)
    def put(self, payload, note_id: int):
        """Replace/update a note (title/content)."""
        user_id = request.user_id
        note = Note.query.filter_by(id=note_id, owner_id=user_id).first()
        if not note:
            abort(404, message="Note not found")
        note.update(title=payload.get("title"), content=payload.get("content"))
        db.session.commit()
        return note

    @jwt_required
    @blp.arguments(NoteUpdateRequest, location="json")
    @blp.response(200, NoteSchema)
    @blp.alt_response(404, ErrorSchema)
    def patch(self, payload, note_id: int):
        """Partially update a note."""
        user_id = request.user_id
        note = Note.query.filter_by(id=note_id, owner_id=user_id).first()
        if not note:
            abort(404, message="Note not found")
        note.update(title=payload.get("title"), content=payload.get("content"))
        db.session.commit()
        return note

    @jwt_required
    @blp.response(204)
    @blp.alt_response(404, ErrorSchema)
    def delete(self, note_id: int):
        """Delete a note."""
        user_id = request.user_id
        note = Note.query.filter_by(id=note_id, owner_id=user_id).first()
        if not note:
            abort(404, message="Note not found")
        db.session.delete(note)
        db.session.commit()
        return ""
