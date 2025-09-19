"""
Player API routes for Blue's Book
Handles all player-related endpoints
"""

from flask import Blueprint, jsonify, request
from services.firebase_service import firebase_service
from utils.validators import validate_player_filters
from utils.formatters import format_player_response
import time

player_bp = Blueprint('players', __name__)

@player_bp.route('/', methods=['GET'])
def get_players():
    """Get all players with optional filtering"""
    try:
        # Get query parameters
        position = request.args.get('position')
        is_active = request.args.get('is_active', 'true').lower() == 'true'
        sort_by = request.args.get('sort_by', 'jersey_number')
        limit = int(request.args.get('limit', 50))
        
        # Validate filters
        filters = validate_player_filters({
            'position': position,
            'is_active': is_active
        })
        
        # Get players from Firebase
        start_time = time.time()
        players = firebase_service.get_all_players(filters)
        query_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        # Sort players
        if sort_by == 'jersey_number':
            players.sort(key=lambda x: x.get('jersey_number', 999))
        elif sort_by == 'age':
            players.sort(key=lambda x: x.get('age', 0), reverse=True)
        elif sort_by == 'name':
            players.sort(key=lambda x: x.get('name', ''))
        elif sort_by == 'signing_fee':
            # Sort by signing fee (simplified)
            players.sort(key=lambda x: x.get('signing_fee', '£0'), reverse=True)
        
        # Apply limit
        players = players[:limit]
        
        # Format response
        formatted_players = [format_player_response(player) for player in players]
        
        return jsonify({
            'success': True,
            'data': formatted_players,
            'total': len(formatted_players),
            'query_time': f"{query_time:.2f}ms",
            'filters_applied': filters
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@player_bp.route('/<player_id>', methods=['GET'])
def get_player(player_id):
    """Get specific player by ID"""
    try:
        start_time = time.time()
        player = firebase_service.get_player(player_id)
        query_time = (time.time() - start_time) * 1000
        
        if not player:
            return jsonify({
                'success': False,
                'error': 'Player not found'
            }), 404
        
        # Format response
        formatted_player = format_player_response(player, detailed=True)
        
        return jsonify({
            'success': True,
            'data': formatted_player,
            'query_time': f"{query_time:.2f}ms"
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@player_bp.route('/random', methods=['GET'])
def get_random_player():
    """Get random player of the day"""
    try:
        start_time = time.time()
        player = firebase_service.get_random_player()
        query_time = (time.time() - start_time) * 1000
        
        if not player:
            return jsonify({
                'success': False,
                'error': 'No active players found'
            }), 404
        
        # Format response
        formatted_player = format_player_response(player, detailed=True)
        
        return jsonify({
            'success': True,
            'data': formatted_player,
            'query_time': f"{query_time:.2f}ms",
            'feature': 'Random Player of the Day'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@player_bp.route('/search', methods=['GET'])
def search_players():
    """Search players by name with autocomplete"""
    try:
        query = request.args.get('q', '').strip()
        limit = int(request.args.get('limit', 10))
        
        if len(query) < 2:
            return jsonify({
                'success': False,
                'error': 'Query must be at least 2 characters long'
            }), 400
        
        start_time = time.time()
        players = firebase_service.search_players(query, limit)
        query_time = (time.time() - start_time) * 1000
        
        # Format response for autocomplete
        formatted_players = []
        for player in players:
            formatted_players.append({
                'player_id': player.get('player_id'),
                'name': player.get('name'),
                'position': player.get('position'),
                'jersey_number': player.get('jersey_number'),
                'image_url': player.get('image_url'),
                'nationality': player.get('nationality')
            })
        
        return jsonify({
            'success': True,
            'data': formatted_players,
            'query': query,
            'total': len(formatted_players),
            'query_time': f"{query_time:.2f}ms"
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@player_bp.route('/stats', methods=['GET'])
def get_player_stats():
    """Get player statistics and collection info"""
    try:
        stats = firebase_service.get_collection_stats('players')
        
        return jsonify({
            'success': True,
            'data': {
                'total_players': stats.get('total', 0),
                'active_players': stats.get('active', 0),
                'inactive_players': stats.get('inactive', 0),
                'last_updated': firebase_service.get_player('last_updated') or 'Unknown'
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

