import os
from pathlib import Path

DEBUG = True

# シークレットキーの設定
SECRET_KEY = os.urandom(24).hex()

# インスタンスディレクトリのパスを取得
BASE_DIR = Path(__file__).resolve().parent.parent
INSTANCE_DIR = BASE_DIR / "instance"

# データベースのパスを `instance/local.sqlite` に設定
SQLALCHEMY_DATABASE_URI = f"sqlite:///{INSTANCE_DIR / 'local.sqlite'}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False