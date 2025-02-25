from dx_app.models import db

class Organization(db.Model):
    __tablename__ = 'Organization'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    depertment=db.Column(db.String(100), nullable=False)

class Period(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organization = db.Column(db.String(100), db.ForeignKey('Organization.name'), nullable=False)
    name=db.Column(db.String(100), nullable=False)
    