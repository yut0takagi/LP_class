from flask import render_template, Blueprint
from utils import make_dict

bp = Blueprint("misc", __name__)


@bp.route("/edit-profile")
def edit_profile():
    return render_template("dx_app/edit-profile.html",data=make_dict("edit-profile"))

@bp.route('/')
def homepage():
    return render_template("dx_app/homepage.html",data=make_dict("homepage"))

# 設定画面
@bp.route('/settings')
def settings():
    return render_template("dx_app/settings.html",data=make_dict("settings"))
