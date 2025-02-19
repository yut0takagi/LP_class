from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from dx_app.models import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        """ パスワードをハッシュ化して保存 """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """ パスワードが正しいか検証 """
        return check_password_hash(self.password_hash, password)