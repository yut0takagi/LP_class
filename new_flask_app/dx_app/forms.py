from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, EmailField, TelField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField("メールアドレス", validators=[DataRequired(), Email()])
    password = PasswordField("パスワード", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("ログイン")

class RegisterForm(FlaskForm):
    student_id = StringField("生徒ID", validators=[DataRequired(), Length(min=1, max=10)])
    email = EmailField("メールアドレス", validators=[DataRequired(), Email()])
    phone = TelField("電話番号", validators=[DataRequired(), Length(min=10, max=15)])
    emergency_phone1 = TelField("緊急連絡先1")
    emergency_phone2 = TelField("緊急連絡先2")
    emergency_phone3 = TelField("緊急連絡先3")
    dob = DateField("生年月日", validators=[DataRequired()])
    gender = SelectField("性別", choices=[("male", "男性"), ("female", "女性"), ("other", "その他")])
    address = StringField("住所", validators=[DataRequired(), Length(min=5, max=255)])
    password = PasswordField("パスワード", validators=[
        DataRequired(),
        Length(min=6, max=128),
        EqualTo("confirm_password", message="パスワードが一致しません")
    ])
    confirm_password = PasswordField("パスワード（確認用）", validators=[DataRequired()])

class ShiftSubmissionForm(FlaskForm):
    date = DateField("日付", validators=[DataRequired()])
    period = SelectField("時限", choices=[("1", "1限"), ("2", "2限"), ("3", "3限"), ("4", "4限"), ("5", "5限")], validators=[DataRequired()])
    submit = SubmitField("シフトを提出")
