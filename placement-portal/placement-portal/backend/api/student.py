import os
import uuid
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from extensions import db, cache
from models import Student, Drive, Application
from api.decorators import role_required, current_user_id

student_bp = Blueprint("student", __name__)


def _get_student_or_404():
    return Student.query.filter_by(user_id=current_user_id()).first()


def _allowed_resume(filename):
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in current_app.config["ALLOWED_RESUME_EXTENSIONS"]


def _is_eligible(student, drive):
    if drive.min_cgpa and (student.cgpa is None or student.cgpa < drive.min_cgpa):
        return False, "Your CGPA does not meet the eligibility criteria"
    if drive.grad_year_eligible and student.grad_year != drive.grad_year_eligible:
        return False, "Your graduation year does not match the eligibility criteria"
    if drive.branch_eligible:
        allowed_branches = [b.strip().lower() for b in drive.branch_eligible.split(",") if b.strip()]
        if allowed_branches and (student.branch or "").strip().lower() not in allowed_branches:
            return False, "Your branch is not eligible for this drive"
    return True, None


# ---------------------------------------------------------------------------
# Profile
# ---------------------------------------------------------------------------
@student_bp.route("/profile", methods=["GET"])
@role_required("student")
def get_profile():
    student = _get_student_or_404()
    if not student:
        return jsonify({"error": "Student profile not found"}), 404
    return jsonify(student.to_dict(include_email=True)), 200


@student_bp.route("/profile", methods=["PUT"])
@role_required("student")
def update_profile():
    student = _get_student_or_404()
    if not student:
        return jsonify({"error": "Student profile not found"}), 404

    data = request.get_json(force=True) or {}
    for field in ("name", "branch", "cgpa", "grad_year", "phone"):
        if field in data:
            setattr(student, field, data[field])
    db.session.commit()
    return jsonify(student.to_dict(include_email=True)), 200


@student_bp.route("/profile/resume", methods=["POST"])
@role_required("student")
def upload_resume():
    student = _get_student_or_404()
    if not student:
        return jsonify({"error": "Student profile not found"}), 404

    if "resume" not in request.files:
        return jsonify({"error": "No file part named 'resume' in request"}), 400
    file = request.files["resume"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    if not _allowed_resume(file.filename):
        return jsonify({"error": "Only PDF, DOC, DOCX files are allowed"}), 400

    ext = file.filename.rsplit(".", 1)[-1].lower()
    unique_name = f"{student.user_id}_{uuid.uuid4().hex}.{ext}"
    save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], unique_name)
    file.save(save_path)

    student.resume_path = unique_name
    db.session.commit()

    return jsonify({"message": "Resume uploaded", "resume_path": unique_name}), 200


# ---------------------------------------------------------------------------
# Browse drives
# ---------------------------------------------------------------------------
@cache.memoize(timeout=30)
def _fetch_approved_drives(search, branch):
    """
    Memoized (not @cache.cached) so it can be reliably invalidated via
    cache.delete_memoized() whenever a drive's approval status changes
    (approve/reject/edit-forces-re-approval/close).
    """
    query = Drive.query.filter_by(status="Approved")
    if search:
        query = query.filter(Drive.job_title.ilike(f"%{search}%"))
    if branch:
        query = query.filter(Drive.branch_eligible.ilike(f"%{branch}%"))
    drives = query.order_by(Drive.application_deadline.asc()).all()
    return [d.to_dict() for d in drives]


def invalidate_drive_list_cache():
    """
    Called whenever a drive's status changes in a way that could affect the
    approved-drives list shown to students (approve, reject, edit forcing
    re-approval, close). Clears every (search, branch) variant that has
    been cached, since memoize keys vary by argument combination.
    """
    cache.delete_memoized(_fetch_approved_drives)


@student_bp.route("/drives", methods=["GET"])
@role_required("student")
def list_approved_drives():
    search = request.args.get("q")
    branch = request.args.get("branch")
    return jsonify(_fetch_approved_drives(search, branch)), 200


# ---------------------------------------------------------------------------
# Apply
# ---------------------------------------------------------------------------
@student_bp.route("/drives/<int:drive_id>/apply", methods=["POST"])
@role_required("student")
def apply_to_drive(drive_id):
    student = _get_student_or_404()
    if not student:
        return jsonify({"error": "Student profile not found"}), 404

    drive = Drive.query.get_or_404(drive_id)
    if drive.status != "Approved":
        return jsonify({"error": "This drive is not currently open for applications"}), 400

    from datetime import datetime
    if drive.application_deadline and datetime.utcnow() > drive.application_deadline:
        return jsonify({"error": "The application deadline for this drive has passed"}), 400

    existing = Application.query.filter_by(student_id=student.id, drive_id=drive_id).first()
    if existing:
        return jsonify({"error": "You have already applied to this drive"}), 409

    eligible, reason = _is_eligible(student, drive)
    if not eligible:
        return jsonify({"error": reason}), 403

    application = Application(student_id=student.id, drive_id=drive_id, status="Applied")
    db.session.add(application)
    db.session.commit()

    return jsonify(
        {"message": "Application submitted", "application": application.to_dict(with_drive=True)}
    ), 201


# ---------------------------------------------------------------------------
# Application status / history
# ---------------------------------------------------------------------------
@student_bp.route("/applications", methods=["GET"])
@role_required("student")
def my_applications():
    student = _get_student_or_404()
    if not student:
        return jsonify({"error": "Student profile not found"}), 404

    apps = (
        Application.query.filter_by(student_id=student.id)
        .order_by(Application.applied_on.desc())
        .all()
    )
    return jsonify([a.to_dict(with_drive=True) for a in apps]), 200


# ---------------------------------------------------------------------------
# Async CSV export (Celery)
# ---------------------------------------------------------------------------
@student_bp.route("/applications/export", methods=["POST"])
@role_required("student")
def export_applications():
    student = _get_student_or_404()
    if not student:
        return jsonify({"error": "Student profile not found"}), 404

    from tasks import export_applications_csv_task

    task = export_applications_csv_task.delay(student.id)
    return jsonify(
        {"message": "Export started. You'll be notified when it's ready.", "task_id": task.id}
    ), 202


@student_bp.route("/applications/export/status/<task_id>", methods=["GET"])
@role_required("student")
def export_status(task_id):
    from tasks import export_applications_csv_task

    result = export_applications_csv_task.AsyncResult(task_id)
    payload = {"task_id": task_id, "state": result.state}
    if result.state == "SUCCESS":
        payload["result"] = result.result
    elif result.state == "FAILURE":
        payload["error"] = str(result.info)
    return jsonify(payload), 200
