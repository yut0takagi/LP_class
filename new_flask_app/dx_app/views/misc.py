from flask import render_template, Blueprint
from utils import make_dict

bp = Blueprint("misc", __name__)

@bp.route('/homepage')
def homepage():
    return render_template("misc/homepage.html",data=make_dict("homepage"))

@bp.route("/edit-profile")
def edit_profile():
    return render_template("misc/edit-profile.html",data=make_dict("edit-profile"))

# 設定画面
@bp.route('/settings')
def settings():
    return render_template("misc/settings.html",data=make_dict("settings"))


# エラーについての処理
def page_not_found(e):
    return render_template("errors/404.html"), 404

@bp.errorhandler(400)
def bad_request_handler(error):
    return render_template("errors/404.html"), 400