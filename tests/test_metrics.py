"""
Tests for /metrics endpoint.
"""
import pytest
import time
from src.service.app import app


@pytest.fixture
def client():
    """Create a test client for the app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_metrics_endpoint_returns_200(client):
    """Test that /metrics returns 200 status code."""
    response = client.get('/metrics')
    assert response.status_code == 200


def test_metrics_endpoint_returns_json(client):
    """Test that /metrics returns JSON content."""
    response = client.get('/metrics')
    assert response.content_type == 'application/json'


def test_metrics_endpoint_has_required_fields(client):
    """Test that /metrics includes required fields."""
    response = client.get('/metrics')
    data = response.get_json()
    assert 'requests_total' in data
    assert 'uptime_seconds' in data


def test_metrics_endpoint_request_count_increments(client):
    """Test that request counter increments."""
    # Make first request
    response1 = client.get('/metrics')
    count1 = response1.get_json()['requests_total']
    
    # Make second request
    response2 = client.get('/metrics')
    count2 = response2.get_json()['requests_total']
    
    # Count should increment (by at least 1, accounting for the metrics call itself)
    assert count2 > count1


def test_metrics_endpoint_uptime_is_positive(client):
    """Test that uptime is a positive number."""
    response = client.get('/metrics')
    data = response.get_json()
    assert data['uptime_seconds'] >= 0
    assert isinstance(data['uptime_seconds'], int)


def test_metrics_endpoint_uptime_increases(client):
    """Test that uptime increases over time."""
    response1 = client.get('/metrics')
    uptime1 = response1.get_json()['uptime_seconds']
    
    time.sleep(1)
    
    response2 = client.get('/metrics')
    uptime2 = response2.get_json()['uptime_seconds']
    
    assert uptime2 >= uptime1
