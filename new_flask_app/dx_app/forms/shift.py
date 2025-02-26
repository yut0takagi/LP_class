from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, EmailField, TelField, SelectField, BooleanField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional
from wtforms.widgets import HiddenInput


class ShiftSubmissionForm(FlaskForm):
    date = DateField("日付", validators=[DataRequired()])
    period = SelectField("時限", choices=[("1", "1限"), ("2", "2限"), ("3", "3限"), ("4", "4限"), ("5", "5限")], validators=[DataRequired()])
    submit = SubmitField("シフトを提出")
