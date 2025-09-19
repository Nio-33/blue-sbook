"""
Manager API routes for Blue's Book
Handles manager-related endpoints
"""

from flask import Blueprint, jsonify, request
from services.firebase_service import firebase_service
from utils.formatters import format_manager_response
import time

manager_bp = Blueprint('managers', __name__)

@manager_bp.route('/current', methods=['GET'])
def get_current_manager():
    """Get current Chelsea manager"""
    try:
        start_time = time.time()
        manager = firebase_service.get_current_manager()
        query_time = (time.time() - start_time) * 1000
        
        if not manager:
            return jsonify({
                'success': False,
                'error': 'Current manager not found'
            }), 404
        
        # Format response
        formatted_manager = format_manager_response(manager)
        
        return jsonify({
            'success': True,
            'data': formatted_manager,
            'query_time': f"{query_time:.2f}ms"
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@manager_bp.route('/history', methods=['GET'])
def get_manager_history():
    """Get Chelsea manager history (placeholder for future implementation)"""
    try:
        # This would be implemented in Phase 2 or 3
        return jsonify({
            'success': True,
            'data': [],
            'message': 'Manager history feature coming soon'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

