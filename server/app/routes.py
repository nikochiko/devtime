from datetime import datetime
from dateutil.parser import isoparse

from flask import (
    url_for,
    request,
    redirect,
    render_template,
    jsonify,
    session,
    g,
)
from werkzeug.urls import url_encode

from app import app, auth0, db
from app.models import User, CodingSession
from app.decorators import requires_auth, requires_api_key


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

    if not (user := User.query.get(user_id)):
        user = User(id=user_id, username=username)
        db.session.add(user)
        db.session.commit()

    g.user = user

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
        "returnTo": url_for("index", _external=True),
        "client_id": "a5IXxvCxOHrLFuT9YfunS320hTZqWY7p",
    }
    return redirect(f"{auth0.api_base_url}/v2/logout?{url_encode(params)}")


@app.route("/dashboard")
@requires_auth
def dashboard():
    user_id = session["profile"]["user_id"]

    user = User.query.get(user_id)
    return render_template("dashboard.html")


@app.route("/activity")
@requires_auth
def activity():
    g.user = User.query.get(session["profile"]["user_id"])
    return render_template("activity.html")


@app.route("/api/heartbeats", methods=["POST"])
@requires_api_key
def heartbeats():
    """
    Anatomy of a heartbeat:
      recorded_at: datetime (iso8601)
      language: string

    e.g.
    {
      "recorded_at": "2021-03-19T19:23:09",
      "language": "python"
    }
    """
    data = request.get_json()
    recorded_at, language = data["recorded_at"], data["language"]
    recorded_at = isoparse(recorded_at)

    # try to get last session with the same programming language
    last_session = (
        CodingSession.query.filter_by(user=g.api_user, language=language)
        .order_by(CodingSession.id.desc())
        .first()
    )

    # add a new session object if it is first for the language or stale
    if (
        last_session is None
        or recorded_at - last_session.last_heartbeat_at
        > app.config["DEVTIME_ACCEPTABLE_BREAK_DURATION"]
    ):
        coding_session = CodingSession(
            user=g.api_user,
            language=language,
            started_at=recorded_at,
            last_heartbeat_at=recorded_at,
        )
        db.session.add(coding_session)
    else:
        # overwrite last_heartbeat to most recent heartbeat
        last_session.last_heartbeat_at = recorded_at
        db.session.add(last_session)

    db.session.commit()

    # return OK response
    return jsonify({"status": "OK"})
