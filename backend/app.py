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

# Import routes
from routes.player_routes import player_bp
from routes.manager_routes import manager_bp
from routes.search_routes import search_bp
from routes.chat_routes import chat_bp

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
    CORS(app, origins=['http://localhost:3000', 'http://127.0.0.1:5000', 'http://localhost:5000'])
    
    # Register blueprints
    app.register_blueprint(player_bp, url_prefix='/api/v1/players')
    app.register_blueprint(manager_bp, url_prefix='/api/v1/managers')
    app.register_blueprint(search_bp, url_prefix='/api/v1/search')
    app.register_blueprint(chat_bp, url_prefix='/api/v1/chat')
    
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
    app.run(debug=True, host='0.0.0.0', port=5000)

