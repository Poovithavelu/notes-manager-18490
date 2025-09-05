import datetime
import functools
from typing import Any, Dict, Optional

import jwt
from flask import current_app, request
from werkzeug.exceptions import Unauthorized


# PUBLIC_INTERFACE
def create_access_token(identity: int, additional_claims: Optional[Dict[str, Any]] = None) -> str:
    """Create a signed JWT access token with the configured expiration."""
    now = datetime.datetime.utcnow()
    exp = now + current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]
    payload = {
        "sub": str(identity),
        "iat": now,
        "nbf": now,
        "exp": exp,
        "type": "access",
    }
    if additional_claims:
        payload.update(additional_claims)
    token = jwt.encode(payload, current_app.config["JWT_SECRET_KEY"], algorithm=current_app.config["JWT_ALGORITHM"])
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token


# PUBLIC_INTERFACE
def decode_token(token: str) -> Dict[str, Any]:
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(
            token,
            current_app.config["JWT_SECRET_KEY"],
            algorithms=[current_app.config["JWT_ALGORITHM"]],
            options={"require": ["exp", "iat", "nbf"]},
        )
        return payload
    except jwt.ExpiredSignatureError as e:
        raise Unauthorized("Token has expired") from e
    except jwt.InvalidTokenError as e:
        raise Unauthorized("Invalid token") from e


# PUBLIC_INTERFACE
def get_bearer_token_from_request() -> str:
    """Extract Bearer token from the Authorization header."""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.lower().startswith("bearer "):
        raise Unauthorized("Missing or invalid Authorization header")
    return auth_header.split(" ", 1)[1].strip()


# PUBLIC_INTERFACE
def jwt_required(fn):
    """Decorator to enforce JWT auth on a route method."""

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        token = get_bearer_token_from_request()
        payload = decode_token(token)
        request.user_id = int(payload["sub"])
        return fn(*args, **kwargs)

    return wrapper
