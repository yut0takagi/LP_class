from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, timedelta
from dx_app import db
from dx_app.models.shift import ShiftPossib,ShiftSubmission, ShiftComp
from utils import make_dict

bp = Blueprint("classroom", __name__)

@bp.route("/classroom_schedule")
def classroom_schedule():
    start_date_str = request.args.get("start_date", datetime.today().strftime("%Y-%m-%d"))
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")

    date_list = [start_date + timedelta(days=i) for i in range(7)]
    weekday_list = [date.strftime("%a") for date in date_list]
    period_list = ["1限", "2限", "3限", "4限", "5限"]

    return render_template("classroom/manage-classroom.html", data={
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

@bp.route("/manage-classroom", methods=["GET", "POST"])
def manage_classroom():
    # 現在のシフト期間を取得
    shift_period = ShiftPeriod.query.order_by(ShiftPeriod.id.desc()).first()

    if request.method == "POST":
        # フォームからデータを取得
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        submission_start = request.form["submission_start"]
        submission_end = request.form["submission_end"]

        # 既存のシフト期間を削除し、新しいデータを登録
        ShiftPeriod.query.delete()
        new_period = ShiftPeriod(
            start_date=start_date, end_date=end_date,
            submission_start=submission_start, submission_end=submission_end
        )
        db.session.add(new_period)
        db.session.commit()

        flash("教室開講時間とシフト期間を更新しました！", "success")
        return redirect(url_for("misc.manage_classroom"))

    return render_template("classroom/manage-classroom.html", period=shift_period, data=make_dict("classroom"))