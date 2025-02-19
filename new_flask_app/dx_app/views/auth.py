from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from utils import make_dict
from dx_app.forms import LoginForm, RegisterForm
from dx_app.models.user import User
from dx_app import db

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("このメールアドレスは既に登録されています。", "danger")
            return redirect(url_for("auth.register"))

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("登録が完了しました！ログインしてください。", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/make_account.html",data=make_dict("make-account"))

@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # フォームのバリデーション
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("ログイン成功！", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("ログイン失敗。メールアドレスまたはパスワードが間違っています。", "danger")

    return render_template("auth/login.html", form=form, data=make_dict("login"))

@bp.route("/make-account", methods=["POST","GET"])
def make_account():
    return render_template("dx_app/make_account.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("ログアウトしました。", "info")
    return redirect(url_for("auth.login"))
