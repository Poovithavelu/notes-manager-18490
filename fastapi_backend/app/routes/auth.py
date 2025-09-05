from flask_smorest import Blueprint, abort
from flask.views import MethodView

from ..models import db, User
from ..auth import create_access_token
from ..schemas import RegisterRequest, LoginRequest, TokenResponse, UserSchema, ErrorSchema

blp = Blueprint(
    "Auth",
    "auth",
    url_prefix="/",
    description="Authentication endpoints for registering and logging in users",
)


@blp.route("/register")
class Register(MethodView):
    @blp.arguments(RegisterRequest, location="json")
    @blp.response(201, UserSchema)
    @blp.alt_response(400, ErrorSchema)
    def post(self, payload):
        """Register a new user.
        Registers a user with an email and password. Passwords are stored securely using hashing.
        Returns the created user (without password).
        """
        email = payload["email"].strip().lower()
        password = payload["password"]

        if User.query.filter_by(email=email).first():
            abort(400, message="Email already registered")

        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user


@blp.route("/login")
class Login(MethodView):
    @blp.arguments(LoginRequest, location="json")
    @blp.response(200, TokenResponse)
    @blp.alt_response(401, ErrorSchema)
    def post(self, payload):
        """Login and obtain a JWT access token.
        Provide email and password to receive a Bearer token for authenticated requests.
        """
        email = payload["email"].strip().lower()
        password = payload["password"]

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            abort(401, message="Invalid email or password")

        token = create_access_token(identity=user.id, additional_claims={"email": user.email})
        return {"access_token": token, "token_type": "Bearer"}
