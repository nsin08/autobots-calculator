"""
Tests for User model and database operations.
"""
import pytest
from datetime import datetime
from src.service.models import User
from src.service.database import db


def test_user_creation(app, db):
    """Test creating a new user."""
    user = User(
        username='john_doe',
        email='john@example.com'
    )
    user.set_password('SecurePassword123')
    
    db.session.add(user)
    db.session.commit()
    
    # Verify user was created
    assert user.id is not None
    assert user.username == 'john_doe'
    assert user.email == 'john@example.com'
    assert user.password_hash is not None
    assert user.created_at is not None
    assert isinstance(user.created_at, datetime)
    assert user.last_login is None


def test_password_hashing(app, db):
    """Test password is hashed and not stored in plain text."""
    user = User(username='testuser', email='test@example.com')
    password = 'MySecretPassword'
    user.set_password(password)
    
    # Password should be hashed
    assert user.password_hash != password
    assert len(user.password_hash) > 50  # bcrypt hashes are long


def test_password_verification_success(app, db):
    """Test correct password verification."""
    user = User(username='testuser', email='test@example.com')
    password = 'CorrectPassword123'
    user.set_password(password)
    
    # Correct password should verify
    assert user.check_password(password) is True


def test_password_verification_failure(app, db):
    """Test incorrect password verification."""
    user = User(username='testuser', email='test@example.com')
    user.set_password('CorrectPassword123')
    
    # Wrong password should not verify
    assert user.check_password('WrongPassword') is False


def test_username_uniqueness(app, db):
    """Test username must be unique."""
    user1 = User(username='john_doe', email='john1@example.com')
    user1.set_password('password1')
    db.session.add(user1)
    db.session.commit()
    
    # Try to create another user with same username
    user2 = User(username='john_doe', email='john2@example.com')
    user2.set_password('password2')
    db.session.add(user2)
    
    with pytest.raises(Exception):  # Should raise IntegrityError
        db.session.commit()


def test_email_uniqueness(app, db):
    """Test email must be unique."""
    user1 = User(username='john_doe', email='same@example.com')
    user1.set_password('password1')
    db.session.add(user1)
    db.session.commit()
    
    # Try to create another user with same email
    user2 = User(username='jane_doe', email='same@example.com')
    user2.set_password('password2')
    db.session.add(user2)
    
    with pytest.raises(Exception):  # Should raise IntegrityError
        db.session.commit()


def test_user_query_by_username(app, db):
    """Test querying user by username."""
    user = User(username='findme', email='findme@example.com')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    
    # Query by username
    found_user = User.query.filter_by(username='findme').first()
    assert found_user is not None
    assert found_user.username == 'findme'
    assert found_user.email == 'findme@example.com'


def test_user_query_by_email(app, db):
    """Test querying user by email."""
    user = User(username='emailtest', email='query@example.com')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    
    # Query by email
    found_user = User.query.filter_by(email='query@example.com').first()
    assert found_user is not None
    assert found_user.username == 'emailtest'


def test_user_update_last_login(app, db):
    """Test updating user's last login timestamp."""
    user = User(username='logintest', email='login@example.com')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    # Verify update
    updated_user = User.query.filter_by(username='logintest').first()
    assert updated_user.last_login is not None
    assert isinstance(updated_user.last_login, datetime)


def test_user_repr(app, db):
    """Test user string representation."""
    user = User(username='reprtest', email='repr@example.com')
    assert repr(user) == '<User reprtest>'


def test_database_session_management(app, db):
    """Test database session creates and tears down properly."""
    # Create user
    user = User(username='sessiontest', email='session@example.com')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    
    # Verify user exists
    assert User.query.count() == 1
    
    # Session should be clean for next test
    # (handled by conftest.py fixture teardown)


def test_user_flask_login_integration(app, db):
    """Test User model works with Flask-Login (UserMixin)."""
    user = User(username='loginuser', email='login@example.com')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    
    # UserMixin provides these methods
    assert hasattr(user, 'is_authenticated')
    assert hasattr(user, 'is_active')
    assert hasattr(user, 'is_anonymous')
    assert hasattr(user, 'get_id')
    
    # User should be authenticated and active
    assert user.is_authenticated is True
    assert user.is_active is True
    assert user.is_anonymous is False
    assert user.get_id() == str(user.id)
