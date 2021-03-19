from functools import wraps


def requires_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "profile" not in session:
            return redirect("/login")
        return f(*args, **kwargs)

    return wrapper
