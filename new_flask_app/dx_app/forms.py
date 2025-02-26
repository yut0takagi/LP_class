from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, EmailField, TelField, SelectField, BooleanField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional
from wtforms.widgets import HiddenInput

class LoginForm(FlaskForm):
    email = StringField("メールアドレス", validators=[DataRequired(), Email()])
    password = PasswordField("パスワード", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("ログイン")

class RegisterForm(FlaskForm):
    id = StringField("ID", widget=HiddenInput())
    name = StringField("氏名", validators=[DataRequired(), Length(max=50)])
    email = StringField("メールアドレス", validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField("パスワード", validators=[
        DataRequired(),
        Length(min=6, max=50),
        EqualTo("confirm_password", message="パスワードが一致しません")
    ])
    confirm_password = PasswordField("パスワード（確認）", validators=[DataRequired()])
    user_type = SelectField("アカウントタイプ", choices=[("student", "学生"), ("teacher", "教務スタッフ"),("admin", "管理者")], validators=[DataRequired()])

    submit = SubmitField("登録")

class RegistrationFormForStudent1(FlaskForm):
    user_type = SelectField(
        "登録種別を選択してください",
        choices=[("", "選択してください"), ("cram", "塾生"), ("individual", "個人")],
        validators=[DataRequired(message="登録種別を選択してください")],
        default=""
    )
    submit = SubmitField("次へ")

class CramForm(FlaskForm):
    elementary_school = StringField("小学校", validators=[Optional(), Length(max=100)])
    middle_school = StringField("中学校", validators=[Optional(), Length(max=100)])
    high_school = StringField("高校", validators=[Optional(), Length(max=100)])
    age = IntegerField("年齢", validators=[DataRequired()])
    grade = StringField("学年", validators=[Optional(), Length(max=20)])
    emergency_contact1_name = StringField("緊急連絡先1 氏名", validators=[DataRequired(), Length(max=50)])
    emergency_contact1_number = TelField("緊急連絡先1 電話番号", validators=[DataRequired(), Length(max=20)])
    emergency_contact2_name = StringField("緊急連絡先2 氏名", validators=[Optional(), Length(max=50)])
    emergency_contact2_number = TelField("緊急連絡先2 電話番号", validators=[Optional(), Length(max=20)])
    emergency_contact3_name = StringField("緊急連絡先3 氏名", validators=[Optional(), Length(max=50)])
    emergency_contact3_number = TelField("緊急連絡先3 電話番号", validators=[Optional(), Length(max=20)])
    address = StringField("住所", validators=[Optional(), Length(max=255)])
    postal_code = StringField("郵便番号", validators=[Optional(), Length(max=10)])
    gender = SelectField("性別", choices=[("male", "男性"), ("female", "女性"), ("other", "その他"), ("no_choice", "回答しない")], validators=[Optional()])
    organization_id = StringField("所属ID", validators=[DataRequired(), Length(max=14)])
    depertment_id = StringField("教室ID", validators=[DataRequired(), Length(max=14)])
    enrollment_years = IntegerField("在籍年数", validators=[Optional()])
    graduation_status = SelectField("卒業状況", choices=[("在籍", "在籍"), ("卒業", "卒業"), ("退会", "退会")], validators=[Optional()])
    guardian_id = StringField("保護者ID", validators=[DataRequired(), Length(max=14)])
    submit = SubmitField("登録")

class IndividualForm(FlaskForm):
    elementary_school = StringField("小学校", validators=[Optional(), Length(max=100)])
    middle_school = StringField("中学校", validators=[Optional(), Length(max=100)])
    high_school = StringField("高校", validators=[Optional(), Length(max=100)])
    age = IntegerField("年齢", validators=[DataRequired()])
    grade = StringField("学年", validators=[Optional(), Length(max=20)])
    address = StringField("住所", validators=[Optional(), Length(max=255)])
    postal_code = StringField("郵便番号", validators=[Optional(), Length(max=10)])
    gender = SelectField("性別", choices=[("male", "男性"), ("female", "女性"), ("other", "その他"), ("no_choice", "回答しない")], validators=[Optional()])
    submit = SubmitField("登録")

class StudentForm(FlaskForm):
    elementary_school = StringField("小学校", validators=[Optional(), Length(max=100)])
    middle_school = StringField("中学校", validators=[Optional(), Length(max=100)])
    high_school = StringField("高校", validators=[Optional(), Length(max=100)])
    age = IntegerField("年齢", validators=[DataRequired()])
    grade = StringField("学年", validators=[Optional(), Length(max=20)])
    emergency_contact1 = StringField("緊急連絡先1", validators=[DataRequired(), Length(max=20)])
    emergency_contact2 = StringField("緊急連絡先2", validators=[Optional(), Length(max=20)])
    emergency_contact3 = StringField("緊急連絡先3", validators=[Optional(), Length(max=20)])
    address = StringField("住所", validators=[Optional(), Length(max=255)])
    postal_code = StringField("郵便番号", validators=[Optional(), Length(max=10)])
    gender = SelectField("性別", choices=[("male", "男性"), ("female", "女性"), ("other", "その他"), ("no_choice", "回答しない")], validators=[Optional()])
    organization_id = StringField("所属ID", validators=[DataRequired(), Length(max=14)])
    depertment_id = StringField("教室ID", validators=[DataRequired(), Length(max=14)])
    enrollment_years = IntegerField("在籍年数", validators=[Optional()])
    graduation_status = SelectField("卒業状況", choices=[("在籍", "在籍"), ("卒業", "卒業"), ("退会", "退会")], validators=[Optional()])
    submit = SubmitField("登録")

class ShiftSubmissionForm(FlaskForm):
    date = DateField("日付", validators=[DataRequired()])
    period = SelectField("時限", choices=[("1", "1限"), ("2", "2限"), ("3", "3限"), ("4", "4限"), ("5", "5限")], validators=[DataRequired()])
    submit = SubmitField("シフトを提出")
