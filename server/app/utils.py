import base64
import uuid
from datetime import datetime
from typing import Optional

import jwt
from flask import current_app


def generate_api_key():
    """Generates new API key by encoding a UUID to base64"""
    uuid_bytes = str(uuid.uuid4()).encode()
    return base64.b64encode(uuid_bytes).decode()


def get_jwt_for_user(user: "User") -> str:
    """Generates JWT (with payload) for user"""
    return jwt_encode(jwt_payload_for_user(user))


def jwt_encode(
    payload: dict[str, any],
    secret: Optional[str] = None,
    algo: Optional[str] = None,
) -> str:
    """Encode payload into a JWT"""
    return jwt.encode(
        payload,
        secret or current_app.config["SECRET_KEY"],
        algorithm=algo or current_app.config["JWT_ALGORITHM"],
    )


def jwt_payload_for_user(user: "User") -> dict[str, any]:
    """Get payload for creating user's JWT"""
    return {"id": user.id}
