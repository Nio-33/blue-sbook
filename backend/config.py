"""
Configuration settings for Blue's Book application
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration class"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # API-Football Configuration
    API_FOOTBALL_KEY = os.getenv('API_FOOTBALL_KEY')
    API_FOOTBALL_URL = os.getenv('API_FOOTBALL_URL', 'https://api-football-v1.p.rapidapi.com/v3')
    
    # Firebase Configuration
    FIREBASE_PROJECT_ID = os.getenv('FIREBASE_PROJECT_ID')
    FIREBASE_PRIVATE_KEY_ID = os.getenv('FIREBASE_PRIVATE_KEY_ID')
    FIREBASE_PRIVATE_KEY = os.getenv('FIREBASE_PRIVATE_KEY')
    FIREBASE_CLIENT_EMAIL = os.getenv('FIREBASE_CLIENT_EMAIL')
    FIREBASE_CLIENT_ID = os.getenv('FIREBASE_CLIENT_ID')
    FIREBASE_AUTH_URI = os.getenv('FIREBASE_AUTH_URI', 'https://accounts.google.com/o/oauth2/auth')
    FIREBASE_TOKEN_URI = os.getenv('FIREBASE_TOKEN_URI', 'https://accounts.google.com/o/oauth2/token')
    
    # Redis Configuration
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
    
    # Performance Settings
    CACHE_TTL = 86400  # 24 hours in seconds
    SEARCH_TIMEOUT = 0.3  # 300ms search timeout
    MAX_SEARCH_RESULTS = 10
    
    # Chelsea FC Configuration
    CHELSEA_TEAM_ID = 49  # Chelsea FC team ID in API-Football
    CHELSEA_LEAGUE_ID = 39  # Premier League ID
    
    # Data Quality Settings
    MIN_FUN_FACTS = 3
    MAX_FUN_FACTS = 5
    REQUIRED_FIELDS = [
        'name', 'position', 'jersey_number', 'nationality', 
        'age', 'image_url', 'is_active'
    ]

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    FIREBASE_PROJECT_ID = 'test-project'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

