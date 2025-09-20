"""
Player API routes for Blue's Book
Handles all player-related endpoints
"""

from flask import Blueprint, jsonify, request
import sys
import os

# Add data directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data'))
from chelsea_players import (
    get_all_players, get_player_by_id, get_random_player, 
    search_players, filter_players_by_position, sort_players,
    calculate_advanced_statistics
)
import time

player_bp = Blueprint('players', __name__)

@player_bp.route('/', methods=['GET'])
def get_players():
    """Get all players with optional filtering"""
    try:
        # Get query parameters
        position = request.args.get('position')
        sort_by = request.args.get('sort_by', 'jersey_number')
        limit = int(request.args.get('limit', 50))
        
        start_time = time.time()
        
        # Get all players
        players = get_all_players()
        
        # Filter by position if specified
        if position:
            players = filter_players_by_position(position)
        
        # Sort players
        players = sort_players(players, sort_by)
        
        # Apply limit
        players = players[:limit]
        
        query_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        return jsonify({
            'success': True,
            'data': players,
            'total': len(players),
            'query_time': f"{query_time:.2f}ms",
            'filters_applied': {
                'position': position,
                'sort_by': sort_by
            }
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
        player = get_player_by_id(player_id)
        query_time = (time.time() - start_time) * 1000
        
        if not player:
            return jsonify({
                'success': False,
                'error': 'Player not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': player,
            'query_time': f"{query_time:.2f}ms"
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@player_bp.route('/random', methods=['GET'])
def get_random_player_route():
    """Get random player of the day"""
    try:
        start_time = time.time()
        player = get_random_player()
        query_time = (time.time() - start_time) * 1000
        
        if not player:
            return jsonify({
                'success': False,
                'error': 'No active players found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': player,
            'query_time': f"{query_time:.2f}ms",
            'feature': 'Random Player of the Day'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@player_bp.route('/search', methods=['GET'])
def search_players_route():
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
        players = search_players(query)[:limit]
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
        players = get_all_players()
        active_players = [p for p in players if p.get('is_active', True)]
        
        return jsonify({
            'success': True,
            'data': {
                'total_players': len(players),
                'active_players': len(active_players),
                'inactive_players': len(players) - len(active_players),
                'last_updated': players[0].get('last_updated') if players else 'Unknown'
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@player_bp.route('/statistics/advanced', methods=['GET'])
def get_advanced_statistics_route():
    """Get comprehensive squad statistics"""
    try:
        start_time = time.time()
        stats = calculate_advanced_statistics()
        query_time = (time.time() - start_time) * 1000
        
        return jsonify({
            'success': True,
            'data': stats,
            'query_time': f"{query_time:.2f}ms"
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500