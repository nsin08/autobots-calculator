"""
Custom decorators for route protection.
"""
from functools import wraps
from flask import jsonify
from flask_login import current_user


def login_required(f):
    """
    Decorator to require authentication for routes.
    
    Returns 401 with JSON error if user is not authenticated.
    
    Usage:
        @app.route('/protected')
        @login_required
        def protected_route():
            return jsonify({'data': 'secret'})
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function
