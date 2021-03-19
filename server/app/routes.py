from flask import url_for, session

from app import app, oauth
from app.models import User
from app.utils import requires_auth


@app.route("/")
def index():
    return redirect("/dashboard")


@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(redirect_uri=url_for("login_callback"))


@app.route("/login/callback")
def login_callback():
    auth0 = oauth.auth0

    # handle response from token endpoint
    token = auth0.authorize_access_token()
    userinfo = oauth.auth0.parse_id_token(token)

    # store user info in flask session
    session["jwt_payload"] = userinfo
    session["profile"] = {
        "user_id": userinfo["sub"],
        "name": userinfo["name"],
        "picture": userinfo["picture"],
    }

    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {
        "returnTo": url_for("dashboard", _external=True),
        "client_id": "a5IXxvCxOHrLFuT9YfunS320hTZqWY7p",
    }
    return redirect(f"{oauth.auth0.api_base_url}/v2/logout?{urlencode(params)}")


@app.route("/dashboard")
@requires_auth
def dashboard():
    user_id = session["profile"]["user_id"]

    user = User.query.get(user_id)
    return render(f"<h1>Hello! {user.username}</h1>")
