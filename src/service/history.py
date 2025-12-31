"""
History management endpoints for calculation history.
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from src.service.database import db
from src.service.models import CalculationHistory

history_bp = Blueprint('history', __name__, url_prefix='/api/history')


@history_bp.route('', methods=['GET'])
@login_required
def get_history():
    """
    Get user's calculation history.
    
    Query parameters:
        limit (int): Maximum number of results (default: 50, max: 100)
        page (int): Page number for pagination (default: 1)
    
    Returns:
        200: {
            "calculations": [
                {
                    "id": int,
                    "calculation_type": str,
                    "expression": str,
                    "result": str,
                    "timestamp": str (ISO 8601)
                }
            ],
            "total": int,
            "page": int,
            "per_page": int
        }
    """
    # Parse query parameters
    limit = request.args.get('limit', 50, type=int)
    page = request.args.get('page', 1, type=int)
    
    # Validate parameters
    if limit < 1 or limit > 100:
        return jsonify({'error': 'Limit must be between 1 and 100'}), 400
    if page < 1:
        return jsonify({'error': 'Page must be at least 1'}), 400
    
    # Query calculations for current user
    query = CalculationHistory.query.filter_by(user_id=current_user.id).order_by(
        CalculationHistory.timestamp.desc()
    )
    
    # Get total count
    total = query.count()
    
    # Paginate
    calculations = query.limit(limit).offset((page - 1) * limit).all()
    
    return jsonify({
        'calculations': [calc.to_dict() for calc in calculations],
        'total': total,
        'page': page,
        'per_page': limit
    }), 200


@history_bp.route('', methods=['POST'])
@login_required
def save_calculation():
    """
    Save a calculation to history.
    
    Request body:
        {
            "calculation_type": str (required) - 'basic', 'scientific', 'emi', etc.
            "expression": str (required) - The calculation expression
            "result": str (required) - The calculation result
        }
    
    Returns:
        201: {"success": true, "id": int}
        400: {"error": str} - validation error
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400
    
    # Validate required fields
    calculation_type = data.get('calculation_type', '').strip()
    expression = data.get('expression', '').strip()
    result = data.get('result', '').strip()
    
    if not calculation_type:
        return jsonify({'error': 'calculation_type is required'}), 400
    if not expression:
        return jsonify({'error': 'expression is required'}), 400
    if not result:
        return jsonify({'error': 'result is required'}), 400
    
    # Validate calculation_type
    valid_types = ['basic', 'scientific', 'emi', 'simple_interest', 'compound_interest']
    if calculation_type not in valid_types:
        return jsonify({'error': f'Invalid calculation_type. Must be one of: {", ".join(valid_types)}'}), 400
    
    # Validate length
    if len(expression) > 500:
        return jsonify({'error': 'expression too long (max 500 characters)'}), 400
    if len(result) > 100:
        return jsonify({'error': 'result too long (max 100 characters)'}), 400
    
    # Create history entry
    calculation = CalculationHistory(
        user_id=current_user.id,
        calculation_type=calculation_type,
        expression=expression,
        result=result
    )
    
    db.session.add(calculation)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'id': calculation.id
    }), 201


@history_bp.route('', methods=['DELETE'])
@login_required
def clear_history():
    """
    Clear all calculation history for the current user.
    
    Returns:
        200: {"success": true, "message": str, "deleted_count": int}
    """
    # Delete all calculations for current user
    deleted_count = CalculationHistory.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'Deleted {deleted_count} calculation(s)',
        'deleted_count': deleted_count
    }), 200
