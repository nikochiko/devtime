from functools import wraps

from flask import g, make_response, redirect, request, session

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
