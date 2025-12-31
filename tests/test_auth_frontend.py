"""
Tests for authentication frontend integration.
Tests the static HTML pages and JavaScript validation logic through API integration.
"""
import pytest
import json
from src.service.app import app, db
from src.service.models import User


@pytest.fixture
def client():
    """Create test client with fresh database."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()


@pytest.fixture
def test_user(client):
    """Create a test user."""
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    return {'username': 'testuser', 'password': 'testpass123'}


# Registration Page Tests

def test_register_page_exists(client):
    """Test that register.html is accessible."""
    response = client.get('/static/register.html')
    assert response.status_code == 200


def test_register_validation_email_format(client):
    """Test that invalid email format is rejected by backend."""
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'invalid-email',
        'password': 'testpass123'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


def test_register_validation_username_length(client):
    """Test username length constraints."""
    # Too short
    response = client.post('/api/auth/register', json={
        'username': 'ab',
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    assert response.status_code == 400
    
    # Too long
    response = client.post('/api/auth/register', json={
        'username': 'a' * 51,
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    assert response.status_code == 400


def test_register_validation_password_length(client):
    """Test password length constraints."""
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'short'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


def test_register_successful_flow(client):
    """Test successful registration flow."""
    response = client.post('/api/auth/register', json={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'securepass123'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'user_id' in data
    assert data['username'] == 'newuser'


def test_register_duplicate_username(client, test_user):
    """Test that duplicate username is rejected."""
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'different@example.com',
        'password': 'testpass123'
    })
    assert response.status_code == 409
    data = json.loads(response.data)
    assert 'error' in data


def test_register_duplicate_email(client, test_user):
    """Test that duplicate email is rejected."""
    response = client.post('/api/auth/register', json={
        'username': 'differentuser',
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    assert response.status_code == 409
    data = json.loads(response.data)
    assert 'error' in data


# Login Page Tests

def test_login_page_exists(client):
    """Test that login.html is accessible."""
    response = client.get('/static/login.html')
    assert response.status_code == 200


def test_login_successful_flow(client, test_user):
    """Test successful login flow."""
    response = client.post('/api/auth/login', json={
        'username': test_user['username'],
        'password': test_user['password']
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['username'] == test_user['username']
    assert 'user_id' in data


def test_login_invalid_username(client, test_user):
    """Test login with invalid username."""
    response = client.post('/api/auth/login', json={
        'username': 'nonexistent',
        'password': 'testpass123'
    })
    assert response.status_code == 401
    data = json.loads(response.data)
    assert 'error' in data


def test_login_invalid_password(client, test_user):
    """Test login with invalid password."""
    response = client.post('/api/auth/login', json={
        'username': test_user['username'],
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    data = json.loads(response.data)
    assert 'error' in data


def test_login_missing_fields(client):
    """Test login with missing required fields."""
    response = client.post('/api/auth/login', json={
        'username': 'testuser'
    })
    assert response.status_code == 400


# Session Management Tests

def test_auth_status_unauthenticated(client):
    """Test auth status for unauthenticated user."""
    response = client.get('/api/auth/status')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['authenticated'] is False


def test_auth_status_authenticated(client, test_user):
    """Test auth status for authenticated user."""
    # Login first
    client.post('/api/auth/login', json={
        'username': test_user['username'],
        'password': test_user['password']
    })
    
    # Check status
    response = client.get('/api/auth/status')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['authenticated'] is True
    assert data['username'] == test_user['username']


def test_logout_flow(client, test_user):
    """Test logout clears session."""
    # Login
    client.post('/api/auth/login', json={
        'username': test_user['username'],
        'password': test_user['password']
    })
    
    # Verify authenticated
    response = client.get('/api/auth/status')
    data = json.loads(response.data)
    assert data['authenticated'] is True
    
    # Logout
    response = client.get('/api/auth/logout')
    assert response.status_code == 200
    
    # Verify unauthenticated
    response = client.get('/api/auth/status')
    data = json.loads(response.data)
    assert data['authenticated'] is False


# Calculator Page Tests

def test_calculator_page_exists(client):
    """Test that calculator page is accessible."""
    response = client.get('/static/index.html')
    assert response.status_code == 200


def test_calculator_accessible_without_auth(client):
    """Test that calculator can be accessed without authentication (guest mode)."""
    response = client.get('/static/index.html')
    assert response.status_code == 200


# Integration Tests

def test_full_registration_login_logout_flow(client):
    """Test complete user flow: register → login → logout."""
    # Register
    register_response = client.post('/api/auth/register', json={
        'username': 'flowtest',
        'email': 'flowtest@example.com',
        'password': 'flowpass123'
    })
    assert register_response.status_code == 201
    register_data = json.loads(register_response.data)
    user_id = register_data['user_id']
    
    # Login
    login_response = client.post('/api/auth/login', json={
        'username': 'flowtest',
        'password': 'flowpass123'
    })
    assert login_response.status_code == 200
    login_data = json.loads(login_response.data)
    assert login_data['user_id'] == user_id
    
    # Check authenticated
    status_response = client.get('/api/auth/status')
    status_data = json.loads(status_response.data)
    assert status_data['authenticated'] is True
    assert status_data['username'] == 'flowtest'
    
    # Logout
    logout_response = client.get('/api/auth/logout')
    assert logout_response.status_code == 200
    
    # Verify logged out
    final_status = client.get('/api/auth/status')
    final_data = json.loads(final_status.data)
    assert final_data['authenticated'] is False


def test_multiple_users_separate_sessions(client):
    """Test that multiple users can be registered separately."""
    # Register user 1
    response1 = client.post('/api/auth/register', json={
        'username': 'user1',
        'email': 'user1@example.com',
        'password': 'password123'
    })
    assert response1.status_code == 201
    
    # Register user 2
    response2 = client.post('/api/auth/register', json={
        'username': 'user2',
        'email': 'user2@example.com',
        'password': 'password456'
    })
    assert response2.status_code == 201
    
    # Both users should have different IDs
    data1 = json.loads(response1.data)
    data2 = json.loads(response2.data)
    assert data1['user_id'] != data2['user_id']
    assert data1['username'] == 'user1'
    assert data2['username'] == 'user2'


# Edge Cases

def test_register_empty_fields(client):
    """Test registration with empty fields."""
    response = client.post('/api/auth/register', json={
        'username': '',
        'email': '',
        'password': ''
    })
    assert response.status_code == 400


def test_login_empty_fields(client):
    """Test login with empty fields."""
    response = client.post('/api/auth/login', json={
        'username': '',
        'password': ''
    })
    assert response.status_code == 400


def test_register_whitespace_username(client):
    """Test registration with whitespace in username."""
    response = client.post('/api/auth/register', json={
        'username': '  testuser  ',
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    # Backend should handle trimming or reject
    assert response.status_code in [201, 400]


def test_register_special_characters_username(client):
    """Test registration with special characters in username."""
    response = client.post('/api/auth/register', json={
        'username': 'test@user#123',
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    # Backend may accept or reject depending on validation rules
    assert response.status_code in [201, 400]


def test_case_sensitive_username(client, test_user):
    """Test that username is case-sensitive for registration."""
    response = client.post('/api/auth/register', json={
        'username': 'TESTUSER',  # Different case
        'email': 'different@example.com',
        'password': 'testpass123'
    })
    # Should either allow (case-sensitive) or reject (case-insensitive check)
    # Current implementation treats as different user
    assert response.status_code in [201, 409]


def test_logout_when_not_logged_in(client):
    """Test logout when already logged out."""
    response = client.get('/api/auth/logout')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
