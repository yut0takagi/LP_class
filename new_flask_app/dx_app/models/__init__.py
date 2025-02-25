from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from dx_app.models.user import User, Student, Teacher, Guardian
from dx_app.models.shift import SubjectPossib, ShiftPossib, ShiftPeriod, ShiftComp
from dx_app.models.classroom import Organization, Period
