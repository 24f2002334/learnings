from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db


class User(db.Model):
    """
    Unified user model. Every login (admin/company/student) is a row here.
    `role` differentiates the three types. Student/Company profile data
    lives in satellite tables linked 1:1 via user_id.
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin' | 'company' | 'student'
    is_active = db.Column(db.Boolean, default=True, nullable=False)  # blacklist/deactivate flag
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    student_profile = db.relationship(
        "Student", backref="user", uselist=False, cascade="all, delete-orphan"
    )
    company_profile = db.relationship(
        "Company", backref="user", uselist=False, cascade="all, delete-orphan"
    )

    def set_password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password_hash, raw_password)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "role": self.role,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)

    name = db.Column(db.String(120), nullable=False)
    branch = db.Column(db.String(80))
    cgpa = db.Column(db.Float)
    grad_year = db.Column(db.Integer)
    phone = db.Column(db.String(20))
    resume_path = db.Column(db.String(255))  # relative path under uploads/resumes

    applications = db.relationship(
        "Application", backref="student", cascade="all, delete-orphan"
    )

    def to_dict(self, include_email=False):
        data = {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "branch": self.branch,
            "cgpa": self.cgpa,
            "grad_year": self.grad_year,
            "phone": self.phone,
            "resume_path": self.resume_path,
            "is_active": self.user.is_active if self.user else None,
        }
        if include_email and self.user:
            data["email"] = self.user.email
        return data


class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)

    name = db.Column(db.String(150), nullable=False)
    hr_contact = db.Column(db.String(120))
    website = db.Column(db.String(255))
    description = db.Column(db.Text)
    approval_status = db.Column(db.String(20), default="Pending")  # Pending/Approved/Rejected

    drives = db.relationship("Drive", backref="company", cascade="all, delete-orphan")

    def to_dict(self, include_email=False):
        data = {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "hr_contact": self.hr_contact,
            "website": self.website,
            "description": self.description,
            "approval_status": self.approval_status,
            "is_active": self.user.is_active if self.user else None,
        }
        if include_email and self.user:
            data["email"] = self.user.email
        return data


class Drive(db.Model):
    __tablename__ = "drives"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)

    job_title = db.Column(db.String(150), nullable=False)
    job_description = db.Column(db.Text)

    # Eligibility criteria
    branch_eligible = db.Column(db.String(255))  # comma-separated branches, empty = all
    min_cgpa = db.Column(db.Float, default=0.0)
    grad_year_eligible = db.Column(db.Integer)  # nullable = any year

    application_deadline = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default="Pending")  # Pending/Approved/Rejected/Closed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship(
        "Application", backref="drive", cascade="all, delete-orphan"
    )

    def to_dict(self, with_company=True, applicant_count=None):
        data = {
            "id": self.id,
            "company_id": self.company_id,
            "job_title": self.job_title,
            "job_description": self.job_description,
            "branch_eligible": self.branch_eligible,
            "min_cgpa": self.min_cgpa,
            "grad_year_eligible": self.grad_year_eligible,
            "application_deadline": self.application_deadline.isoformat()
            if self.application_deadline
            else None,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
        if with_company and self.company:
            data["company_name"] = self.company.name
        if applicant_count is not None:
            data["applicant_count"] = applicant_count
        return data


class Application(db.Model):
    __tablename__ = "applications"
    __table_args__ = (
        db.UniqueConstraint("student_id", "drive_id", name="uq_student_drive"),
    )

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey("drives.id"), nullable=False)

    applied_on = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="Applied")  # Applied/Shortlisted/Selected/Rejected
    interview_datetime = db.Column(db.DateTime)
    remarks = db.Column(db.Text)

    def to_dict(self, with_drive=False, with_student=False):
        data = {
            "id": self.id,
            "student_id": self.student_id,
            "drive_id": self.drive_id,
            "applied_on": self.applied_on.isoformat() if self.applied_on else None,
            "status": self.status,
            "interview_datetime": self.interview_datetime.isoformat()
            if self.interview_datetime
            else None,
            "remarks": self.remarks,
        }
        if with_drive and self.drive:
            data["drive_title"] = self.drive.job_title
            data["company_name"] = self.drive.company.name if self.drive.company else None
        if with_student and self.student:
            data["student_name"] = self.student.name
        return data
