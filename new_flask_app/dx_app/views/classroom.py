from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, timedelta
from dx_app import db
from dx_app.models.shift import ShiftPossib  # 新しく作成するモデル

bp = Blueprint("classroom", __name__)

@bp.route("/classroom_schedule")
def classroom_schedule():
    start_date_str = request.args.get("start_date", datetime.today().strftime("%Y-%m-%d"))
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")

    date_list = [start_date + timedelta(days=i) for i in range(7)]
    weekday_list = [date.strftime("%a") for date in date_list]
    period_list = ["1限", "2限", "3限", "4限", "5限"]

    return render_template("classroom/classroom-schedule.html", data={
        "date_list": date_list,
        "weekday_list": weekday_list,
        "period_list": period_list
    })

@bp.route("/submit_schedule", methods=["POST"])
def submit_schedule():
    for period in ["1限", "2限", "3限", "4限", "5限"]:
        for date in request.form:
            if f"shift_{period}_" in date:
                shift_date = date.split("_")[1]
                shift_value = request.form[date]
                new_entry = ShiftPossib(
                    classroom_id=1,  # 教室ID（仮で1固定）
                    date=shift_date,
                    period=period,
                    is_available=(shift_value == "○")
                )
                db.session.add(new_entry)

    db.session.commit()
    flash("スケジュールが保存されました。", "success")
    return redirect(url_for("classroom.classroom_schedule"))