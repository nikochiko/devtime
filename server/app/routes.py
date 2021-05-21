from datetime import date, datetime, timedelta, timezone
from dateutil.parser import isoparse

import pytz
from flask import (
    request,
    redirect,
    render_template,
    jsonify,
    g,
)

from app import app, db
from app.models import User, CodingSession
from app.decorators import requires_auth, requires_internal_auth, requires_api_key, requires_jwt_token
from app.utils import get_jwt_for_user


@app.route("/")
def index():
    return redirect("/dashboard")

@app.route("/dashboard")
@requires_auth
def dashboard():
    g.jwt_token = get_jwt_for_user(g.user)
    return render_template("dashboard.html")


@app.route("/activity")
@requires_auth
def activity():
    g.jwt_token = get_jwt_for_user(g.user)
    return render_template("activity.html")


@app.route("/profile")
@requires_auth
def profile():
    g.jwt_token = get_jwt_for_user(g.user)
    return render_template("profile.html")


@app.route("/widgets")
@requires_auth
def widgets():
    return render_template("widgets.html")


@app.route("/internal/users", methods=["POST"])
@requires_internal_auth
def users():
    data = request.get_json()
    hyperlog_uid = data["hyperlog_uid"]

    user = User(id=hyperlog_uid)
    db.session.add(user)
    db.session.commit()

    return jsonify({"success": True, "api_key": user.api_key})


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
    user = g.api_user

    data = request.get_json()
    recorded_at, language = data["recorded_at"], data["language"]
    editor = data["client"]

    recorded_at = isoparse(recorded_at)
    tz_naive_recorded_at = recorded_at.replace(tzinfo=None)

    if recorded_at.tzinfo is None:
        recorded_at = recorded_at.replace(tzinfo=timezone.utc)

    # the date for that datetime
    tz_aware_date = recorded_at.astimezone(pytz.timezone(user.timezone)).date()

    # try to get last session with the same programming language
    last_session = (
        CodingSession.query.filter_by(user=user, language=language)
        .order_by(CodingSession.id.desc())
        .first()
    )

    # add a new session object if it is first for the language or stale
    if (
        last_session is None
        or tz_naive_recorded_at - last_session.last_heartbeat_at
        > app.config["DEVTIME_ACCEPTABLE_BREAK_DURATION"]
    ):
        coding_session = CodingSession(
            user=user,
            language=language,
            started_at=tz_naive_recorded_at,
            last_heartbeat_at=tz_naive_recorded_at,
            editor=editor,
        )
        user.statistics[tz_aware_date.strftime("%d-%m-%Y")] = user.get_stats_by_date(tz_aware_date)
        db.session.add(coding_session)
        db.session.add(user)
    else:
        user.statistics[tz_aware_date.strftime("%d-%m-%Y")] = user.get_stats_by_date(tz_aware_date)

        # overwrite last_heartbeat to most recent heartbeat
        last_session.last_heartbeat_at = tz_naive_recorded_at
        db.session.add(last_session)
        db.session.add(user)

    db.session.commit()

    # return OK response
    return jsonify({"status": "OK"})


@app.route("/api/activity", methods=["GET"])
@requires_jwt_token
def activity_api():
    start_iso, end_iso = request.args.get("start"), request.args.get("end")

    start = (
        isoparse(start_iso).astimezone(timezone.utc).replace(tzinfo=None)
        if start_iso
        else datetime.now(timezone.utc) - timedelta(days=1)
    )
    end = isoparse(end_iso).astimezone(timezone.utc).replace(tzinfo=None) if end_iso else start + timedelta(days=1)

    return jsonify(g.user.get_stats_between(start, end))


@app.route("/api/daywise_stats", methods=["GET"])
@requires_jwt_token
def daywise_stats():
    start_date, end_date = request.args.get("start"), request.args.get("end")

    # default weekly stats
    start = (
        isoparse(start_date).astimezone(timezone.utc).replace(tzinfo=None)
        if start_date
        else date.today() - timedelta(days=7)
    )
    end = isoparse(end_date).astimezone(timezone.utc).replace(tzinfo=None) if end_date else date.today()

    remove_time_attrs = lambda d: date(d.year, d.month, d.day)

    start_date, end_date = (
        remove_time_attrs(start),
        remove_time_attrs(end)
    )

    return jsonify(g.user.daywise_stats(start_date, end_date))
