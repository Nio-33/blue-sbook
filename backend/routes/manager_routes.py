"""
Manager API routes for Blue's Book
Handles manager-related endpoints
"""

from flask import Blueprint, jsonify, request
import sys
import os

# Add data directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data'))
from chelsea_players import (
    get_current_manager, get_all_managers, get_manager_by_id, 
    search_managers, get_managers_by_status
)
import time

manager_bp = Blueprint('managers', __name__)

@manager_bp.route('/current', methods=['GET'])
def get_current_manager_route():
    """Get current Chelsea manager"""
    try:
        start_time = time.time()
        manager = get_current_manager()
        query_time = (time.time() - start_time) * 1000
        
        if not manager:
            return jsonify({
                'success': False,
                'error': 'Current manager not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': manager,
            'query_time': f"{query_time:.2f}ms"
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@manager_bp.route('/history', methods=['GET'])
def get_manager_history():
    """Get all Chelsea managers (historical and current)"""
    try:
        start_time = time.time()
        managers = get_all_managers()
        query_time = (time.time() - start_time) * 1000
        
        return jsonify({
            'success': True,
            'data': managers,
            'total': len(managers),
            'query_time': f"{query_time:.2f}ms"
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@manager_bp.route('/search', methods=['GET'])
def search_managers_route():
    """Search managers by name with autocomplete"""
    try:
        query = request.args.get('q', '').strip()
        limit = int(request.args.get('limit', 10))
        
        if len(query) < 2:
            return jsonify({
                'success': False,
                'error': 'Query must be at least 2 characters long'
            }), 400
        
        start_time = time.time()
        managers = search_managers(query)[:limit]
        query_time = (time.time() - start_time) * 1000
        
        return jsonify({
            'success': True,
            'data': managers,
            'query': query,
            'total': len(managers),
            'query_time': f"{query_time:.2f}ms"
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@manager_bp.route('/<manager_id>', methods=['GET'])
def get_manager_by_id_route(manager_id):
    """Get specific manager by ID"""
    try:
        start_time = time.time()
        manager = get_manager_by_id(manager_id)
        query_time = (time.time() - start_time) * 1000
        
        if not manager:
            return jsonify({
                'success': False,
                'error': 'Manager not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': manager,
            'query_time': f"{query_time:.2f}ms"
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

