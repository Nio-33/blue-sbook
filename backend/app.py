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
                'health': '/health'
            }
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
    app.run(debug=True, host='0.0.0.0', port=5000)

