import base64
import uuid


def generate_api_key():
    """Generates new API key by encoding a UUID to base64"""
    uuid_bytes = str(uuid.uuid4()).encode()
    return base64.b64encode(uuid_bytes).decode()
