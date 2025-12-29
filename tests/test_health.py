"""
Tests for /health endpoint.
"""
import pytest
from src.service.app import app


@pytest.fixture
def client():
    """Create a test client for the app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint_returns_200(client):
    """Test that /health returns 200 status code."""
    response = client.get('/health')
    assert response.status_code == 200


def test_health_endpoint_returns_json(client):
    """Test that /health returns JSON content."""
    response = client.get('/health')
    assert response.content_type == 'application/json'


def test_health_endpoint_has_status_ok(client):
    """Test that /health returns status:ok."""
    response = client.get('/health')
    data = response.get_json()
    assert data['status'] == 'ok'


def test_health_endpoint_has_timestamp(client):
    """Test that /health includes a timestamp."""
    response = client.get('/health')
    data = response.get_json()
    assert 'timestamp' in data
    assert data['timestamp'].endswith('Z')  # ISO 8601 UTC format


def test_health_endpoint_multiple_calls(client):
    """Test that /health can be called multiple times successfully."""
    for _ in range(5):
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
