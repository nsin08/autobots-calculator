"""
Tests for calculation history endpoints.
"""
import pytest
from datetime import datetime
from src.service.models import User, CalculationHistory
from src.service.database import db


def test_get_history_unauthenticated(client):
    """Test that unauthenticated users cannot access history."""
    response = client.get('/api/history')
    assert response.status_code == 401


def test_save_calculation_unauthenticated(client):
    """Test that unauthenticated users cannot save calculations."""
    response = client.post('/api/history', json={
        'calculation_type': 'basic',
        'expression': '5 + 3',
        'result': '8'
    })
    assert response.status_code == 401


def test_clear_history_unauthenticated(client):
    """Test that unauthenticated users cannot clear history."""
    response = client.delete('/api/history')
    assert response.status_code == 401


def test_save_calculation_success(auth_client):
    """Test saving a calculation to history."""
    response = auth_client.post('/api/history', json={
        'calculation_type': 'basic',
        'expression': '5 + 3',
        'result': '8'
    })
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['success'] is True
    assert 'id' in data
    
    # Verify in database
    calc = CalculationHistory.query.get(data['id'])
    assert calc is not None
    assert calc.expression == '5 + 3'
    assert calc.result == '8'
    assert calc.calculation_type == 'basic'


def test_save_calculation_missing_fields(auth_client):
    """Test that missing required fields return error."""
    # Missing calculation_type
    response = auth_client.post('/api/history', json={
        'expression': '5 + 3',
        'result': '8'
    })
    assert response.status_code == 400
    assert 'calculation_type' in response.get_json()['error']
    
    # Missing expression
    response = auth_client.post('/api/history', json={
        'calculation_type': 'basic',
        'result': '8'
    })
    assert response.status_code == 400
    assert 'expression' in response.get_json()['error']
    
    # Missing result
    response = auth_client.post('/api/history', json={
        'calculation_type': 'basic',
        'expression': '5 + 3'
    })
    assert response.status_code == 400
    assert 'result' in response.get_json()['error']


def test_save_calculation_invalid_type(auth_client):
    """Test that invalid calculation type returns error."""
    response = auth_client.post('/api/history', json={
        'calculation_type': 'invalid',
        'expression': '5 + 3',
        'result': '8'
    })
    
    assert response.status_code == 400
    assert 'Invalid calculation_type' in response.get_json()['error']


def test_save_calculation_too_long(auth_client):
    """Test that overly long expressions/results return error."""
    # Expression too long
    response = auth_client.post('/api/history', json={
        'calculation_type': 'basic',
        'expression': 'a' * 501,
        'result': '8'
    })
    assert response.status_code == 400
    assert 'too long' in response.get_json()['error']
    
    # Result too long
    response = auth_client.post('/api/history', json={
        'calculation_type': 'basic',
        'expression': '5 + 3',
        'result': 'x' * 101
    })
    assert response.status_code == 400
    assert 'too long' in response.get_json()['error']


def test_get_history_empty(auth_client):
    """Test getting history when no calculations exist."""
    response = auth_client.get('/api/history')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['calculations'] == []
    assert data['total'] == 0
    assert data['page'] == 1


def test_get_history_with_calculations(auth_client, test_user):
    """Test getting history with existing calculations."""
    # Add some calculations
    calc1 = CalculationHistory(
        user_id=test_user.id,
        calculation_type='basic',
        expression='5 + 3',
        result='8'
    )
    calc2 = CalculationHistory(
        user_id=test_user.id,
        calculation_type='scientific',
        expression='sqrt(16)',
        result='4'
    )
    db.session.add(calc1)
    db.session.add(calc2)
    db.session.commit()
    
    response = auth_client.get('/api/history')
    
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['calculations']) == 2
    assert data['total'] == 2
    
    # Check that most recent is first (descending order)
    assert data['calculations'][0]['expression'] == 'sqrt(16)'
    assert data['calculations'][1]['expression'] == '5 + 3'


