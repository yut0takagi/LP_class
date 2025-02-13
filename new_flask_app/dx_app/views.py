from flask import Flask, render_template


app = Flask(__name__)
from dx_app import app

def make_dict(pagenames):
    """
    ページ名を指定することで、適切な辞書を返す関数
    title: ページのタイトル
            titleの値は初期では、Noneであるため、変更必須
    login: ログインした後(True)か前(False)かを示す。
            loginの値は初期では、Falseであり、ダッシュボードやAIエージェントでは、背景色を#C4D9FFにするため、任意。
            影響対象)
                bodyの背景色(/Users/y.takagi/GitHub/LP_class/new_flask_app/dx_app/static/css/style.css)
                サイドナビゲーションバーの有無(ログイン後のみ、表示する。)

    """
    # 初期設定
    dict={"title":None,#ページのタイトル(必須)
          "login":False #ログインした後(True)か前(False)か
          }
    # 各ページに応じた引渡しデータの編集
    if pagenames =="login":
        dict["title"] = "ログイン"
        dict["login"] = False
    if pagenames =="make-account":
        dict["title"] = "アカウントの新規作成"
        dict["login"] = False
    elif pagenames =="dashboard":
        dict["title"] = "ダッシュボード"
        dict["login"] = True
    return dict

@app.route('/')
def homepage():
    return render_template("dx_app/homepage.html",data=make_dict("homepage"))

@app.route("/login")
def login():
    return render_template("dx_app/login.html",data=make_dict("login"))

@app.route("/make-account", methods=["POST","GET"])
def make_account():
    return render_template("dx_app/make_account.html",data=make_dict("make-account"))

@app.route("/dashboard")
def dashboard():
    return render_template("dx_app/dashboard.html",data=make_dict("dashboard"))

@app.route("/edit-profile")
def edit_profile():
    return render_template("dx_app/edit-profile.html",data=make_dict("edit-profile"))


