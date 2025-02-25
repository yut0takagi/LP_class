from flask import render_template, Blueprint
from flask_login import login_required
from utils import make_dict

bp = Blueprint("dashboard", __name__)


# ログイン後のページであるため、layoutは"new_flask_app/dx_app/templates/layoutForLogined.html"とする。
@bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard/dashboardForEducator.html",data=make_dict("dashboard"))
