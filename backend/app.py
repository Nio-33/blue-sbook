"""
Blue's Book - Flask Application Entry Point
The definitive digital reference for Chelsea FC squad information
"""

from flask import Flask, jsonify, request, send_from_directory, render_template_string
from flask_cors import CORS
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from project root
load_dotenv(dotenv_path=Path(__file__).parent.parent / '.env')

# Import routes with error handling
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from routes.player_routes import player_bp
    logger.info("✅ Successfully imported player_routes")
except Exception as e:
    logger.error(f"❌ Failed to import player_routes: {str(e)}")
    player_bp = None

try:
    from routes.manager_routes import manager_bp
    logger.info("✅ Successfully imported manager_routes")
except Exception as e:
    logger.error(f"❌ Failed to import manager_routes: {str(e)}")
    manager_bp = None

try:
    from routes.search_routes import search_bp
    logger.info("✅ Successfully imported search_routes")
except Exception as e:
    logger.error(f"❌ Failed to import search_routes: {str(e)}")
    search_bp = None

try:
    from routes.chat_routes import chat_bp
    logger.info("✅ Successfully imported chat_routes")
except Exception as e:
    logger.error(f"❌ Failed to import chat_routes: {str(e)}")
    logger.error(f"Error details: {repr(e)}")
    chat_bp = None

def create_app():
    """Create and configure the Flask application"""
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    
    app = Flask(__name__, 
                static_folder=str(project_root / 'frontend'),
                static_url_path='')
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['FLASK_ENV'] = os.getenv('FLASK_ENV', 'development')
    
    # Debug environment variables (only in development)
    if app.config['FLASK_ENV'] == 'development':
        gemini_key = os.getenv('GEMINI_API_KEY')
        if gemini_key:
            print(f"✅ GEMINI_API_KEY loaded: {gemini_key[:10]}...")
        else:
            print("❌ GEMINI_API_KEY not found in environment variables")
        
        api_football_key = os.getenv('API_FOOTBALL_KEY')
        if api_football_key and api_football_key != 'your-api-football-key-here':
            print(f"✅ API_FOOTBALL_KEY loaded: {api_football_key[:10]}...")
        else:
            print("⚠️ API_FOOTBALL_KEY not configured (optional)")
            
        print(f"📁 Environment file location: {project_root / '.env'}")
        print(f"🔍 Environment file exists: {(project_root / '.env').exists()}")
    
    # Enable CORS for frontend
    CORS(app, origins=[
        'http://localhost:5001',
        'http://127.0.0.1:5001',
        'http://192.168.0.113:5001'
    ])
    
    # Register blueprints with error handling
    blueprints_registered = []
    
    if player_bp:
        app.register_blueprint(player_bp, url_prefix='/api/v1/players')
        blueprints_registered.append('players')
        logger.info("✅ Registered player routes")
    else:
        logger.error("❌ Skipped player routes (import failed)")
    
    if manager_bp:
        app.register_blueprint(manager_bp, url_prefix='/api/v1/managers')
        blueprints_registered.append('managers')
        logger.info("✅ Registered manager routes")
    else:
        logger.error("❌ Skipped manager routes (import failed)")
    
    if search_bp:
        app.register_blueprint(search_bp, url_prefix='/api/v1/search')
        blueprints_registered.append('search')
        logger.info("✅ Registered search routes")
    else:
        logger.error("❌ Skipped search routes (import failed)")
    
    if chat_bp:
        app.register_blueprint(chat_bp, url_prefix='/api/v1/chat')
        blueprints_registered.append('chat')
        logger.info("✅ Registered chat routes")
    else:
        logger.error("❌ Skipped chat routes (import failed)")
    
    logger.info(f"📋 Total blueprints registered: {len(blueprints_registered)} - {blueprints_registered}")
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'Blue\'s Book API',
            'version': '1.0.0'
        })
    
    # API info endpoint
    @app.route('/api')
    def api_info():
        return jsonify({
            'message': 'Welcome to Blue\'s Book API',
            'version': '1.0.0',
            'endpoints': {
                'players': '/api/v1/players',
                'managers': '/api/v1/managers',
                'search': '/api/v1/search',
                'chat': '/api/v1/chat',
                'health': '/health',
                'debug': '/debug'
            }
        })
    
    # Debug endpoint for API configuration
    @app.route('/debug')
    def debug_config():
        """Debug endpoint to check API configuration"""
        if app.config['FLASK_ENV'] != 'development':
            return jsonify({'error': 'Debug endpoint only available in development'}), 403
            
        # Import here to avoid circular imports
        from services.gemini_service import GeminiService
        
        debug_info = {
            'environment': app.config['FLASK_ENV'],
            'gemini_api_key_configured': bool(os.getenv('GEMINI_API_KEY')),
            'api_football_key_configured': bool(os.getenv('API_FOOTBALL_KEY') and os.getenv('API_FOOTBALL_KEY') != 'your-api-football-key-here'),
            'env_file_exists': (Path(__file__).parent.parent / '.env').exists()
        }
        
        # Test Gemini service
        try:
            gemini_service = GeminiService()
            debug_info['gemini_service_initialized'] = True
            debug_info['gemini_api_key_present'] = bool(gemini_service.api_key)
            
            # Quick API test
            if gemini_service.api_key:
                test_response = gemini_service.generate_response("Test")
                debug_info['gemini_api_test'] = {
                    'success': test_response.get('success', False),
                    'error': test_response.get('error') if not test_response.get('success', False) else None
                }
            else:
                debug_info['gemini_api_test'] = {'success': False, 'error': 'No API key'}
                
        except Exception as e:
            debug_info['gemini_service_error'] = str(e)
            
        return jsonify(debug_info)
    
    # Debug endpoint to list all registered routes
    @app.route('/debug/routes')
    def debug_routes():
        """Debug endpoint to list all registered routes"""
        if app.config['FLASK_ENV'] != 'development':
            return jsonify({'error': 'Debug endpoint only available in development'}), 403
        
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({
                'endpoint': rule.endpoint,
                'methods': list(rule.methods - {'HEAD', 'OPTIONS'}),  # Remove automatic methods
                'rule': str(rule)
            })
        
        # Filter for chat routes specifically
        chat_routes = [r for r in routes if '/chat' in r['rule']]
        
        return jsonify({
            'total_routes': len(routes),
            'chat_routes': chat_routes,
            'chat_routes_count': len(chat_routes),
            'all_routes': sorted(routes, key=lambda x: x['rule'])
        })
    
    # Serve the main frontend application
    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, 'index.html')
    
    # Serve static files (CSS, JS, images)
    @app.route('/<path:filename>')
    def static_files(filename):
        return send_from_directory(app.static_folder, filename)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)

