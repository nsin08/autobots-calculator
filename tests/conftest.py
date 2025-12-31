"""
Pytest configuration and fixtures.
"""
import pytest
from src.service.app import app as flask_app
from src.service.database import db as _db
from src.service.models import User


@pytest.fixture(scope='function')
def app():
    """
    Create Flask app configured for testing with in-memory database.
    """
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with flask_app.app_context():
        _db.create_all()
        yield flask_app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope='function')
def db(app):
    """
    Provide database instance for tests.
    """
    return _db


@pytest.fixture(scope='function')
def client(app):
    """
    Create test client.
    """
    return app.test_client()


@pytest.fixture(scope='function')
def test_user(db):
    """
    Create a test user for authentication tests.
    """
    user = User(
        username='testuser',
        email='test@example.com'
    )
    user.set_password('TestPassword123')
    db.session.add(user)
    db.session.commit()
    return user
