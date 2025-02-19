from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField("メールアドレス", validators=[DataRequired(), Email()])
    password = PasswordField("パスワード", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("ログイン")

from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo

class RegisterForm(FlaskForm):
    username = StringField("ユーザー名", validators=[DataRequired()])
    email = StringField("メールアドレス", validators=[DataRequired(), Email()])
    password = PasswordField("パスワード", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("パスワード（確認用）", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("登録")

from wtforms import SelectField, DateField

class ShiftSubmissionForm(FlaskForm):
    date = DateField("日付", validators=[DataRequired()])
    period = SelectField("時限", choices=[("1", "1限"), ("2", "2限"), ("3", "3限"), ("4", "4限"), ("5", "5限")], validators=[DataRequired()])
    submit = SubmitField("シフトを提出")


