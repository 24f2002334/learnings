from app import db

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profile.id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drive.id'), nullable=False)
    date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='applied')

    student = db.relationship('StudentProfile', backref='applications')
    drive = db.relationship('PlacementDrive', backref='applications')
