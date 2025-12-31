"""
Financial calculators including EMI, Simple Interest, and Compound Interest.
"""
from decimal import Decimal, ROUND_HALF_UP
from flask import Blueprint, request, jsonify

financial_bp = Blueprint('financial', __name__, url_prefix='/api/calculate')


def calculate_emi(loan_amount, annual_rate, tenure_years):
    """
    Calculate Equated Monthly Installment (EMI) for a loan.
    
    Formula: EMI = [P × r × (1+r)^n] / [(1+r)^n - 1]
    Where:
        P = Principal (loan amount)
        r = Monthly interest rate (annual_rate / 12 / 100)
        n = Number of months (tenure_years * 12)
    
    Args:
        loan_amount (float): Loan principal amount
        annual_rate (float): Annual interest rate (percentage)
        tenure_years (int): Loan tenure in years
    
    Returns:
        dict: {
            'emi': Decimal,  # Monthly EMI payment
            'total_interest': Decimal,  # Total interest paid
            'total_payment': Decimal  # Total amount paid (principal + interest)
        }
    """
    # Convert to Decimal for precision
    P = Decimal(str(loan_amount))
    annual_rate_decimal = Decimal(str(annual_rate))
    n = tenure_years * 12
    
    # Handle zero interest rate edge case
    if annual_rate == 0:
        emi = P / Decimal(str(n))
        total_payment = P
        total_interest = Decimal('0')
    else:
        # Calculate monthly rate
        r = annual_rate_decimal / Decimal('12') / Decimal('100')
        
        # Calculate EMI: [P × r × (1+r)^n] / [(1+r)^n - 1]
        one_plus_r = Decimal('1') + r
        one_plus_r_power_n = one_plus_r ** n
        
        numerator = P * r * one_plus_r_power_n
        denominator = one_plus_r_power_n - Decimal('1')
        
        emi = numerator / denominator
        
        # Calculate totals
        total_payment = emi * Decimal(str(n))
        total_interest = total_payment - P
    
    # Round to 2 decimal places
    emi = emi.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    total_interest = total_interest.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    total_payment = total_payment.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    return {
        'emi': emi,
        'total_interest': total_interest,
        'total_payment': total_payment
    }


@financial_bp.route('/emi', methods=['POST'])
def emi_calculator():
    """
    EMI Calculator endpoint.
    
    Request body:
        {
            "loan_amount": float (1000 - 10000000),
            "annual_rate": float (0.1 - 30),
            "tenure_years": int (1 - 30)
        }
    
    Returns:
        200: {
            "emi": float,  # Monthly EMI payment
            "total_interest": float,  # Total interest paid
            "total_payment": float  # Total amount paid
        }
        400: {"error": str} - validation error
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400
    
    # Extract and validate parameters
    try:
        loan_amount = data.get('loan_amount')
        annual_rate = data.get('annual_rate')
        tenure_years = data.get('tenure_years')
        
        if loan_amount is None:
            return jsonify({'error': 'loan_amount is required'}), 400
        if annual_rate is None:
            return jsonify({'error': 'annual_rate is required'}), 400
        if tenure_years is None:
            return jsonify({'error': 'tenure_years is required'}), 400
        
        # Convert to appropriate types
        loan_amount = float(loan_amount)
        annual_rate = float(annual_rate)
        tenure_years = int(tenure_years)
        
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid parameter types'}), 400
    
    # Validate ranges
    if loan_amount < 1000 or loan_amount > 10000000:
        return jsonify({'error': 'Loan amount must be between $1,000 and $10,000,000'}), 400
    
    if annual_rate < 0 or annual_rate > 30:
        return jsonify({'error': 'Annual rate must be between 0% and 30%'}), 400
    
    if tenure_years < 1 or tenure_years > 30:
        return jsonify({'error': 'Tenure must be between 1 and 30 years'}), 400
    
    # Calculate EMI
    result = calculate_emi(loan_amount, annual_rate, tenure_years)
    
    # Convert Decimal to float for JSON response
    return jsonify({
        'emi': float(result['emi']),
        'total_interest': float(result['total_interest']),
        'total_payment': float(result['total_payment'])
    }), 200


def calculate_simple_interest(principal, rate, time_years):
    """
    Calculate Simple Interest.
    
    Formula: I = P × R × T
    Where:
        P = Principal amount
        R = Rate of interest (as percentage)
        T = Time period in years
    
    Args:
        principal (float): Principal amount
        rate (float): Annual interest rate (percentage)
        time_years (float): Time period in years
    
    Returns:
        dict: {
            'interest': Decimal,  # Interest earned
            'final_amount': Decimal  # Principal + Interest
        }
    """
    P = Decimal(str(principal))
    R = Decimal(str(rate)) / Decimal('100')
    T = Decimal(str(time_years))
    
    interest = P * R * T
    final_amount = P + interest
    
    # Round to 2 decimal places
    interest = interest.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    final_amount = final_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    return {
        'interest': interest,
        'final_amount': final_amount
    }


def calculate_compound_interest(principal, rate, time_years, frequency):
    """
    Calculate Compound Interest.
    
    Formula: A = P(1 + r/n)^(nt)
    Where:
        P = Principal amount
        r = Annual interest rate (as decimal)
        n = Compounding frequency per year
        t = Time in years
    
    Args:
        principal (float): Principal amount
        rate (float): Annual interest rate (percentage)
        time_years (float): Time period in years
        frequency (str): Compounding frequency ('monthly', 'quarterly', 'annual')
    
    Returns:
        dict: {
            'interest': Decimal,  # Interest earned
            'final_amount': Decimal  # Principal + Interest
        }
    """
    P = Decimal(str(principal))
    r = Decimal(str(rate)) / Decimal('100')
    t = Decimal(str(time_years))
    
    # Determine compounding frequency
    frequency_map = {
        'monthly': 12,
        'quarterly': 4,
        'annual': 1
    }
    n = Decimal(str(frequency_map.get(frequency.lower(), 12)))
    
    # Calculate: A = P(1 + r/n)^(nt)
    rate_per_period = r / n
    num_periods = n * t
    
    final_amount = P * ((Decimal('1') + rate_per_period) ** num_periods)
    interest = final_amount - P
    
    # Round to 2 decimal places
    interest = interest.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    final_amount = final_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    return {
        'interest': interest,
        'final_amount': final_amount
    }
