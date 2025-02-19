from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, EmailField, TelField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField("メールアドレス", validators=[DataRequired(), Email()])
    password = PasswordField("パスワード", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("ログイン")

class RegisterForm(FlaskForm):
    name = StringField("氏名", validators=[DataRequired(), Length(max=50)])
    email = StringField("メールアドレス", validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField("パスワード", validators=[
        DataRequired(),
        Length(min=6, max=50),
        EqualTo("confirm_password", message="パスワードが一致しません")
    ])
    confirm_password = PasswordField("パスワード（確認）", validators=[DataRequired()])
    user_type = SelectField("アカウントタイプ", choices=[("individual", "個人"), ("cram", "塾生")], validators=[DataRequired()])

    submit = SubmitField("登録")

class ShiftSubmissionForm(FlaskForm):
    date = DateField("日付", validators=[DataRequired()])
    period = SelectField("時限", choices=[("1", "1限"), ("2", "2限"), ("3", "3限"), ("4", "4限"), ("5", "5限")], validators=[DataRequired()])
    submit = SubmitField("シフトを提出")
