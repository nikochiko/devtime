import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    AUTH0_CLIENT_ID = "a5IXxvCxOHrLFuT9YfunS320hTZqWY7p"
    AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")
    AUTH0_API_BASE_URL = "https://nikochiko.us.auth0.com"
    AUTH0_ACCESS_TOKEN_URL = f"{AUTH0_API_BASE_URL}/oauth/token"
    AUTH0_AUTHORIZE_URL = f"{AUTH0_API_BASE_URL}/authorize"
    AUTH0_CLIENT_KWARGS = {"scope": "openid profile email"}
