from dx_app import db
from datetime import datetime

class ShiftPossib(db.Model):
    __tablename__ = "shift_possib"  # テーブル名を変更

    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)  # 教師ID（UserテーブルのIDを参照）
    date = db.Column(db.Date, nullable=False)  # 日付
    period = db.Column(db.String(10), nullable=False)  # 時限（1限, 2限, ...）
    status = db.Column(db.String(1), nullable=False)  # ○ or ✖
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 登録日時

    teacher = db.relationship("User", backref="shift_possibilities")  # 教師情報の取得用