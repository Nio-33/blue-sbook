"""
Search API routes for Blue's Book
Handles global search functionality
"""

from flask import Blueprint, jsonify, request
from services.firebase_service import firebase_service
from utils.formatters import format_search_result
import time

search_bp = Blueprint('search', __name__)

@search_bp.route('/', methods=['GET'])
def global_search():
    """Global search across players and managers"""
    try:
        query = request.args.get('q', '').strip()
        limit = int(request.args.get('limit', 20))
        category = request.args.get('category', 'all')  # all, players, managers
        
        if len(query) < 2:
            return jsonify({
                'success': False,
                'error': 'Query must be at least 2 characters long'
            }), 400
        
        start_time = time.time()
        results = []
        
        # Search players
        if category in ['all', 'players']:
            players = firebase_service.search_players(query, limit)
            for player in players:
                results.append({
                    'type': 'player',
                    'data': format_search_result(player, 'player')
                })
        
        # Search managers
        if category in ['all', 'managers']:
            manager = firebase_service.get_current_manager()
            if manager and query.lower() in manager.get('name', '').lower():
                results.append({
                    'type': 'manager',
                    'data': format_search_result(manager, 'manager')
                })
        
        query_time = (time.time() - start_time) * 1000
        
        # Sort results by relevance (exact matches first)
        results.sort(key=lambda x: (
            not x['data']['name'].lower().startswith(query.lower()),
            x['data']['name']
        ))
        
        # Apply limit
        results = results[:limit]
        
        return jsonify({
            'success': True,
            'data': results,
            'query': query,
            'total': len(results),
            'query_time': f"{query_time:.2f}ms",
            'categories_searched': ['players', 'managers'] if category == 'all' else [category]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@search_bp.route('/suggestions', methods=['GET'])
def get_search_suggestions():
    """Get search suggestions based on partial query"""
    try:
        query = request.args.get('q', '').strip()
        limit = int(request.args.get('limit', 5))
        
        if len(query) < 1:
            return jsonify({
                'success': True,
                'data': [],
                'query': query
            })
        
        start_time = time.time()
        
        # Get player suggestions
        players = firebase_service.search_players(query, limit)
        suggestions = []
        
        for player in players:
            suggestions.append({
                'text': player.get('name'),
                'type': 'player',
                'position': player.get('position'),
                'jersey_number': player.get('jersey_number')
            })
        
        query_time = (time.time() - start_time) * 1000
        
        return jsonify({
            'success': True,
            'data': suggestions,
            'query': query,
            'query_time': f"{query_time:.2f}ms"
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

