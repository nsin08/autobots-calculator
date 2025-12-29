"""
Service application entry point.
Minimal Flask service with health and metrics endpoints.
"""
from flask import Flask, jsonify
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


@app.route('/', methods=['GET'])
def root():
    """Root endpoint with service info."""
    return jsonify({
        'service': 'autobots-service-readiness-baseline',
        'version': '0.1.0',
        'endpoints': ['/health', '/metrics']
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
