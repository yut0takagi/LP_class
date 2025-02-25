from dx_app.models import db
from datetime import datetime

class SubjectPossib(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    available = db.Column(db.Boolean, nullable=False)  # 可能か不可か（True = 可能, False = 不可）

# 来塾可能日（ShiftPossib）
class ShiftPossib(db.Model):
    __tablename__ = "shift_possib"  # テーブル名を変更
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    period = db.Column(db.Integer,db.ForeignKey('period.name'),nullable=True)
    available = db.Column(db.Boolean, nullable=False)  # 可能か不可か（True = 可能, False = 不可）

# シフト提出期間
class ShiftPeriod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organization = db.Column(db.String(50), nullable=False)
    depertment = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)  # シフト開始日
    end_date = db.Column(db.Date, nullable=False)    # シフト終了日
    submission_start = db.Column(db.Date, nullable=False)  # 提出開始日
    submission_end = db.Column(db.Date, nullable=False)    # 提出締切日
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())# いつ登録されたか

    def __repr__(self):
        return f"<ShiftPeriod {self.start_date} - {self.end_date}, 提出: {self.submission_start} - {self.submission_end}>"
    
# シフト完成版（ShiftComp）
class ShiftComp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    booth = db.Column(db.String(20), nullable=False)  # 教室番号
    lesson_id = db.Column(db.Integer, nullable=False)  # 授業割り当てナンバー
