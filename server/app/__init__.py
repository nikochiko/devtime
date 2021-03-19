from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from authlib.integrations.flask_client import OAuth

from app.config import Config

app = Flask("Dev-Tick,Tick,Tick")
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
oauth = OAuth(app)
auth0 = oauth.register("auth0", jwks_uri=Config.AUTH0_JWKS_URI)

from app import routes, models  # noqa: F401, E402
