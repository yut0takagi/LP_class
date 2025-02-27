from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, EmailField, TelField, SelectField, BooleanField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional
from wtforms.widgets import HiddenInput
from  utils import get_data_by_filting

class AgencySearch(FlaskForm):
    grade=SelectField("学年",choices=[("elementary_school","小学生"),("junior_high_school","中学生"),("high_school","高校生")])
    subject = SelectField("科目", choices=[("math","数学"),("english","英語"),("science","理科")])
    date_from = DateField("日付", validators=[DataRequired()])
    date_to = DateField("日付", validators=[DataRequired()])
    submit = SubmitField("シフトを提出")
