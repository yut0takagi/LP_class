from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from dx_app.models.organization import Organization, Depertment, Period, Attention, Subject, Booth
from dx_app.models.user import User, Student, Educator, Guardian
from dx_app.models.shift import SubjectPossib, ShiftPossib,ShiftSubmission, ShiftComp

