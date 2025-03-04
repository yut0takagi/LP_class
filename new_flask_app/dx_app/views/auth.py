from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from utils import make_dict
from dx_app.forms import LoginForm, RegisterForm, RegistrationFormForStudent1, CramForm, IndividualForm, RegistrationFormForEducator
from dx_app.models import User, Student, Educator, Guardian
from dx_app import db
import uuid

# BluePrint is used to group related views
# auth :全体の認証処理
# auth/settings :個人設定等
# auth/settings/student -> 学生の個人設定(cram, individual)
# auth/settings/teacher -> 教務スタッフ,管理者向けの個人設定
# auth/settings/guardian -> 保護者向けの個人設定
#

# ✅ `auth` Blueprint の定義（メインの認証関連）
bp = Blueprint("auth", __name__, url_prefix="/auth")
bp_auth_settings = Blueprint("settings", __name__, url_prefix="/auth/settings")
bp_auth_settings_students = Blueprint("settings_students", __name__, url_prefix="/auth/settings/students")
bp_auth_settings_teachers = Blueprint("settings_teachers", __name__, url_prefix="/auth/settings/teachers")
bp_auth_settings_guardians = Blueprint("settings_guardians", __name__, url_prefix="/auth/settings/guardians")






# /auth/register
@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "GET":
        form.id.data = str(uuid.uuid4())  # UUID を生成してセット
<<<<<<< HEAD

=======
>>>>>>> origin/main
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

# /auth/login
@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # フォームのバリデーション
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            session["user_id"] = user.id
            flash("ログイン成功！", "success")
            # ユーザーの役割に応じて対応するテーブルをチェック
            if user.role == "student":
                student = Student.query.filter_by(id=user.id).first()
                if not student:
                    return redirect(url_for('settings.first_settings_for_student'))
                else:
                    return redirect(url_for("dashboard.student"))
            elif user.role == "educator": 
                educator = Educator.query.filter_by(id=user.id).first()
                if not educator:
                    return redirect(url_for("settings.first_settings_for_educator"))
                else:
                    return redirect(url_for("dashboard.educator"))
            elif user.role == "guardian":
                guardian = Guardian.query.filter_by(id=user.id).first()
                if not guardian:
                    return redirect(url_for("auth.settings.guardians"))
                else:
                    return redirect(url_for("保護者向けダッシュボード"))
            flash("ページ移動に失敗しました。")
            return redirect(url_for("auth.login"))
        else:
            flash("ログイン失敗。メールアドレスまたはパスワードが間違っています。", "danger")

    return render_template("auth/login.html", form=form, data=make_dict("login"))

# /auth/settings/students
@login_required
@bp_auth_settings.route("/student", methods=["POST","GET"])
def first_settings_for_student():
    form = RegistrationFormForStudent1()
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login')) 
    user_id = current_user.id
    if form.validate_on_submit():
        session["user_type"] = form.user_type.data
        return redirect(url_for("settings_students.student_details"))
    return render_template("auth/details/student/fot_student.html", data=make_dict("account_settings_for_student", form=form))

# auth/settings/teachers
@login_required
@bp_auth_settings.route("/educator", methods=["POST","GET"])
def first_settings_for_educator():
    form= RegistrationFormForEducator()
    if request.method == "GET":
        return render_template("auth/details/educator/educator.html", data=make_dict("educator_details", form=form))
    elif request.method == "POST":
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        user_id = current_user.id
        if form.validate_on_submit():
            new_educator=Educator(
                id=user_id,
                organization_id = form.organization_id.data,
                depertment_id = form.depertment_id.data,
                hire_date = form.hire_date.data,
                permissions=form.permissions.data
            )
            db.session.add(new_educator)
            db.session.commit()
            return redirect(url_for("dashboard.educator"))
        else:
            flash("登録に失敗しました。", "danger")
            return redirect(url_for("auth.login"))
    return render_template("auth/details/educator/educator.html", data=make_dict("educator_details", form=form))

# auth/settings/guardians
@login_required
@bp_auth_settings.route("/guardians", methods=["GET", "POST"])
def first_settings_for_student_details():
    print("保護者向けの新規登録")

@login_required
@bp_auth_settings_students.route("/details", methods=["GET", "POST"])
def student_details():
    form = None
    user_id = current_user.id
    user_type = session.get("user_type", "")

    if user_type == "cram":
        form = CramForm()
    elif user_type == "individual":
        form = IndividualForm()
    else:
        form = None

    if request.method == "GET":
        if user_type == "cram":
            return render_template("auth/details/student/cram.html", data=make_dict("student_cram", form=form))
        elif user_type == "individual":
            return render_template("auth/details/student/individual.html", data=make_dict("student_individual", form=form))

    if request.method == "POST":
        print("🔹 フォーム送信処理開始")
        print("current_user:", current_user)
        print("current_user.is_authenticated:", current_user.is_authenticated)
        print("current_user.id:", current_user.id if current_user.is_authenticated else "Not logged in")
        print("session['user_type']:", session.get("user_type"))
        print("🔍 request.method:", request.method)
        print("🔍 `request.form` の内容:", request.form)
        print("📌 `form` の内容（パース後）:", form.data)
        print("🚨 CSRF Token:", form.csrf_token.data)
        print("🚨 フォームバリデーションエラー:", form.errors)
    if form and form.validate_on_submit():
        print("✅ フォームが正常に送信されました")
        if user_type == "cram":
            new_student = Student(
                id=user_id,
                elementary_school=form.elementary_school.data,
                middle_school=form.middle_school.data,
                high_school=form.high_school.data,
                age=form.age.data,
                grade=form.grade.data,
                emergency_contact1_name=form.emergency_contact1_name.data,
                emergency_contact1_number=form.emergency_contact1_number.data,
                emergency_contact2_name=form.emergency_contact2_name.data,
                emergency_contact2_number=form.emergency_contact2_number.data,
                emergency_contact3_name=form.emergency_contact3_name.data,
                emergency_contact3_number=form.emergency_contact3_number.data,
                guardian_id=form.guardian_id.data,
                address=form.address.data,
                postal_code=form.postal_code.data,
                gender=form.gender.data,
                organization_id=form.organization_id.data,
                depertment_id=form.depertment_id.data,
                enrollment_years=form.enrollment_years.data,
                graduation_status=form.graduation_status.data
            )
            db.session.add(new_student)
            db.session.commit()
            print("Redirecting to:", url_for("dashboard.student"))
            return redirect(url_for("dashboard.student"))

        elif user_type == "individual":
            new_student = Student(
                id=user_id,
                elementary_school=form.elementary_school.data,
                middle_school=form.middle_school.data,
                high_school=form.high_school.data,
                age=form.age.data,
                grade=form.grade.data,
                emergency_contact1_name="",
                emergency_contact1_number="",
                emergency_contact2_name="",
                emergency_contact2_number="",
                emergency_contact3_name="",
                emergency_contact3_number="",
                guardian_id="",
                address=form.address.data,
                postal_code=form.postal_code.data,
                gender=form.gender.data,
                organization_id=0,
                depertment_id=0,
                enrollment_years=0,
                graduation_status="",
            )
            db.session.add(new_student)
            db.session.commit()
            return redirect(url_for("dashboard.student"))
    else:
        flash("サーバーで何らかのエラーが発生しました。")
        return redirect(url_for("auth.login"))

# 教務スタッフにおけるログイン時個人情報入力処理


# ログアウト時のエンドポイント
@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("ログアウトしました。", "info")
    return redirect(url_for("auth.login"))
