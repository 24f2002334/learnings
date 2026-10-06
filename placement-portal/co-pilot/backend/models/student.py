from app import db

class StudentProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100))
    branch = db.Column(db.String(50))
    cgpa = db.Column(db.Float)
    year = db.Column(db.Integer)
    resume = db.Column(db.String(200))  # file path

    user = db.relationship('User', backref='student_profile')
