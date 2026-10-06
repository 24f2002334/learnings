from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity


def role_required(*allowed_roles):
    """
    Decorator that verifies a valid JWT is present AND that its `role`
    claim is one of `allowed_roles`. Use like:

        @admin_bp.route("/companies")
        @role_required("admin")
        def list_companies(): ...
    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("role") not in allowed_roles:
                return jsonify({"error": "Forbidden: insufficient role"}), 403
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def current_user_id():
    return int(get_jwt_identity())
