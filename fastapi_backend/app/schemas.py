from marshmallow import Schema, fields, validate


class MessageSchema(Schema):
    message = fields.String(required=True, description="Information message")


class ErrorSchema(Schema):
    code = fields.Integer()
    status = fields.String()
    message = fields.String()
    errors = fields.Dict(keys=fields.String(), values=fields.Raw())


class PaginationMetadata(Schema):
    total = fields.Integer()
    total_pages = fields.Integer()
    first_page = fields.Integer()
    last_page = fields.Integer()
    page = fields.Integer()
    previous_page = fields.Integer(allow_none=True)
    next_page = fields.Integer(allow_none=True)


class RegisterRequest(Schema):
    email = fields.Email(required=True, description="User email")
    password = fields.String(required=True, validate=validate.Length(min=6), description="User password (min 6 characters)")


class LoginRequest(Schema):
    email = fields.Email(required=True, description="User email")
    password = fields.String(required=True, description="User password")


class TokenResponse(Schema):
    access_token = fields.String(required=True, description="JWT access token")
    token_type = fields.String(required=True, description="Token type (Bearer)")


class UserSchema(Schema):
    id = fields.Integer()
    email = fields.Email()
    created_at = fields.DateTime()


class NoteCreateRequest(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1, max=255), description="Note title")
    content = fields.String(allow_none=True, description="Note content (Markdown supported)")


class NoteUpdateRequest(Schema):
    title = fields.String(validate=validate.Length(min=1, max=255))
    content = fields.String(allow_none=True)


class NoteSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    content = fields.String(allow_none=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
