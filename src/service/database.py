"""
Database initialization and configuration.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    """
    Initialize database with Flask app.
    
    Args:
        app: Flask application instance
    """
    # SQLite configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config.get(
        'SQLALCHEMY_DATABASE_URI', 
        'sqlite:///calculator.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize SQLAlchemy with app
    db.init_app(app)
    
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
