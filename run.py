#!/usr/bin/env python3
"""
Blue's Book - Application Runner
Simple script to run the Flask application
"""

import os
import sys
from pathlib import Path

# Add backend to Python path
backend_path = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_path))

# Set environment variables
os.environ.setdefault('FLASK_APP', 'app.py')
os.environ.setdefault('FLASK_ENV', 'development')

if __name__ == '__main__':
    from app import create_app
    
    app = create_app()
    print("🔵 Blue's Book - Starting Flask Application")
    print("=" * 50)
    print("🌐 Server: http://localhost:5000")
    print("📚 API Docs: http://localhost:5000")
    print("🔍 Health Check: http://localhost:5000/health")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

