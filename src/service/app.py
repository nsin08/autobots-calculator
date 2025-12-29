"""
Service application entry point.
Minimal Flask service with health and metrics endpoints.
"""
from flask import Flask, jsonify, request
from datetime import datetime
import time

app = Flask(__name__)

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
    Performs basic arithmetic operations.
    
    Request body: {"operation": "add|subtract|multiply|divide", "a": number, "b": number}
    Returns: {"result": number} or {"error": "message"}
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400
    
    operation = data.get('operation')
    a = data.get('a')
    b = data.get('b')
    
    # Validate inputs
    if operation not in ['add', 'subtract', 'multiply', 'divide']:
        return jsonify({'error': 'Invalid operation'}), 400
    
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
    
    return jsonify({'result': result}), 200


@app.route('/', methods=['GET'])
def root():
    """Root endpoint with service info."""
    return jsonify({
        'service': 'autobots-calculator',
        'version': '0.1.0',
        'endpoints': ['/health', '/metrics', '/api/calculate']
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
