from functools import wraps
from flask import abort
from flask_login import current_user
from .models import UserRole

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(403) 
        if current_user.role != UserRole.ADMIN:
            print(f"User role: {UserRole.ADMIN}")  # Debugging line
            abort(403) 
        return f(*args, **kwargs)
    return decorated_function