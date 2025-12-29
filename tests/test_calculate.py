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
        'operation': 'invalid',
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


# Factorial tests
def test_calculate_factorial_valid(client):
    """Test factorial with valid input."""
    response = client.post('/api/calculate', json={
        'operation': 'factorial',
        'a': 5
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['result'] == 120


def test_calculate_factorial_zero(client):
    """Test factorial of zero equals 1."""
    response = client.post('/api/calculate', json={
        'operation': 'factorial',
        'a': 0
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['result'] == 1


def test_calculate_factorial_negative(client):
    """Test factorial with negative number returns 400."""
    response = client.post('/api/calculate', json={
        'operation': 'factorial',
        'a': -5
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Factorial not defined for negative numbers'


def test_calculate_factorial_too_large(client):
    """Test factorial with number > 20 returns 400."""
    response = client.post('/api/calculate', json={
        'operation': 'factorial',
        'a': 21
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Factorial input too large (max 20)'


def test_calculate_factorial_non_integer(client):
    """Test factorial with non-integer returns 400."""
    response = client.post('/api/calculate', json={
        'operation': 'factorial',
        'a': 5.5
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Factorial requires integer input'


# Power tests
def test_calculate_power_basic(client):
    """Test power operation with basic inputs."""
    response = client.post('/api/calculate', json={
        'operation': 'power',
        'a': 2,
        'b': 3
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['result'] == 8


def test_calculate_power_negative_exponent(client):
    """Test power with negative exponent."""
    response = client.post('/api/calculate', json={
        'operation': 'power',
        'a': 2,
        'b': -2
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['result'] == 0.25


def test_calculate_power_large_exponent(client):
    """Test power with exponent out of bounds returns 400."""
    response = client.post('/api/calculate', json={
        'operation': 'power',
        'a': 2,
        'b': 101
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Exponent out of bounds (-100 to 100)'


# Modulo tests
def test_calculate_modulo_basic(client):
    """Test modulo operation with basic inputs."""
    response = client.post('/api/calculate', json={
        'operation': 'modulo',
        'a': 10,
        'b': 3
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['result'] == 1


def test_calculate_modulo_zero_divisor(client):
    """Test modulo with zero divisor returns 400."""
    response = client.post('/api/calculate', json={
        'operation': 'modulo',
        'a': 10,
        'b': 0
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Division by zero'
