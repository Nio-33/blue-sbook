#!/usr/bin/env python3
"""
Blue's Book - Setup Test Script
Tests if the application is properly configured
"""

import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_path))

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from app import create_app
        print("✅ Flask app import successful")
    except ImportError as e:
        print(f"❌ Flask app import failed: {e}")
        return False
    
    try:
        from services.firebase_service import firebase_service
        print("✅ Firebase service import successful")
    except ImportError as e:
        print(f"❌ Firebase service import failed: {e}")
        return False
    
    try:
        from services.data_loader import data_loader
        print("✅ Data loader import successful")
    except ImportError as e:
        print(f"❌ Data loader import failed: {e}")
        return False
    
    return True

def test_configuration():
    """Test if configuration is properly loaded"""
    print("\n🔍 Testing configuration...")
    
    try:
        from config import Config
        
        # Check required environment variables
        required_vars = [
            'FIREBASE_PROJECT_ID',
            'API_FOOTBALL_KEY'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not getattr(Config, var, None):
                missing_vars.append(var)
        
        if missing_vars:
            print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
            print("   Please check your .env file")
            return False
        
        print("✅ Configuration loaded successfully")
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_flask_app():
    """Test if Flask app can be created"""
    print("\n🔍 Testing Flask app creation...")
    
    try:
        from app import create_app
        app = create_app()
        
        # Test if app has required blueprints
        blueprint_names = [bp.name for bp in app.blueprints.values()]
        required_blueprints = ['players', 'managers', 'search']
        
        missing_blueprints = [bp for bp in required_blueprints if bp not in blueprint_names]
        
        if missing_blueprints:
            print(f"❌ Missing blueprints: {', '.join(missing_blueprints)}")
            return False
        
        print("✅ Flask app created successfully")
        print(f"   Blueprints loaded: {', '.join(blueprint_names)}")
        return True
        
    except Exception as e:
        print(f"❌ Flask app creation failed: {e}")
        return False

def test_file_structure():
    """Test if all required files exist"""
    print("\n🔍 Testing file structure...")
    
    required_files = [
        'backend/app.py',
        'backend/config.py',
        'backend/requirements.txt',
        'frontend/index.html',
        'frontend/css/tailwind.css',
        'frontend/js/app.js',
        'scripts/sync_squad.py',
        'env.example',
        '.gitignore'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files present")
    return True

def main():
    """Run all tests"""
    print("🔵 Blue's Book - Setup Test")
    print("=" * 50)
    
    tests = [
        test_file_structure,
        test_imports,
        test_configuration,
        test_flask_app
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Blue's Book is ready to run.")
        print("\n🚀 Next steps:")
        print("   1. Configure your .env file with API keys")
        print("   2. Run: python run.py")
        print("   3. Open: http://localhost:5000")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\n🔧 Troubleshooting:")
        print("   1. Make sure you're in the project root directory")
        print("   2. Check that all files are present")
        print("   3. Verify your Python environment is activated")
        print("   4. Install requirements: pip install -r backend/requirements.txt")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