def test_get_history_pagination(auth_client, test_user):
    """Test pagination of history results."""
    # Add 5 calculations
    for i in range(5):
        calc = CalculationHistory(
            user_id=test_user.id,
            calculation_type='basic',
            expression=f'{i} + 1',
            result=str(i + 1)
        )
        db.session.add(calc)
    db.session.commit()
    
    # Get first page with limit 2
    response = auth_client.get('/api/history?limit=2&page=1')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['calculations']) == 2
    assert data['total'] == 5
    assert data['per_page'] == 2
    assert data['page'] == 1
    
    # Get second page
    response = auth_client.get('/api/history?limit=2&page=2')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['calculations']) == 2
    assert data['page'] == 2
    
    # Get third page (only 1 result)
    response = auth_client.get('/api/history?limit=2&page=3')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['calculations']) == 1


def test_get_history_limit_validation(auth_client):
    """Test that limit parameter is validated."""
    # Limit too small
    response = auth_client.get('/api/history?limit=0')
    assert response.status_code == 400
    
    # Limit too large
    response = auth_client.get('/api/history?limit=101')
    assert response.status_code == 400
    
    # Negative page
    response = auth_client.get('/api/history?page=0')
    assert response.status_code == 400


def test_get_history_user_isolation(auth_client, test_user):
    """Test that users only see their own history."""
    # Create another user with calculations
    other_user = User(username='otheruser', email='other@example.com')
    other_user.set_password('password123')
    db.session.add(other_user)
    db.session.commit()
    
    # Add calculation for other user
    other_calc = CalculationHistory(
        user_id=other_user.id,
        calculation_type='basic',
        expression='100 + 200',
        result='300'
    )
    db.session.add(other_calc)
    
    # Add calculation for test user
    user_calc = CalculationHistory(
        user_id=test_user.id,
        calculation_type='basic',
        expression='5 + 3',
        result='8'
    )
    db.session.add(user_calc)
    db.session.commit()
    
    # Get history as test_user
    response = auth_client.get('/api/history')
    
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['calculations']) == 1
    assert data['calculations'][0]['expression'] == '5 + 3'


def test_clear_history_success(auth_client, test_user):
    """Test clearing all history."""
    # Add some calculations
    for i in range(3):
        calc = CalculationHistory(
            user_id=test_user.id,
            calculation_type='basic',
            expression=f'{i} + {i}',
            result=str(i * 2)
        )
        db.session.add(calc)
    db.session.commit()
    
    # Clear history
    response = auth_client.delete('/api/history')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['deleted_count'] == 3
    
    # Verify history is empty
    response = auth_client.get('/api/history')
    data = response.get_json()
    assert len(data['calculations']) == 0


def test_clear_history_user_isolation(auth_client, test_user):
    """Test that clearing history only affects current user."""
    # Create another user
    other_user = User(username='otheruser', email='other@example.com')
    other_user.set_password('password123')
    db.session.add(other_user)
    db.session.commit()
    
    # Add calculations for both users
    for i in range(2):
        calc = CalculationHistory(
            user_id=test_user.id,
            calculation_type='basic',
            expression=f'{i} + 1',
            result=str(i + 1)
        )
        db.session.add(calc)
        
        other_calc = CalculationHistory(
            user_id=other_user.id,
            calculation_type='basic',
            expression=f'{i} * 2',
            result=str(i * 2)
        )
        db.session.add(other_calc)
    
    db.session.commit()
    
    # Clear history as test_user
    response = auth_client.delete('/api/history')
    assert response.status_code == 200
    data = response.get_json()
    assert data['deleted_count'] == 2
    
    # Verify other user's history is intact
    other_calcs = CalculationHistory.query.filter_by(user_id=other_user.id).all()
    assert len(other_calcs) == 2


def test_calculation_to_dict(test_user):
    """Test the to_dict method of CalculationHistory."""
    calc = CalculationHistory(
        user_id=test_user.id,
        calculation_type='scientific',
        expression='sin(30)',
        result='0.5'
    )
    db.session.add(calc)
    db.session.commit()
    
    dict_data = calc.to_dict()
    
    assert dict_data['id'] == calc.id
    assert dict_data['calculation_type'] == 'scientific'
    assert dict_data['expression'] == 'sin(30)'
    assert dict_data['result'] == '0.5'
    assert 'timestamp' in dict_data
    assert dict_data['timestamp'].endswith('Z')
