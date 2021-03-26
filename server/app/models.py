from datetime import datetime, timedelta, timezone

from sqlalchemy import event

from app import db
from app.utils import generate_api_key


class User(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True)
    api_key = db.Column(db.String(255), index=True, unique=True)

    def __repr__(self):
        return f"<User: {self.username}>"

    @property
    def current_activity_message(self):
        """An activity message for the user in English (Online/Idle/Offline)"""

        last_coding_session = (
            CodingSession.query.filter_by(user=self)
            .order_by(CodingSession.last_heartbeat_at.desc())
            .first()
        )
        if last_coding_session is None:
            return (
                "It seems you haven't connected DevTime to your editors yet!"
            )
        elif (
            since_last_hb := datetime.now(timezone.utc)
            - last_coding_session.last_heartbeat_at
        ) < timedelta(seconds=60):
            session_length = last_coding_session.length
            return f"You're writing code right now! Time spent coding: {str(session_length)}, Language: {last_coding_session.language}"
        elif since_last_hb < timedelta(minutes=5):
            session_length = last_coding_session.length
            return f"You're idle right now. Just before that, you wrote {last_coding_session.language} code for: {session_length}"
        else:
            return f"You're currently not writing any code. It's been {since_last_hb} since you last coded."

    @property
    def last_session(self):
        """Return last recorded session"""


class CodingSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(64), index=True)
    started_at = db.Column(db.DateTime(timezone=True))
    last_heartbeat_at = db.Column(db.DateTime(timezone=True))

    user_id = db.Column(
        db.String(64), db.ForeignKey("user.id"), nullable=False
    )
    user = db.relationship(
        "User", backref=db.backref("coding_sessions", lazy=True)
    )

    def __repr__(self):
        return f"<CodingSession {self.id}: {self.language}>"

    @property
    def length(self):
        return self.last_heartbeat_at - self.started_at


# Events


@event.listens_for(User, "before_insert")
def receive_before_insert(_mapper, _connection, target):
    """When a new record is created, assign an api key to it"""
    if not target.api_key:
        target.api_key = generate_api_key()
