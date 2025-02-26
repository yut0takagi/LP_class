from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from dx_app.models import db


# 全ユーザーが登録するUserテーブル
class User(db.Model, UserMixin):
    """
    Userテーブル
    id(Integer): ユーザーID (Primary Key)->本サービスを利用するすべてのユーザーに配分(同一はないように分配する)
    name(String max_50 null_unable): ユーザー名
    email(String max_100 null_unable): メールアドレス->ログイン時に利用する
    pasword_hash: パスワードのハッシュ化した文字列
    role: 役割（student, teacher, Guardianなど）
    """
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="student")  # 追加: 役割（student, teacher, Guardianなど）


    def set_password(self, password):
        """
        引数のパスワードをハッシュ化してpassword_hashに格納する
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        引数のパスワードが本登録されているパスワードと一致するかを判断する
        """
        return check_password_hash(self.password_hash, password)

# 生徒テーブル
class Student(db.Model):
    """
    id(Integer): ユーザーID (Primary Key)->本サービスを利用するすべてのユーザーに配分(同一はないように分配する)
    elementary_school(String max_100 )
    """
    __tablename__ = 'Student'
    id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False, primary_key=True)
    elementary_school = db.Column(db.String(100), nullable=True)
    middle_school = db.Column(db.String(100),nullable=True)
    high_school = db.Column(db.String(100),nullable=True)
    age = db.Column(db.Integer,nullable=False)
    grade = db.Column(db.String(20))
    emergency_contact1 = db.Column(db.String(20), nullable=False)
    emergency_contact2 = db.Column(db.String(20), nullable=True)
    emergency_contact3 = db.Column(db.String(20), nullable=True)
    guardian_id = db.Column(db.Integer, db.ForeignKey('guardian.id'), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    postal_code = db.Column(db.String(10))
    gender = db.Column(db.String(10))
    classification_id = db.Column(db.String(14), unique=True, nullable=False)
    enrollment_years = db.Column(db.Integer, nullable=True)  # 追加: 塾在籍年数
    graduation_status = db.Column(db.String(20), nullable=True)  # 追加: 卒業 or 退会
    guardian_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

# 教師テーブル
class Teacher(db.Model):
    __tablename__ = 'Teacher'
    id = db.Column(db.Integer,db.ForeignKey('User.id'), nullable=False, primary_key=True)
    organization_id = db.Column(db.String(100), db.ForeignKey('Organization.organization_id'), nullable=False)
    department_id = db.Column(db.String(100),db.ForeignKey('Depertment.department_id'), nullable=False)
    hire_date = db.Column(db.Date, nullable=True)  # 追加: 勤務開始日
    permissions = db.Column(db.String(50), nullable=False, default="basic")

# 保護者テーブル
class Guardian(db.Model):
    __tablename__ = 'Guardian'
    id = db.Column(db.Integer,db.ForeignKey('User.id'), nullable=False, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=True)  # 追加: 連絡用メール






