"""
Authentication endpoints for user registration and login.
"""
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, current_user
from datetime import datetime
from src.service.database import db
from src.service.models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    
    Request body:
        {
            "username": str (3-50 chars, required),
            "email": str (valid email, required),
            "password": str (min 8 chars, required)
        }
    
    Returns:
        201: {"success": true, "user_id": int, "username": str}
        400: {"error": str} - validation error
        409: {"error": str} - username or email already exists
    """
    data = request.get_json()
    
    # Validate required fields
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400
    
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    # Validate username
    if not username:
        return jsonify({'error': 'Username is required'}), 400
    if len(username) < 3 or len(username) > 50:
        return jsonify({'error': 'Username must be 3-50 characters'}), 400
    
    # Validate email
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    if '@' not in email or '.' not in email.split('@')[-1]:
        return jsonify({'error': 'Invalid email format'}), 400
    if len(email) > 100:
        return jsonify({'error': 'Email must be less than 100 characters'}), 400
    
    # Validate password
    if not password:
        return jsonify({'error': 'Password is required'}), 400
    if len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters'}), 400
    
    # Check if username already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 409
    
    # Check if email already exists
    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        return jsonify({'error': 'Email already exists'}), 409
    
    # Create new user
    user = User(username=username, email=email)
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'user_id': user.id,
        'username': user.username
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticate user and create session.
    
    Request body:
        {
            "username": str (required),
            "password": str (required)
        }
    
    Returns:
        200: {"success": true, "user_id": int, "username": str}
        400: {"error": str} - validation error
        401: {"error": str} - invalid credentials
    """
    data = request.get_json()
    
    # Validate required fields
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400
    
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username:
        return jsonify({'error': 'Username is required'}), 400
    if not password:
        return jsonify({'error': 'Password is required'}), 400
    
    # Find user
    user = User.query.filter_by(username=username).first()
    
    # Verify password
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    # Create session
    login_user(user, remember=True, duration=None)  # 24h default from Flask-Login config
    
    return jsonify({
        'success': True,
        'user_id': user.id,
        'username': user.username
    }), 200


@auth_bp.route('/logout', methods=['GET'])
def logout():
    """
    Destroy user session.
    
    Returns:
        200: {"success": true, "message": str}
    """
    logout_user()
    return jsonify({
        'success': True,
        'message': 'Logged out successfully'
    }), 200


@auth_bp.route('/status', methods=['GET'])
def status():
    """
    Get current authenticated user status.
    
    Returns:
        200: {"authenticated": true, "user_id": int, "username": str} - if logged in
        200: {"authenticated": false} - if not logged in
    """
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user_id': current_user.id,
            'username': current_user.username
        }), 200
    else:
        return jsonify({
            'authenticated': False
        }), 200
