from flask import Flask, render_template, request, jsonify,redirect,url_for
import openai
import json
from dotenv import dotenv_values
import os
import datetime
app = Flask(__name__)
from dx_app import app

staff_list = [
    {"id": 1, "name": "田中"},
    {"id": 2, "name": "佐藤"},
    {"id": 3, "name": "鈴木"}
]
# 日付のリスト（例: 今日から1週間分）
date_list = [datetime.date.today() + datetime.timedelta(days=i) for i in range(50)]
# 曜日のリスト（日本語で表示）
weekday_list = [date.strftime("%a") for date in date_list]  # "Mon", "Tue", "Wed" など
# 日付を文字列に変換
date_str_list = [date.strftime("%Y-%m-%d") for date in date_list]  # YYYY-MM-DD 形式
# 時限のリスト（例: 1限〜5限）
period_list = ["1限", "2限", "3限", "4限", "5限"]


def make_dict(pagename):
    '''
    引数で与えられたページ名に応じた辞書を返す
    dict={title:"ページタイトル"}
    '''
    global staff_list,date_list, period_list,weekday_list
    # 初期設定
    dict={}
    titles={
        "login":"ログイン",
        "make-account":"アカウントの新規作成",
        "dashboard":"ダッシュボード",
        "edit-profile":"プロフィール編集",
        "chatbot":"教室運営用AIエージェント",
        "homepage":"ホーム",
        "shift-sub":"シフトの提出"
    }
    # 各ページに応じた引渡しデータの編集
    try:
        dict["title"] = titles[pagename]
    except:
        dict["title"] = "ページが見つかりません"
        
    try:
        dict["data"]=[staff_list,date_list, period_list,weekday_list]
    except:
        dict["data"] = "データが取得できませんでした"
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


@app.route('/chatbot')
def chat_bot():
    return render_template("dx_app/chatbot.html",data=make_dict("chatbot"))

@app.route("/chat", methods=["POST"])
def chat():
    env_path = "/Users/y.takagi/GitHub/LP_class/new_flask_app/dx_app/.env"  # 例: "/home/user/project/.env"
    config = dotenv_values(env_path)
    # OPENAI_API_KEY を取得
    openai.api_key = config.get("OPENAI_API_KEY")
    data = request.get_json()
    user_message = data.get("message", "")

    try:
        # OpenAI API で応答を取得
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # または `gpt-4`
            messages=[{"role": "user", "content": user_message}]
        )

        ai_response = response["choices"][0]["message"]["content"]
    except Exception as e:
        ai_response = "エラーが発生しました。管理者へお伝えください。"

    return jsonify({"response": ai_response})


@app.route('/shift-sub')
def shift():
    return render_template("dx_app/shift-sub.html",data=make_dict("shift-sub"))



@app.route("/submit_shift", methods=["POST"])
def submit_shift():
    submitted_shifts = {}
    for period in period_list:
        for date in date_list:
            key = f"shift_{period}_{date}"
            value = request.form.get(key, "未選択")
            submitted_shifts[key] = value

    # ここでデータベースに保存する処理を追加可能（例: SQLite, MySQL）
    print("提出されたシフト:", submitted_shifts)

    return redirect(url_for("shift"))