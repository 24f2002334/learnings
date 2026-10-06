from app import db

class PlacementDrive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company_profile.id'), nullable=False)
    job_title = db.Column(db.String(100))
    description = db.Column(db.Text)
    eligibility = db.Column(db.String(200))
    deadline = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='pending')

    company = db.relationship('CompanyProfile', backref='drives')
