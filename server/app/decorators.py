import jwt
from functools import wraps
from typing import Optional

from flask import (
    current_app,
    g,
    jsonify,
    make_response,
    redirect,
    request,
    session,
)

from app.config import Config
from app.models import User


def requires_auth(f):
    """
    Auth decorator for view functions
    Redirects to login page when user isn't authenticated
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        if "profile" not in session:
            return redirect("/login")
        g.user = User.query.get(session["profile"]["user_id"])
        return f(*args, **kwargs)

    return wrapper


def requires_internal_auth(f):
    """
    Auth decorator for internal API
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if auth_header is None or not auth_header.lower().startswith(
            "bearer "
        ):
            return make_response(
                jsonify({"message": "Authorization Header is required"}), 401
            )

        token = auth_header.split(maxsplit=1)[-1]
        if token != Config.INTERNAL_AUTH_TOKEN:
            return make_response(jsonify({"message": "Unauthorized"}), 401)

        return f(*args, **kwargs)

    return wrapper


def requires_api_key(f):
    """
    Decorator for view functions. This checks for X-API-KEY header
    and adds the user onto 'g' global object
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get("X-API-KEY")
        if api_key is None:
            return make_response(
                {"message": "X-API-KEY header is required."}, 401
            )

        user = User.query.filter_by(api_key=api_key).first()
        if user is None:
            return make_response({"message": "API key is invalid"}, 401)

        g.api_user = user
        return f(*args, **kwargs)

    return wrapper


def requires_jwt_token(f):
    """
    Decorator for view function. Requires a HTTP Authorization header with token.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if auth_header is None:
            return make_response(
                {"message": "HTTP_AUTHORIZATION header is required"}, 403
            )

        # check if auth header is a 'token' type
        auth_type, token = auth_header.split(" ", maxsplit=1)
        if auth_type != "token":
            return make_response(
                {"message": "Authorization header must start with `Token `"}
            )

        user = jwt_user_from_payload(jwt_decode(token))
        g.user = user
        return f(*args, **kwargs)

    return wrapper


def jwt_decode(
    token: str, secret: Optional[str] = None, algo: Optional[str] = None
) -> dict[str, any]:
    """Decode a JWT to its payload form"""
    return jwt.decode(
        token,
        secret or current_app.config["SECRET_KEY"],
        algorithms=[algo or current_app.config["JWT_ALGORITHM"]],
    )


def jwt_user_from_payload(payload: dict[str, any]) -> User:
    """Gets user from JWT payload"""

    # TODO: add expiry check
    return User.query.get(payload["id"])
