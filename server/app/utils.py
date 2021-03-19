import base64
import uuid
from functools import wraps

from flask import session, redirect


def requires_auth(f):
    """
    Auth decorator for view functions
    Redirects to login page when user isn't authenticated 
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "profile" not in session:
            return redirect("/login")
        return f(*args, **kwargs)

    return wrapper


def generate_api_key():
    """Generates new API key by encoding a UUID to base64"""
    uuid_bytes = str(uuid.uuid4()).encode()
    return base64.b64encode(uuid_bytes).decode()
