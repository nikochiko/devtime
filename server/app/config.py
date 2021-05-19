import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

# two levels outside this file (server/ directory)
base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

DB_URL = os.getenv(
    "DATABASE_URL", f"postgresql://localhost:5432/devtime_dev"
)

# heroku still uses postgres:// idfk why
DB_URL = DB_URL.replace("postgres://", "postgresql://")


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(16))

    JWT_ALGORITHM = "HS256"

    TEMPLATES_AUTO_RELOAD = True

    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEVTIME_ACCEPTABLE_BREAK_DURATION = timedelta(minutes=5)

    INTERNAL_AUTH_TOKEN = os.environ.get("INTERNAL_AUTH_TOKEN", "token123")
