"""
Service application entry point.
Minimal Flask service with health and metrics endpoints.
"""
from flask import Flask, jsonify, request, send_from_directory
from datetime import datetime, timedelta
import time
import os
import math
from src.service.database import init_db, db
from src.service.models import User
from flask_login import LoginManager

app = Flask(__name__, static_folder='../../static')

# Configure Flask app
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# Initialize database
init_db(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = None  # API, no redirect

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    return User.query.get(int(user_id))

# Register blueprints
from src.service.auth import auth_bp
from src.service.history import history_bp
app.register_blueprint(auth_bp)
app.register_blueprint(history_bp)

# Track service start time
START_TIME = time.time()
REQUEST_COUNT = 0


@app.before_request
def count_request():
    """Increment request counter before each request."""
    global REQUEST_COUNT
    REQUEST_COUNT += 1


@app.route('/health', methods=['GET'])
def health():
    """
    Health endpoint.
    Returns 200 with status:ok when service is healthy.
    """
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }), 200


@app.route('/metrics', methods=['GET'])
def metrics():
    """
    Metrics endpoint.
    Returns basic service metrics: request count and uptime.
    """
    uptime = int(time.time() - START_TIME)
    return jsonify({
        'requests_total': REQUEST_COUNT,
        'uptime_seconds': uptime
    }), 200


@app.route('/api/calculate', methods=['POST'])
def calculate():
    """
    Calculate endpoint.
    Performs arithmetic and advanced mathematical operations.
    
    Request body: 
        Basic: {"operation": "add|subtract|multiply|divide", "a": number, "b": number}
        Advanced: {"operation": "factorial|power|modulo", "a": number, "b": number (if needed)}
    Returns: {"result": number} or {"error": "message"}
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400
    
    operation = data.get('operation')
    a = data.get('a')
    b = data.get('b')
    
    # Validate operation
    valid_operations = ['add', 'subtract', 'multiply', 'divide', 'factorial', 'power', 'modulo']
    if operation not in valid_operations:
        return jsonify({'error': 'Invalid operation'}), 400
    
    # Factorial only needs 'a'
    if operation == 'factorial':
        if a is None:
            return jsonify({'error': 'Missing operand'}), 400
        
        try:
            a = float(a)
        except (ValueError, TypeError):
            return jsonify({'error': 'Operand must be a number'}), 400
        
        # Validate factorial constraints
        if a < 0:
            return jsonify({'error': 'Factorial not defined for negative numbers'}), 400
        if a != int(a):
            return jsonify({'error': 'Factorial requires integer input'}), 400
        if a > 20:
            return jsonify({'error': 'Factorial input too large (max 20)'}), 400
        
        result = math.factorial(int(a))
        return jsonify({'result': result}), 200
    
    # All other operations need both 'a' and 'b'
    if a is None or b is None:
        return jsonify({'error': 'Missing operands'}), 400
    
    try:
        a = float(a)
        b = float(b)
    except (ValueError, TypeError):
        return jsonify({'error': 'Operands must be numbers'}), 400
    
    # Perform calculation
    if operation == 'add':
        result = a + b
    elif operation == 'subtract':
        result = a - b
    elif operation == 'multiply':
        result = a * b
    elif operation == 'divide':
        if b == 0:
            return jsonify({'error': 'Division by zero'}), 400
        result = a / b
    elif operation == 'power':
        # Validate power bounds
        if b > 100 or b < -100:
            return jsonify({'error': 'Exponent out of bounds (-100 to 100)'}), 400
        result = pow(a, b)
    elif operation == 'modulo':
        if b == 0:
            return jsonify({'error': 'Division by zero'}), 400
        result = a % b
    
    return jsonify({'result': result}), 200


@app.route('/', methods=['GET'])
def index():
    """Serve the calculator UI."""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api', methods=['GET'])
def api_info():
    """API info endpoint."""
    return jsonify({
        'service': 'autobots-calculator',
        'version': '0.1.0',
        'endpoints': ['/health', '/metrics', '/api/calculate']
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
