import os
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app, send_file
from extensions import db, cache
from models import User, Company, Drive, Application, Student
from api.decorators import role_required, current_user_id
from utils.offer_letter import generate_offer_letter_pdf

company_bp = Blueprint("company", __name__)

VALID_APP_STATUSES = {"Applied", "Shortlisted", "Selected", "Rejected"}


def _get_company_or_404():
    """Resolve the Company row belonging to the currently authenticated company user."""
    company = Company.query.filter_by(user_id=current_user_id()).first()
    return company


# ---------------------------------------------------------------------------
# Profile
# ---------------------------------------------------------------------------
@company_bp.route("/profile", methods=["GET"])
@role_required("company")
def get_profile():
    company = _get_company_or_404()
    if not company:
        return jsonify({"error": "Company profile not found"}), 404
    return jsonify(company.to_dict(include_email=True)), 200


@company_bp.route("/profile", methods=["PUT"])
@role_required("company")
def update_profile():
    company = _get_company_or_404()
    if not company:
        return jsonify({"error": "Company profile not found"}), 404

    data = request.get_json(force=True) or {}
    for field in ("name", "hr_contact", "website", "description"):
        if field in data:
            setattr(company, field, data[field])
    db.session.commit()
    return jsonify(company.to_dict(include_email=True)), 200


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------
@company_bp.route("/dashboard", methods=["GET"])
@role_required("company")
def dashboard():
    company = _get_company_or_404()
    if not company:
        return jsonify({"error": "Company profile not found"}), 404

    drives = Drive.query.filter_by(company_id=company.id).order_by(Drive.id.desc()).all()
    drive_data = []
    for d in drives:
        count = Application.query.filter_by(drive_id=d.id).count()
        drive_data.append(d.to_dict(with_company=False, applicant_count=count))

    return jsonify({"company": company.to_dict(), "drives": drive_data}), 200


