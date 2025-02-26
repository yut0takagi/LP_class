from dx_app.models import db
from datetime import datetime

class SubjectPossib(db.Model):
    __tablename__ = "SubjectPossib"
    subject_possib_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('User.id'), nullable=False)
    subject = db.Column(db.String(50),db.ForeignKey('Subject.subject_id'), nullable=False)
    available = db.Column(db.Boolean, nullable=False)  # 可能か不可か（True = 可能, False = 不可）

# 来塾可能日（ShiftPossib）
class ShiftPossib(db.Model):
    __tablename__ = "ShiftPossib"
    shift_possib_id = db.Column(db.Integer,nullable=False, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('User.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    period = db.Column(db.Integer,db.ForeignKey('Period.period_id'),nullable=False)
    available = db.Column(db.Boolean, nullable=False)  # 可能か不可か（True = 可能, False = 不可）

# シフト提出期間の設定
class ShiftSubmission(db.Model):
    __tablename__ = "ShiftSubmission"
    shift_submission_id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('Organization.organization_id'), nullable=False)
    depertment_id = db.Column(db.String(50),db.ForeignKey('Depertment.department_id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)  # シフト開始日
    end_date = db.Column(db.Date, nullable=False)    # シフト終了日
    submission_start = db.Column(db.Date, nullable=False)  # 提出開始日
    submission_end = db.Column(db.Date, nullable=False)    # 提出締切日
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())# いつ登録されたか
    created_by = db.Column(db.Integer,db.ForeignKey('User.id'), nullable=False) #誰が登録したか

    def __repr__(self):
        return f"<ShiftPeriod {self.start_date} - {self.end_date}, 提出: {self.submission_start} - {self.submission_end}>"
    
# シフト完成版（ShiftComp）
class ShiftComp(db.Model):
    __tablename__ = "ShiftComp"
    shift_comp_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    period_id = db.Column(db.String(50),db.ForeignKey('Period.period_id'), nullable=False)
    booth = db.Column(db.String(20), nullable=False)  # 教室番号
    student_id = db.Column(db.Integer,db.ForeignKey('User.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
