from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy import event
from sqlalchemy.dialects.postgresql import JSONB, UUID
from flask import current_app

from app import db
from app.utils import generate_api_key


class User(db.Model):
    __tablename__ = "devtime_users"
    id = db.Column(UUID(), primary_key=True)
    api_key = db.Column(db.String(255), index=True, unique=True)
    statistics = db.Column(JSONB())

    @property
    def current_activity_message(self):
        """An activity message for the user in English (Online/Idle/Offline)"""

        last_coding_session = self.last_session
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
        return (
            CodingSession.query.filter_by(user=self)
            .order_by(CodingSession.last_heartbeat_at.desc())
            .first()
        )

    def get_stats_between(
        self, dt1: datetime, dt2: datetime
    ) -> dict[str, any]:
        """Compiles stats for user between after dt1 and before dt2"""

        sessions = CodingSession.query.filter(
            CodingSession.user == self,
            CodingSession.last_heartbeat_at > dt1,
            CodingSession.started_at < dt2,
        ).order_by(CodingSession.started_at.asc())

        stats = {
            "languages": defaultdict(int),
            "total": 0,  # minutes
            "editors": defaultdict(int),
            "idle_for": 0,  # minutes
        }

        allowed_break = current_app.config["DEVTIME_ACCEPTABLE_BREAK_DURATION"]
        last_on_left = dt1
        for session in sessions:
            left_end = max(session.started_at, dt1)
            right_end = min(session.last_heartbeat_at, dt2)

            # add to idle time if idle for more than allowed break
            idle_time = left_end - last_on_left
            if idle_time > allowed_break:
                stats["idle_for"] += round(idle_time.seconds / 60)

            # convert duration to minutes
            duration = round(
                (right_end - left_end + timedelta(seconds=30)).seconds / 60
            )

            stats["languages"][session.language] += duration
            stats["editors"][session.editor] += duration

            # in total, don't consider overlapping sessions
            stats["total"] += (
                max(right_end, last_on_left)
                - max(left_end, last_on_left)
                + timedelta(seconds=30)
            ).seconds / 60
            stats["total"] = round(stats["total"])
            last_on_left = max(right_end, last_on_left)

        return stats

    def daywise_stats(
        self, start: datetime, end: Optional[datetime] = None
    ) -> dict[str, any]:
        """Get stats on a daywise-frequency"""
        if end is None:
            end = start + timedelta(days=1)

        # check end is a day after start
        assert (
            start <= end
        ), "End date must be greater than or equal to start date"

        # stats will map dates in isoformat to the stats from get_stats_between for that day
        stats = {}

        # collect statistics for each day in a while loop
        current_date = start
        while current_date <= end:
            day_after_current = current_date + timedelta(days=1)
            stats[current_date.strftime("%d-%m-%y")] = self.get_stats_between(
                current_date, day_after_current
            )

            current_date = day_after_current

        return stats


class CodingSession(db.Model):
    __tablename__ = "devtime_coding_sessions"

    id = db.Column(db.BigInteger(), primary_key=True)
    language = db.Column(db.String(64), index=True)
    started_at = db.Column(db.DateTime())
    last_heartbeat_at = db.Column(db.DateTime())
    editor = db.Column(db.String(20))

    devtime_user_id = db.Column(
        UUID(), db.ForeignKey("devtime_users.id"), nullable=False
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