# ---------------------------------------------------------------------------
# Drives
# ---------------------------------------------------------------------------
@company_bp.route("/drives", methods=["POST"])
@role_required("company")
def create_drive():
    company = _get_company_or_404()
    if not company:
        return jsonify({"error": "Company profile not found"}), 404
    if company.approval_status != "Approved":
        return jsonify({"error": "Your company must be approved by admin before creating drives"}), 403

    data = request.get_json(force=True) or {}
    required = ["job_title", "application_deadline"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    try:
        deadline = datetime.fromisoformat(data["application_deadline"])
    except ValueError:
        return jsonify({"error": "application_deadline must be an ISO datetime string"}), 400

    if deadline <= datetime.utcnow():
        return jsonify({"error": "application_deadline must be in the future"}), 400

    drive = Drive(
        company_id=company.id,
        job_title=data["job_title"],
        job_description=data.get("job_description"),
        branch_eligible=data.get("branch_eligible"),
        min_cgpa=data.get("min_cgpa", 0.0),
        grad_year_eligible=data.get("grad_year_eligible"),
        application_deadline=deadline,
        status="Pending",  # requires admin approval
    )
    db.session.add(drive)
    db.session.commit()
    # New drive starts Pending, so it doesn't affect the student-facing
    # Approved list yet; admin dashboard's pending_drives count does change.
    from api.admin import invalidate_admin_dashboard_cache

    invalidate_admin_dashboard_cache()

    return jsonify({"message": "Drive created, pending admin approval", "drive": drive.to_dict()}), 201


@company_bp.route("/drives/<int:drive_id>", methods=["PUT"])
@role_required("company")
def update_drive(drive_id):
    company = _get_company_or_404()
    drive = Drive.query.get_or_404(drive_id)
    if drive.company_id != company.id:
        return jsonify({"error": "Forbidden"}), 403

    data = request.get_json(force=True) or {}
    for field in ("job_title", "job_description", "branch_eligible", "min_cgpa", "grad_year_eligible"):
        if field in data:
            setattr(drive, field, data[field])
    if "application_deadline" in data:
        try:
            drive.application_deadline = datetime.fromisoformat(data["application_deadline"])
        except ValueError:
            return jsonify({"error": "application_deadline must be an ISO datetime string"}), 400

    # Editing a drive sends it back for re-approval to keep admin in the loop
    was_approved = drive.status == "Approved"
    if was_approved:
        drive.status = "Pending"

    db.session.commit()

    if was_approved:
        # Drive just dropped out of the Approved list students see
        from api.admin import invalidate_admin_dashboard_cache
        from api.student import invalidate_drive_list_cache

        invalidate_admin_dashboard_cache()
        invalidate_drive_list_cache()

    return jsonify(drive.to_dict()), 200


@company_bp.route("/drives/<int:drive_id>/close", methods=["POST"])
@role_required("company")
def close_drive(drive_id):
    company = _get_company_or_404()
    drive = Drive.query.get_or_404(drive_id)
    if drive.company_id != company.id:
        return jsonify({"error": "Forbidden"}), 403
    drive.status = "Closed"
    db.session.commit()

    from api.student import invalidate_drive_list_cache

    invalidate_drive_list_cache()  # closed drive must disappear from student view immediately

    return jsonify({"message": "Drive closed", "drive": drive.to_dict()}), 200


# ---------------------------------------------------------------------------
# Applications: view, shortlist, update status, schedule interview
# ---------------------------------------------------------------------------
@company_bp.route("/drives/<int:drive_id>/applications", methods=["GET"])
@role_required("company")
def list_drive_applications(drive_id):
    company = _get_company_or_404()
    drive = Drive.query.get_or_404(drive_id)
    if drive.company_id != company.id:
        return jsonify({"error": "Forbidden"}), 403

    apps = Application.query.filter_by(drive_id=drive_id).order_by(Application.id.desc()).all()
    result = []
    for a in apps:
        d = a.to_dict(with_student=True)
        if a.student:
            d["student_branch"] = a.student.branch
            d["student_cgpa"] = a.student.cgpa
            d["student_resume_path"] = a.student.resume_path
        result.append(d)
    return jsonify(result), 200


@company_bp.route("/applications/<int:application_id>/status", methods=["PUT"])
@role_required("company")
def update_application_status(application_id):
    company = _get_company_or_404()
    application = Application.query.get_or_404(application_id)
    drive = Drive.query.get(application.drive_id)
    if not drive or drive.company_id != company.id:
        return jsonify({"error": "Forbidden"}), 403

    data = request.get_json(force=True) or {}
    new_status = data.get("status")
    if new_status not in VALID_APP_STATUSES:
        return jsonify({"error": f"status must be one of {sorted(VALID_APP_STATUSES)}"}), 400

    application.status = new_status
    if "remarks" in data:
        application.remarks = data["remarks"]
    if "interview_datetime" in data and data["interview_datetime"]:
        try:
            application.interview_datetime = datetime.fromisoformat(data["interview_datetime"])
        except ValueError:
            return jsonify({"error": "interview_datetime must be an ISO datetime string"}), 400

    db.session.commit()
    return jsonify(application.to_dict(with_drive=True, with_student=True)), 200


# ---------------------------------------------------------------------------
# Optional feature: dummy offer letter generator (company side)
# ---------------------------------------------------------------------------
@company_bp.route("/applications/<int:application_id>/offer-letter", methods=["GET"])
@role_required("company")
def download_offer_letter(application_id):
    company = _get_company_or_404()
    application = Application.query.get_or_404(application_id)
    drive = Drive.query.get(application.drive_id)
    if not drive or drive.company_id != company.id:
        return jsonify({"error": "Forbidden"}), 403

    if application.status != "Selected":
        return jsonify({"error": "Offer letters can only be generated for Selected candidates"}), 400

    student = application.student
    if not student:
        return jsonify({"error": "Student record not found"}), 404

    export_folder = current_app.config["EXPORT_FOLDER"]
    filename = f"offer_letter_{application.id}_{uuid.uuid4().hex[:8]}.pdf"
    filepath = os.path.join(export_folder, filename)

    generate_offer_letter_pdf(
        company_name=company.name,
        student_name=student.name,
        job_title=drive.job_title,
        output_path=filepath,
    )

    return send_file(
        filepath,
        as_attachment=True,
        download_name=f"Offer_Letter_{student.name.replace(' ', '_')}.pdf",
        mimetype="application/pdf",
    )
