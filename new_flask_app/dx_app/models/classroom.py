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
    
class Attention(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organization = db.Column(db.String(100), db.ForeignKey('Organization.name'), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    attention_title=db.Column(db.String(100), nullable=False)
    statement = db.Column(db.String(2000), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    role = db.Column(db.String(50), nullable=False)