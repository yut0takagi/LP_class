from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
import datetime
from utils import make_dict
from dx_app import db
from dx_app.models import ShiftPossib,ShiftSubmission



#後日DataBaseと紐付ける----------------------------------------------------------------

# 日付のリスト（例: 今日から1週間分）
# シフト提出の該当期間を設定する。
date_list = [datetime.date.today() + datetime.timedelta(days=i) for i in range(50)]
# 曜日のリスト（日本語で表示）
weekday_list = [date.strftime("%a") for date in date_list]  # "Mon", "Tue", "Wed" など
# 日付を文字列に変換
date_str_list = [date.strftime("%Y-%m-%d") for date in date_list]  # YYYY-MM-DD 形式
# 時限のリスト（例: 1限〜5限）
period_list = ["1限", "2限", "3限", "4限", "5限"]


#-----------------------------------------------------------------------------------

bp = Blueprint("shift", __name__)


@bp.route('/shift-sub')
def shift():
    return render_template("shift/shift-sub.html",data=make_dict("shift-sub"))




@bp.route("/check-shift")
def check_shift():
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month

    # 過去3ヶ月～未来3ヶ月を選択可能
    available_months=[]
    for i in range(-3, 4):
        new_month = (current_month + i) % 12
        new_year = current_year + (current_month + i - 1) // 12
        if new_month == 0:
            new_month = 12
            new_year -= 1
        available_months.append({"year": new_year, "month": new_month})

    calendar = generate_calendar(current_year, current_month)

    return render_template("shift/check-shift.html", data={
        "title": "シフト確認",
        "calendar": calendar,
        "available_months": available_months,
        "current_year": current_year,
        "current_month": current_month
    })

def generate_calendar(year, month):
    """ 指定された年月のカレンダーを作成する関数 """
    first_day = datetime.date(year, month, 1)
    last_day = (first_day.replace(day=28) + datetime.timedelta(days=4)).replace(day=1) - datetime.timedelta(days=1)

    calendar_data = []
    week = []
    current_day = first_day
    while current_day <= last_day:
        if current_day.weekday() == 6 and week:
            calendar_data.append(week)
            week = []
        week.append({"date": current_day, "shifts": []})  # シフトデータを後で入れる
        current_day += datetime.timedelta(days=1)
    if week:
        calendar_data.append(week)

    return calendar_data

@bp.route("/get_calendar")
def get_calendar():
    """ 選択された月のカレンダーを取得 """
    month_str = request.args.get("month")
    year, month = map(int, month_str.split("-"))

    calendar = generate_calendar(year, month)

    # 修正: `data` に `title`, `available_months` などを追加
    return render_template("shift/check-shift.html", data={
        "title": "シフト確認",
        "calendar": calendar,
        "available_months": available_months,
        "current_year": year,
        "current_month": month
    })

@bp.route("/submit_shift", methods=["GET","POST"])
@login_required
def submit_shift():
    """ 教師のシフト提出処理 """
    shift_period = ShiftPeriod.query.order_by(ShiftPeriod.id.desc()).first()

    # シフト対象期間が設定されていない場合
    if not shift_period:
        flash("シフト対象期間が設定されていません。", "danger")
        return redirect(url_for("shift.check_shift"))

    submitted_shifts = []

    for key, value in request.form.items():
        # キーの形式: shift_1限_2025-02-20
        try:
            _, period, date_str = key.split("_")
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            continue  # 無効なキーはスキップ

        # 設定されたシフト対象期間内でなければ無視
        if not (shift_period.start_date <= date <= shift_period.end_date):
            flash(f"{date} はシフト対象期間外です。", "warning")
            continue

        # すでに存在するデータを削除し、新規保存
        existing_shift = ShiftPossib.query.filter_by(
            user_type="teacher", user_id=current_user.id, date=date, period=period
        ).first()

        if existing_shift:
            db.session.delete(existing_shift)

        new_shift = ShiftPossib(
            user_type="teacher", user_id=current_user.id,
            date=date, period=period, is_possible=(value == "○")
        )
        db.session.add(new_shift)
        submitted_shifts.append(new_shift)

    db.session.commit()

    flash(f"{len(submitted_shifts)}件のシフトを提出しました！", "success")
    return redirect(url_for("shift.check_shift"))