from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from server.config import Config

app = Flask("Dev-Tick,Tick,Tick")
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
oauth = OAuth(app)

from server import routes, models  # noqa: F401
