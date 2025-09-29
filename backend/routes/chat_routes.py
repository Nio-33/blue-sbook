"""
Chat API routes for Blue's Book
Handles chat functionality with Gemini AI for Chelsea FC history
"""

from flask import Blueprint, jsonify, request
import sys
import os
import time
import logging
from typing import List, Dict

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add services directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services'))

chat_bp = Blueprint('chat', __name__)

def get_gemini_service():
    """Get GeminiService instance with error handling"""
    try:
        from gemini_service import GeminiService
        return GeminiService()
    except Exception as e:
        logger.error(f"Failed to initialize GeminiService: {str(e)}")
        return None

@chat_bp.route('/send', methods=['POST'])
def send_message():
    """Send a message to the Chelsea FC chat AI"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'success': False,
                'error': 'Message is required'
            }), 400
        
        user_message = data['message'].strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'Message cannot be empty'
            }), 400
        
        if len(user_message) > 500:
            return jsonify({
                'success': False,
                'error': 'Message too long (max 500 characters)'
            }), 400
        
        # Get chat history if provided
        chat_history = data.get('history', [])
        
        # Initialize Gemini service
        gemini_service = get_gemini_service()
        if not gemini_service:
            return jsonify({
                'success': False,
                'error': 'AI service initialization failed',
                'message': "I'm sorry, but the AI chat service is not currently available. Please check the server configuration."
            }), 503
        
        start_time = time.time()
        
        # Generate AI response
        response_data = gemini_service.generate_response(user_message, chat_history)
        
        query_time = (time.time() - start_time) * 1000
        
        # Add timing information
        response_data['query_time'] = f"{query_time:.2f}ms"
        response_data['timestamp'] = int(time.time() * 1000)
        
        # If there's a configuration error, return appropriate status code
        if not response_data.get('success', False) and 'not configured' in response_data.get('error', ''):
            return jsonify(response_data), 503  # Service Unavailable
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}',
            'message': "I'm sorry, something went wrong. Please try again."
        }), 500

@chat_bp.route('/suggestions', methods=['GET'])
def get_suggestions():
    """Get suggested questions for Chelsea FC chat"""
    try:
        # Initialize Gemini service
        gemini_service = get_gemini_service()
        if not gemini_service:
            return jsonify({
                'success': False,
                'error': 'AI service not available'
            }), 503
            
        suggestions = gemini_service.get_suggested_questions()
        
        return jsonify({
            'success': True,
            'data': suggestions,
            'total': len(suggestions)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@chat_bp.route('/health', methods=['GET'])
def chat_health():
    """Check if chat service is healthy"""
    try:
        # Initialize Gemini service
        gemini_service = get_gemini_service()
        if not gemini_service:
            return jsonify({
                'success': True,
                'healthy': False,
                'service': 'Gemini AI Chat',
                'status': 'service_initialization_failed'
            })
            
        # Validate API key and service
        is_healthy = gemini_service.validate_api_key()
        
        return jsonify({
            'success': True,
            'healthy': is_healthy,
            'service': 'Gemini AI Chat',
            'status': 'operational' if is_healthy else 'api_key_missing'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'healthy': False,
            'error': str(e)
        }), 500

@chat_bp.route('/context', methods=['GET'])
def get_chat_context():
    """Get information about what the chat can help with"""
    try:
        # Initialize Gemini service
        gemini_service = get_gemini_service()
        sample_questions = []
        if gemini_service:
            try:
                sample_questions = gemini_service.get_suggested_questions()[:5]
            except:
                sample_questions = [
                    "When was Chelsea FC founded?",
                    "Tell me about Chelsea's Champions League victories",
                    "Who are Chelsea's greatest managers?",
                    "What trophies has Chelsea won?",
                    "Tell me about Stamford Bridge stadium"
                ]
        
        context_info = {
            'name': 'Chelsea FC History Assistant',
            'description': 'Ask me anything about Chelsea Football Club history, players, managers, trophies, and facts!',
            'capabilities': [
                'Chelsea FC history and timeline',
                'Player information and statistics',
                'Manager profiles and achievements', 
                'Trophy wins and memorable matches',
                'Stadium and facilities information',
                'Club records and milestones'
            ],
            'sample_questions': sample_questions
        }
        
        return jsonify({
            'success': True,
            'data': context_info
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500