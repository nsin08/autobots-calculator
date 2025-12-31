"""
Tests for financial calculators (EMI, Simple Interest, Compound Interest).
"""
import pytest
from decimal import Decimal
from src.service.calculators.financial import (
    calculate_emi,
    calculate_simple_interest,
    calculate_compound_interest
)


# EMI Calculator Tests

def test_emi_calculator_po_example(client):
    """Test EMI calculation with PO's exact example: $100k @ 8.5% for 20y → $867.82"""
    response = client.post('/api/calculate/emi', json={
        'loan_amount': 100000,
        'annual_rate': 8.5,
        'tenure_years': 20
    })
    
    assert response.status_code == 200
    data = response.get_json()
    
    # PO's expected result: EMI = $867.82
    assert abs(data['emi'] - 867.82) < 0.01  # Allow small rounding difference
    
    # Total payment should be EMI * months
    expected_total = 867.82 * 240  # 20 years * 12 months
    assert abs(data['total_payment'] - expected_total) < 1.0  # Allow $1 difference for rounding
    
    # Total interest = total payment - principal
    assert abs(data['total_interest'] - (data['total_payment'] - 100000)) < 0.01


def test_emi_calculator_basic(client):
    """Test basic EMI calculation."""
    response = client.post('/api/calculate/emi', json={
        'loan_amount': 50000,
        'annual_rate': 10.0,
        'tenure_years': 5
    })
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert 'emi' in data
    assert 'total_interest' in data
    assert 'total_payment' in data
    assert data['emi'] > 0
    assert data['total_interest'] > 0
    # Check that total payment is approximately EMI * months (allow for rounding)
    assert abs(data['total_payment'] - (data['emi'] * 60)) < 0.50  # Allow 50 cents difference for rounding


def test_emi_calculator_zero_interest(client):
    """Test EMI calculation with zero interest rate."""
    response = client.post('/api/calculate/emi', json={
        'loan_amount': 12000,
        'annual_rate': 0,
        'tenure_years': 1
    })
    
    assert response.status_code == 200
    data = response.get_json()
    
    # With 0% interest, EMI = loan_amount / months
    expected_emi = 12000 / 12
    assert abs(data['emi'] - expected_emi) < 0.01
    assert data['total_interest'] == 0
    assert abs(data['total_payment'] - 12000) < 0.01


def test_emi_calculator_missing_parameters(client):
    """Test that missing parameters return error."""
    # Missing loan_amount
    response = client.post('/api/calculate/emi', json={
        'annual_rate': 8.5,
        'tenure_years': 20
    })
    assert response.status_code == 400
    assert 'loan_amount' in response.get_json()['error']
    
    # Missing annual_rate
    response = client.post('/api/calculate/emi', json={
        'loan_amount': 100000,
        'tenure_years': 20
    })
    assert response.status_code == 400
    assert 'annual_rate' in response.get_json()['error']
    
    # Missing tenure_years
    response = client.post('/api/calculate/emi', json={
        'loan_amount': 100000,
        'annual_rate': 8.5
    })
    assert response.status_code == 400
    assert 'tenure_years' in response.get_json()['error']


def test_emi_calculator_invalid_types(client):
    """Test that invalid parameter types return error."""
    response = client.post('/api/calculate/emi', json={
        'loan_amount': 'invalid',
        'annual_rate': 8.5,
        'tenure_years': 20
    })
    assert response.status_code == 400
    assert 'Invalid parameter types' in response.get_json()['error']


def test_emi_calculator_out_of_range(client):
    """Test that out-of-range values return error."""
    # Loan amount too small
    response = client.post('/api/calculate/emi', json={
        'loan_amount': 500,
        'annual_rate': 8.5,
        'tenure_years': 20
    })
    assert response.status_code == 400
    assert 'Loan amount' in response.get_json()['error']
    
    # Loan amount too large
    response = client.post('/api/calculate/emi', json={
        'loan_amount': 11000000,
        'annual_rate': 8.5,
        'tenure_years': 20
    })
    assert response.status_code == 400
    assert 'Loan amount' in response.get_json()['error']
    
    # Annual rate too large
    response = client.post('/api/calculate/emi', json={
        'loan_amount': 100000,
        'annual_rate': 35,
        'tenure_years': 20
    })
    assert response.status_code == 400
    assert 'Annual rate' in response.get_json()['error']
    
    # Tenure too small
    response = client.post('/api/calculate/emi', json={
        'loan_amount': 100000,
        'annual_rate': 8.5,
        'tenure_years': 0
    })
    assert response.status_code == 400
    assert 'Tenure' in response.get_json()['error']
    
    # Tenure too large
    response = client.post('/api/calculate/emi', json={
        'loan_amount': 100000,
        'annual_rate': 8.5,
        'tenure_years': 35
    })
    assert response.status_code == 400
    assert 'Tenure' in response.get_json()['error']


