import os
from datetime import timedelta


# two levels outside this file (server/ directory)
base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(16))

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(base_dir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    AUTH0_CLIENT_ID = "a5IXxvCxOHrLFuT9YfunS320hTZqWY7p"
    AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")
    AUTH0_API_BASE_URL = "https://nikochiko.us.auth0.com"
    AUTH0_ACCESS_TOKEN_URL = f"{AUTH0_API_BASE_URL}/oauth/token"
    AUTH0_AUTHORIZE_URL = f"{AUTH0_API_BASE_URL}/authorize"
    AUTH0_CLIENT_KWARGS = {"scope": "openid profile email"}
    AUTH0_JWKS_URI = f"{AUTH0_API_BASE_URL}/.well-known/jwks.json"

    DEVTIME_ACCEPTABLE_BREAK_DURATION = timedelta(minutes=5)
