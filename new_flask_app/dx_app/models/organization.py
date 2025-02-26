from dx_app.models import db

class Organization(db.Model):
    __tablename__ = 'Organization'
    organization_id = db.Column(db.Integer, primary_key=True)
    organization_name = db.Column(db.String(100), nullable=False)
    organization_depertment=db.Column(db.String(100), nullable=False)

class Depertment(db.Model):
    __tablename__ = 'Depertment'
    department_id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.String(100), db.ForeignKey('Organization.organization_id'), nullable=False)
    depertment_name = db.Column(db.String(100), nullable=False)

class Period(db.Model):
    __tablename__ = 'Period'
    period_id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.String(100), db.ForeignKey('Organization.organization_id'), nullable=False)
    depertment_id = db.Column(db.String(100), db.ForeignKey('Depertment.department_id'), nullable=False)
    period_name =db.Column(db.String(100), nullable=False)
    counter_number = db.Column(db.Integer, nullable=False)# 時限の何番目か

#お知らせ等
class Attention(db.Model):
    __tablename__ = 'Attention'
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.String(100), db.ForeignKey('Organization.organization_id'), nullable=False)
    department_id = db.Column(db.String(100),db.ForeignKey('Depertment.department_id'), nullable=False)
    attention_title=db.Column(db.String(100), nullable=False)
    statement = db.Column(db.String(2000), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    role = db.Column(db.String(50), nullable=False)

class Subject(db.Model):
    __tablename__ = 'Subject'
    subject_id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.String(100), db.ForeignKey('Organization.organization_id'), nullable=False)
    depertment_id = db.Column(db.String(100), db.ForeignKey('Depertment.department_id'), nullable=False)
    subject_name = db.Column(db.String(100), nullable=False)

class Booth(db.Model):
    __tablename__ = 'Booth'
    booth_id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.String(100), db.ForeignKey('Organization.organization_id'), nullable=False)
    depertment_id = db.Column(db.String(100), db.ForeignKey('Depertment.department_id'), nullable=False)
    booth_name = db.Column(db.String(100), nullable=False)