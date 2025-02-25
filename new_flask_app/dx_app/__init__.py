from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import os
from dx_app.models import db, User

migrate = Migrate()
csrf = CSRFProtect()
# DB と LoginManager の初期化（appより前に定義する）
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('dx_app.config')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # 🔹 未認証ユーザーは 'auth.login' へリダイレクト
    login_manager.login_view = "auth.login"
    
    # 404 Not found errorについての遷移
    from dx_app.views.misc import page_not_found
    app.register_error_handler(404, page_not_found)

    # 🔵 Blueprint の登録
    from dx_app.views.auth import bp as auth_bp
    from dx_app.views.dashboard import bp as dashboard_bp
    from dx_app.views.shift import bp as shift_bp
    from dx_app.views.student import bp as student_bp
    from dx_app.views.chatbot import bp as chatbot_bp
    from dx_app.views.misc import bp as misc_bp
    from dx_app.views.classroom import bp as classroom_bp


    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(shift_bp, url_prefix="/shift")
    app.register_blueprint(student_bp, url_prefix="/student")
    app.register_blueprint(chatbot_bp, url_prefix="/chatbot")
    app.register_blueprint(misc_bp, url_prefix="")
    app.register_blueprint(classroom_bp, url_prefix="/classroom")
    return app

@login_manager.user_loader
def load_user(user_id):
    """ログイン中のユーザーを取得"""
    from dx_app.models.user import User  # ここでインポートして循環インポートを回避
    return User.query.get(int(user_id))