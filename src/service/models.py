"""
Database models for calculator application.
"""
from datetime import datetime
import bcrypt
from flask_login import UserMixin
from src.service.database import db


class User(db.Model, UserMixin):
    """
    User model for authentication and history tracking.
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        """
        Hash and set user password.
        
        Args:
            password (str): Plain text password
        """
        self.password_hash = bcrypt.hashpw(
            password.encode('utf-8'), 
            bcrypt.gensalt()
        ).decode('utf-8')
    
    def check_password(self, password):
        """
        Verify password against stored hash.
        
        Args:
            password (str): Plain text password to verify
            
        Returns:
            bool: True if password matches, False otherwise
        """
        return bcrypt.checkpw(
            password.encode('utf-8'), 
            self.password_hash.encode('utf-8')
        )
    
    def __repr__(self):
        return f'<User {self.username}>'


class CalculationHistory(db.Model):
    """
    Calculation history for user's past calculations.
    """
    __tablename__ = 'calculation_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    calculation_type = db.Column(db.String(20), nullable=False)  # 'basic', 'scientific', 'emi', 'simple_interest', 'compound_interest'
    expression = db.Column(db.String(500), nullable=False)  # e.g., "5 + 3", "sqrt(16)", "EMI(100000, 7.5, 60)"
    result = db.Column(db.String(100), nullable=False)  # String to handle large numbers and special results
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('calculations', lazy='dynamic'))
    
    def to_dict(self):
        """Serialize for API responses."""
        return {
            'id': self.id,
            'calculation_type': self.calculation_type,
            'expression': self.expression,
            'result': self.result,
            'timestamp': self.timestamp.isoformat() + 'Z'
        }
    
    def __repr__(self):
        return f'<CalculationHistory {self.id}: {self.expression} = {self.result}>'
