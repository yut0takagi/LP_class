from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from utils import make_dict
from dx_app.forms import LoginForm, RegisterForm
from dx_app.models.user import User
from dx_app import db
import uuid

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    
    if request.method == "GET":
        form.id.data = str(uuid.uuid4())  # UUID を生成してセット


    if form.validate_on_submit():  # フォームのバリデーションが成功した場合
        id = form.id.data
        name = form.name.data
        email = form.email.data
        password = form.password.data
        role = form.user_type.data

        # 既に登録されているメールアドレスかチェック
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("このメールアドレスは既に登録されています。", "danger")
            return redirect(url_for("auth.register"))

        # 新規ユーザー作成
        new_user = User(
            name=name,
            email=email,
            role=role
        )
        new_user.set_password(password)  # ハッシュ化
        db.session.add(new_user)
        db.session.commit()

        flash("登録が完了しました！ログインしてください。", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)

@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # フォームのバリデーション
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("ログイン成功！", "success")
            return redirect(url_for("dashboard.dashboard"))
        else:
            flash("ログイン失敗。メールアドレスまたはパスワードが間違っています。", "danger")

    return render_template("auth/login.html", form=form, data=make_dict("login"))

@bp.route("/make-account", methods=["POST","GET"])
def make_account():
    return render_template("auth/make_account.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("ログアウトしました。", "info")
    return redirect(url_for("auth.login"))
