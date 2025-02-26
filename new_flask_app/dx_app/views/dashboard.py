from flask import render_template, Blueprint, session, redirect, url_for
from flask_login import login_required, current_user
from utils import make_dict
from dx_app.models import Student
bp = Blueprint("dashboard", __name__)


# ログイン後のページであるため、layoutは"new_flask_app/dx_app/templates/layoutForLogined.html"とする。
@bp.route("/student")
@login_required
def student():
    student = Student.query.filter_by(id=current_user.id).first()
    if not student:
        return redirect(url_for("auth.login"))
    user_type = "individual" if student.depertment_id == "0" else "cram"
    if user_type == "cram":
        return render_template("dashboard/student/cram/dashboard.html", data=make_dict("dashboard"))
    elif user_type == "individual":
        return render_template("dashboard/student/individual/dashboard.html", data=make_dict("dashboard"))
    return redirect(url_for("auth.login"))


@bp.route("/educator")
@login_required
def educator():
    return render_template("dashboard/educator/dashboard.html",data=make_dict("dashboard"))


