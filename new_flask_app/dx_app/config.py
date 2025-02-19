import os
from pathlib import Path

DEBUG = True

SECRET_KEY = os.urandom(24).hex()
SQLALCHEMY_DATABASE_URI = f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}"  # データベースのパス
SQLALCHEMY_TRACK_MODIFICATIONS = False

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, '../instance/schedule_management.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False