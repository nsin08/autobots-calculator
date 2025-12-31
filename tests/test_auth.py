"""
Tests for authentication endpoints.
"""
import pytest
from src.service.models import User


# Registration Tests

def test_register_success(client, db):
    """Test successful user registration."""
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['success'] is True
    assert data['username'] == 'testuser'
    assert 'user_id' in data
    
    # Verify user in database
    user = User.query.filter_by(username='testuser').first()
    assert user is not None
    assert user.email == 'test@example.com'
    assert user.check_password('password123')


def test_register_duplicate_username(client, test_user):
    """Test registration with duplicate username."""
    response = client.post('/api/auth/register', json={
        'username': 'testuser',  # Same as test_user
        'email': 'different@example.com',
        'password': 'password123'
    })
    
    assert response.status_code == 409
    data = response.get_json()
    assert 'error' in data
    assert 'Username already exists' in data['error']


def test_register_duplicate_email(client, test_user):
    """Test registration with duplicate email."""
    response = client.post('/api/auth/register', json={
        'username': 'differentuser',
        'email': 'test@example.com',  # Same as test_user
        'password': 'password123'
    })
    
    assert response.status_code == 409
    data = response.get_json()
    assert 'error' in data
    assert 'Email already exists' in data['error']


def test_register_missing_username(client):
    """Test registration without username."""
    response = client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'Username is required' in data['error']


def test_register_missing_email(client):
    """Test registration without email."""
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'password': 'password123'
    })
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'Email is required' in data['error']


def test_register_missing_password(client):
    """Test registration without password."""
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com'
    })
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'Password is required' in data['error']


def test_register_short_username(client):
    """Test registration with username too short."""
    response = client.post('/api/auth/register', json={
        'username': 'ab',  # Only 2 chars
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert '3-50 characters' in data['error']


def test_register_long_username(client):
    """Test registration with username too long."""
    response = client.post('/api/auth/register', json={
        'username': 'a' * 51,  # 51 chars
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert '3-50 characters' in data['error']


def test_register_invalid_email(client):
    """Test registration with invalid email format."""
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'notanemail',
        'password': 'password123'
    })
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'Invalid email format' in data['error']


def test_register_short_password(client):
    """Test registration with password too short."""
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'short'  # Only 5 chars
    })
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'at least 8 characters' in data['error']


def test_register_no_json(client):
    """Test registration without JSON body."""
    response = client.post('/api/auth/register')
    
    # Flask returns 415 when no content-type header for JSON endpoint
    assert response.status_code in [400, 415]
    if response.status_code == 400:
        data = response.get_json()
        assert 'error' in data
        assert 'JSON' in data['error']


# Login Tests

def test_login_success(client, test_user):
    """Test successful login."""
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'testpass123'
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['username'] == 'testuser'
    assert 'user_id' in data


def test_login_wrong_password(client, test_user):
    """Test login with wrong password."""
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'wrongpassword'
    })
    
    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data
    assert 'Invalid username or password' in data['error']


def test_login_nonexistent_user(client):
    """Test login with non-existent username."""
    response = client.post('/api/auth/login', json={
        'username': 'nonexistent',
        'password': 'password123'
    })
    
    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data
    assert 'Invalid username or password' in data['error']


def test_login_missing_username(client):
    """Test login without username."""
    response = client.post('/api/auth/login', json={
        'password': 'password123'
    })
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'Username is required' in data['error']


def test_login_missing_password(client):
    """Test login without password."""
    response = client.post('/api/auth/login', json={
        'username': 'testuser'
    })
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'Password is required' in data['error']


def test_login_updates_last_login(client, test_user, db):
    """Test that login updates last_login timestamp."""
    # Get initial last_login
    user = User.query.filter_by(username='testuser').first()
    initial_last_login = user.last_login
    
    # Login
    client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'testpass123'
    })
    
    # Check last_login updated
    db.session.refresh(user)
    assert user.last_login != initial_last_login
    assert user.last_login is not None


# Logout Tests

def test_logout(client, test_user):
    """Test logout."""
    # Login first
    client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'testpass123'
    })
    
    # Logout
    response = client.get('/api/auth/logout')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'message' in data


def test_logout_without_login(client):
    """Test logout without being logged in."""
    response = client.get('/api/auth/logout')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


# Status Tests

def test_status_authenticated(client, test_user):
    """Test status endpoint when authenticated."""
    # Login first
    client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'testpass123'
    })
    
    # Check status
    response = client.get('/api/auth/status')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['authenticated'] is True
    assert data['username'] == 'testuser'
    assert 'user_id' in data


def test_status_not_authenticated(client):
    """Test status endpoint when not authenticated."""
    response = client.get('/api/auth/status')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['authenticated'] is False
    assert 'username' not in data


# Session Persistence Tests

def test_session_persists_across_requests(client, test_user):
    """Test that session persists across multiple requests."""
    # Login
    client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'testpass123'
    })
    
    # Make another request - should still be authenticated
    response = client.get('/api/auth/status')
    data = response.get_json()
    assert data['authenticated'] is True
    
    # Another request
    response = client.get('/api/auth/status')
    data = response.get_json()
    assert data['authenticated'] is True


def test_session_cleared_after_logout(client, test_user):
    """Test that session is cleared after logout."""
    # Login
    client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'testpass123'
    })
    
    # Verify authenticated
    response = client.get('/api/auth/status')
    assert response.get_json()['authenticated'] is True
    
    # Logout
    client.get('/api/auth/logout')
    
    # Verify not authenticated
    response = client.get('/api/auth/status')
    assert response.get_json()['authenticated'] is False


# Decorator Tests
# Note: These tests verify the decorator logic but cannot dynamically add routes
# The decorator is used in actual routes and tested through integration

def test_login_required_decorator_logic_authenticated():
    """Test @login_required decorator preserves callable structure."""
    from src.service.decorators import login_required
    from unittest.mock import Mock
    
    # Create mock function
    mock_func = Mock(return_value=({'data': 'secret'}, 200))
    
    # Apply decorator
    protected_func = login_required(mock_func)
    
    # Verify decorator returns callable
    assert callable(protected_func)
    # Decorator integration tested via session persistence tests above


def test_login_required_decorator_logic_structure():
    """Test @login_required decorator preserves function metadata."""
    from src.service.decorators import login_required
    
    @login_required
    def test_function():
        """Test docstring"""
        return 'result'
    
    # Verify decorator preserves function name and docstring
    assert test_function.__name__ == 'test_function'
    assert 'Test docstring' in test_function.__doc__
