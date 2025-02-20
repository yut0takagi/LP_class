from dx_app.models import db
from datetime import datetime


class ShiftPossib(db.Model):
    __tablename__ = "shift_possib"  # テーブル名を変更

    id = db.Column(db.Integer, primary_key=True)
    entity_id = db.Column(db.Integer, nullable=False)  # 教師・教室・生徒のID
    entity_type = db.Column(db.String(10), nullable=False)  # "teacher", "classroom", "student"
    date = db.Column(db.String(10), nullable=False)  # YYYY-MM-DD 形式の日付
    period = db.Column(db.String(10), nullable=False)  # 1限, 2限, ...
    is_available = db.Column(db.Boolean, nullable=False)  # ○=True, ✖=False

    def __repr__(self):
        return f"<ShiftPossib {self.entity_type} {self.entity_id} {self.date} {self.period} {'○' if self.is_available else '✖'}>"

class ShiftPeriod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)  # シフト開始日
    end_date = db.Column(db.Date, nullable=False)    # シフト終了日
    submission_start = db.Column(db.Date, nullable=False)  # 提出開始日
    submission_end = db.Column(db.Date, nullable=False)    # 提出締切日
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<ShiftPeriod {self.start_date} - {self.end_date}, 提出: {self.submission_start} - {self.submission_end}>"