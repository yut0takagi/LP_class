from flask import Flask, render_template


app = Flask(__name__)
from dx_app import app

def make_dict(pagenames):
    # 初期設定
    dict={"title":None,
          "nav_pattern":0
          }
    # 各ページに応じた引渡しデータの編集
    if pagenames =="login":
        dict["nav_pattern"] = 1
    return dict

@app.route('/')
def homepage():
    return render_template("dx_app/homepage.html",title="ホームページ")

@app.route("/login")
def login():
    return render_template("dx_app/login.html",title="ログイン")

@app.route("/make-account")
def make_account():
    return render_template("dx_app/make_account.html",title="アカウントの新規作成")