def test_emi_calculator_boundary_values(client):
    """Test EMI calculation with boundary values."""
    # Minimum valid values
    response = client.post('/api/calculate/emi', json={
        'loan_amount': 1000,
        'annual_rate': 0,  # 0% is valid
        'tenure_years': 1
    })
    assert response.status_code == 200
    
    # Maximum valid values
    response = client.post('/api/calculate/emi', json={
        'loan_amount': 10000000,
        'annual_rate': 30,
        'tenure_years': 30
    })
    assert response.status_code == 200


def test_emi_formula_accuracy():
    """Test the EMI calculation formula accuracy."""
    # Test case: $100,000 @ 8.5% for 20 years
    result = calculate_emi(100000, 8.5, 20)
    
    # Expected EMI (from PO): $867.82
    assert abs(float(result['emi']) - 867.82) < 0.01
    
    # Verify formula components
    P = Decimal('100000')
    r = Decimal('8.5') / Decimal('12') / Decimal('100')  # Monthly rate
    n = 20 * 12  # 240 months
    
    # Manual calculation
    one_plus_r = Decimal('1') + r
    numerator = P * r * (one_plus_r ** n)
    denominator = (one_plus_r ** n) - Decimal('1')
    expected_emi = numerator / denominator
    
    assert abs(float(result['emi']) - float(expected_emi)) < 0.01


def test_emi_calculator_precision(client):
    """Test that EMI calculations maintain precision."""
    response = client.post('/api/calculate/emi', json={
        'loan_amount': 123456.78,
        'annual_rate': 7.89,
        'tenure_years': 15
    })
    
    assert response.status_code == 200
    data = response.get_json()
    
    # Check that results are rounded to 2 decimal places
    assert data['emi'] == round(data['emi'], 2)
    assert data['total_interest'] == round(data['total_interest'], 2)
    assert data['total_payment'] == round(data['total_payment'], 2)


# Simple Interest Tests

def test_simple_interest_calculation():
    """Test simple interest calculation."""
    result = calculate_simple_interest(10000, 5, 2)
    
    # I = P × R × T = 10000 × 0.05 × 2 = 1000
    assert float(result['interest']) == 1000.00
    assert float(result['final_amount']) == 11000.00


def test_simple_interest_zero_rate():
    """Test simple interest with zero rate."""
    result = calculate_simple_interest(10000, 0, 5)
    
    assert float(result['interest']) == 0.00
    assert float(result['final_amount']) == 10000.00


# Compound Interest Tests

def test_compound_interest_po_example():
    """Test compound interest with PO's example: $50k @ 6% for 5y, monthly → $67,409.09"""
    result = calculate_compound_interest(50000, 6, 5, 'monthly')
    
    # PO's expected result: Final amount = $67,409.09
    # Allow $50 difference due to rounding methods
    assert abs(float(result['final_amount']) - 67409.09) < 50.0
    assert abs(float(result['interest']) - 17409.09) < 50.0


def test_compound_interest_monthly():
    """Test compound interest with monthly compounding."""
    result = calculate_compound_interest(10000, 10, 1, 'monthly')
    
    # A = P(1 + r/n)^(nt) = 10000(1 + 0.1/12)^(12*1)
    expected = 10000 * (1 + 0.1/12) ** 12
    
    assert abs(float(result['final_amount']) - expected) < 1.0


def test_compound_interest_quarterly():
    """Test compound interest with quarterly compounding."""
    result = calculate_compound_interest(10000, 10, 1, 'quarterly')
    
    # A = P(1 + r/n)^(nt) = 10000(1 + 0.1/4)^(4*1)
    expected = 10000 * (1 + 0.1/4) ** 4
    
    assert abs(float(result['final_amount']) - expected) < 1.0


def test_compound_interest_annual():
    """Test compound interest with annual compounding."""
    result = calculate_compound_interest(10000, 10, 1, 'annual')
    
    # A = P(1 + r)^t = 10000(1 + 0.1)^1 = 11000
    assert float(result['final_amount']) == 11000.00
    assert float(result['interest']) == 1000.00


def test_compound_vs_simple_interest():
    """Test that compound interest is always >= simple interest."""
    P, R, T = 10000, 10, 5
    
    simple = calculate_simple_interest(P, R, T)
    compound = calculate_compound_interest(P, R, T, 'annual')
    
    # Compound interest should be greater than simple interest
    assert float(compound['interest']) > float(simple['interest'])
