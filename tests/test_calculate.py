"""
Tests for calculate endpoint.
"""
import pytest
from src.service.app import app


@pytest.fixture
def client():
    """Create test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_calculate_addition(client):
    """Test addition operation."""
    response = client.post('/api/calculate', json={
        'operation': 'add',
        'a': 2,
        'b': 3
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['result'] == 5


def test_calculate_subtraction(client):
    """Test subtraction operation."""
    response = client.post('/api/calculate', json={
        'operation': 'subtract',
        'a': 5,
        'b': 3
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['result'] == 2


def test_calculate_multiplication(client):
    """Test multiplication operation."""
    response = client.post('/api/calculate', json={
        'operation': 'multiply',
        'a': 4,
        'b': 3
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['result'] == 12


def test_calculate_division(client):
    """Test division operation."""
    response = client.post('/api/calculate', json={
        'operation': 'divide',
        'a': 10,
        'b': 2
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['result'] == 5


def test_calculate_invalid_operation(client):
    """Test invalid operation returns 400."""
    response = client.post('/api/calculate', json={
        'operation': 'power',
        'a': 2,
        'b': 3
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Invalid operation'


def test_calculate_division_by_zero(client):
    """Test division by zero returns 400."""
    response = client.post('/api/calculate', json={
        'operation': 'divide',
        'a': 10,
        'b': 0
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Division by zero'


def test_calculate_missing_operands(client):
    """Test missing operands returns 400."""
    response = client.post('/api/calculate', json={
        'operation': 'add',
        'a': 5
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


def test_calculate_invalid_operands(client):
    """Test invalid operands returns 400."""
    response = client.post('/api/calculate', json={
        'operation': 'add',
        'a': 'not a number',
        'b': 3
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


def test_calculate_float_operations(client):
    """Test operations with float numbers."""
    response = client.post('/api/calculate', json={
        'operation': 'add',
        'a': 2.5,
        'b': 3.7
    })
    assert response.status_code == 200
    data = response.get_json()
    assert abs(data['result'] - 6.2) < 0.0001
