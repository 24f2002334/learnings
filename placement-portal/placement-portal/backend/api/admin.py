from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from extensions import db, cache
from models import User, Student, Company, Drive, Application
from api.decorators import role_required

admin_bp = Blueprint("admin", __name__)


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------
@cache.memoize(timeout=30)
def _compute_dashboard_stats():
    """
    Memoized (not @cache.cached — that decorator caches by Flask view/request
    and cannot be reliably invalidated with delete_memoized). This plain
    function is memoized instead, and the route below just calls it, so
    `_compute_dashboard_stats.uncache()`-style invalidation via
    cache.delete_memoized() actually works when data changes.
    """
    return {
        "total_students": Student.query.count(),
        "total_companies": Company.query.count(),
        "total_drives": Drive.query.count(),
        "pending_companies": Company.query.filter_by(approval_status="Pending").count(),
        "pending_drives": Drive.query.filter_by(status="Pending").count(),
        "total_applications": Application.query.count(),
        "selected_count": Application.query.filter_by(status="Selected").count(),
    }


def invalidate_admin_dashboard_cache():
    cache.delete_memoized(_compute_dashboard_stats)


@admin_bp.route("/dashboard", methods=["GET"])
@role_required("admin")
def dashboard():
    return jsonify(_compute_dashboard_stats()), 200


# ---------------------------------------------------------------------------
# Companies: list / approve / reject / blacklist
# ---------------------------------------------------------------------------
@admin_bp.route("/companies", methods=["GET"])
@role_required("admin")
def list_companies():
    status = request.args.get("status")  # optional filter: Pending/Approved/Rejected
    search = request.args.get("q")

    query = Company.query
    if status:
        query = query.filter_by(approval_status=status)
    if search:
        query = query.filter(Company.name.ilike(f"%{search}%"))

    companies = query.order_by(Company.id.desc()).all()
    return jsonify([c.to_dict(include_email=True) for c in companies]), 200


@admin_bp.route("/companies/<int:company_id>/approve", methods=["POST"])
@role_required("admin")
def approve_company(company_id):
    company = Company.query.get_or_404(company_id)
    company.approval_status = "Approved"
    db.session.commit()
    invalidate_admin_dashboard_cache()
    return jsonify({"message": "Company approved", "company": company.to_dict()}), 200


@admin_bp.route("/companies/<int:company_id>/reject", methods=["POST"])
@role_required("admin")
def reject_company(company_id):
    company = Company.query.get_or_404(company_id)
    company.approval_status = "Rejected"
    db.session.commit()
    invalidate_admin_dashboard_cache()
    return jsonify({"message": "Company rejected", "company": company.to_dict()}), 200


@admin_bp.route("/companies/<int:company_id>/deactivate", methods=["POST"])
@role_required("admin")
def deactivate_company(company_id):
    company = Company.query.get_or_404(company_id)
    company.user.is_active = False
    db.session.commit()
    return jsonify({"message": "Company blacklisted/deactivated"}), 200


@admin_bp.route("/companies/<int:company_id>/activate", methods=["POST"])
@role_required("admin")
def activate_company(company_id):
    company = Company.query.get_or_404(company_id)
    company.user.is_active = True
    db.session.commit()
    return jsonify({"message": "Company reactivated"}), 200


# ---------------------------------------------------------------------------
# Students: list / blacklist
# ---------------------------------------------------------------------------
@admin_bp.route("/students", methods=["GET"])
@role_required("admin")
def list_students():
    search = request.args.get("q")
    query = Student.query
    if search:
        query = query.filter(
            or_(Student.name.ilike(f"%{search}%"), Student.branch.ilike(f"%{search}%"))
        )
    students = query.order_by(Student.id.desc()).all()
    return jsonify([s.to_dict(include_email=True) for s in students]), 200


@admin_bp.route("/students/<int:student_id>/deactivate", methods=["POST"])
@role_required("admin")
def deactivate_student(student_id):
    student = Student.query.get_or_404(student_id)
    student.user.is_active = False
    db.session.commit()
    return jsonify({"message": "Student blacklisted/deactivated"}), 200


@admin_bp.route("/students/<int:student_id>/activate", methods=["POST"])
@role_required("admin")
def activate_student(student_id):
    student = Student.query.get_or_404(student_id)
    student.user.is_active = True
    db.session.commit()
    return jsonify({"message": "Student reactivated"}), 200


# ---------------------------------------------------------------------------
# Drives: list / approve / reject
# ---------------------------------------------------------------------------
@admin_bp.route("/drives", methods=["GET"])
@role_required("admin")
def list_drives():
    status = request.args.get("status")
    query = Drive.query
    if status:
        query = query.filter_by(status=status)
    drives = query.order_by(Drive.id.desc()).all()

    result = []
    for d in drives:
        count = Application.query.filter_by(drive_id=d.id).count()
        result.append(d.to_dict(applicant_count=count))
    return jsonify(result), 200


@admin_bp.route("/drives/<int:drive_id>/approve", methods=["POST"])
@role_required("admin")
def approve_drive(drive_id):
    from api.student import invalidate_drive_list_cache

    drive = Drive.query.get_or_404(drive_id)
    drive.status = "Approved"
    db.session.commit()
    invalidate_admin_dashboard_cache()
    invalidate_drive_list_cache()
    return jsonify({"message": "Drive approved", "drive": drive.to_dict()}), 200


@admin_bp.route("/drives/<int:drive_id>/reject", methods=["POST"])
@role_required("admin")
def reject_drive(drive_id):
    from api.student import invalidate_drive_list_cache

    drive = Drive.query.get_or_404(drive_id)
    drive.status = "Rejected"
    db.session.commit()
    invalidate_admin_dashboard_cache()
    invalidate_drive_list_cache()  # drive may have been Approved before; remove from student view
    return jsonify({"message": "Drive rejected", "drive": drive.to_dict()}), 200


# ---------------------------------------------------------------------------
# Applications overview (read-only, for admin visibility)
# ---------------------------------------------------------------------------
@admin_bp.route("/applications", methods=["GET"])
@role_required("admin")
def list_all_applications():
    apps = Application.query.order_by(Application.id.desc()).all()
    return jsonify([a.to_dict(with_drive=True, with_student=True) for a in apps]), 200

