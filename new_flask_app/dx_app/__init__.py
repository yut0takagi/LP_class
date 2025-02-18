from flask import Flask
import dx_app.views
from pathlib import Path
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('dx_app.config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

import dx_app.views

