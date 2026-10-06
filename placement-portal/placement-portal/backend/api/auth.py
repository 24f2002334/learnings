from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity
from extensions import db
from models import User, Student, Company

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register/student", methods=["POST"])
def register_student():
    data = request.get_json(force=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    name = (data.get("name") or "").strip()

    if not email or not password or not name:
        return jsonify({"error": "email, password and name are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "An account with this email already exists"}), 409

    user = User(email=email, role="student")
    user.set_password(password)
    db.session.add(user)
    db.session.flush()  # get user.id before commit

    student = Student(
        user_id=user.id,
        name=name,
        branch=data.get("branch"),
        cgpa=data.get("cgpa"),
        grad_year=data.get("grad_year"),
        phone=data.get("phone"),
    )
    db.session.add(student)
    db.session.commit()

    return jsonify({"message": "Student registered successfully", "user": user.to_dict()}), 201


@auth_bp.route("/register/company", methods=["POST"])
def register_company():
    data = request.get_json(force=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    name = (data.get("name") or "").strip()

    if not email or not password or not name:
        return jsonify({"error": "email, password and company name are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "An account with this email already exists"}), 409

    user = User(email=email, role="company")
    user.set_password(password)
    db.session.add(user)
    db.session.flush()

    company = Company(
        user_id=user.id,
        name=name,
        hr_contact=data.get("hr_contact"),
        website=data.get("website"),
        description=data.get("description"),
        approval_status="Pending",
    )
    db.session.add(company)
    db.session.commit()

    return jsonify(
        {
            "message": "Company registered successfully. Awaiting admin approval.",
            "user": user.to_dict(),
        }
    ), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 401

    if not user.is_active:
        return jsonify({"error": "This account has been deactivated. Contact the admin."}), 403

    additional_claims = {"role": user.role}
    token = create_access_token(identity=str(user.id), additional_claims=additional_claims)

    profile = None
    if user.role == "student" and user.student_profile:
        profile = user.student_profile.to_dict()
    elif user.role == "company" and user.company_profile:
        profile = user.company_profile.to_dict()

    return jsonify(
        {
            "access_token": token,
            "user": user.to_dict(),
            "profile": profile,
        }
    ), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    profile = None
    if user.role == "student" and user.student_profile:
        profile = user.student_profile.to_dict()
    elif user.role == "company" and user.company_profile:
        profile = user.company_profile.to_dict()

    return jsonify({"user": user.to_dict(), "profile": profile}), 200
