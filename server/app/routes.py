from flask import url_for, redirect, render_template_string, session
from werkzeug.urls import url_encode

from app import app, auth0, db
from app.models import User
from app.utils import requires_auth


@app.route("/")
def index():
    return redirect("/dashboard")


@app.route("/login")
def login():
    return auth0.authorize_redirect(
        redirect_uri=url_for("login_callback", _external=True)
    )


@app.route("/login/callback")
def login_callback():
    # handle response from token endpoint
    token = auth0.authorize_access_token()
    userinfo = auth0.parse_id_token(token)

    user_id, username = userinfo["sub"], userinfo["nickname"]

    if not User.query.get(user_id):
        user = User(id=user_id, username=username)
        db.session.add(user)
        db.session.commit()

    # store user info in flask session
    session["jwt_payload"] = userinfo
    session["profile"] = {
        "user_id": user_id,
        "username": username,
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
    return redirect(
        f"{auth0.api_base_url}/v2/logout?{url_encode(params)}"
    )


@app.route("/dashboard")
@requires_auth
def dashboard():
    user_id = session["profile"]["user_id"]

    user = User.query.get(user_id)
    return render_template_string(f"<h1>Hello! {user.username}</h1>")
