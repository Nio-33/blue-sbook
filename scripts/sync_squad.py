#!/usr/bin/env python3
"""
Blue's Book - Squad Data Synchronization Script
Syncs player data from API-Football to Firebase
"""

import sys
import os
import argparse
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.data_loader import data_loader
from services.firebase_service import firebase_service

def sync_squad_data():
    """Sync squad data from API-Football to Firebase"""
    print("🔵 Blue's Book - Squad Data Sync")
    print("=" * 50)
    
    try:
        # Check if Firebase is available
        if not firebase_service.db:
            print("❌ Firebase not initialized. Please check your configuration.")
            return False
        
        # Check if API-Football is available
        if not data_loader.api_key:
            print("❌ API-Football key not configured. Please check your .env file.")
            return False
        
        print("🔄 Starting data synchronization...")
        print(f"📅 Sync time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Perform sync
        results = data_loader.sync_all_data()
        
        # Display results
        print("\n📊 Sync Results:")
        print(f"✅ Players synced: {results['players_synced']}")
        print(f"❌ Player errors: {results['players_errors']}")
        print(f"✅ Manager synced: {'Yes' if results['manager_synced'] else 'No'}")
        print(f"❌ Manager errors: {results['manager_errors']}")
        
        # Get collection stats
        player_stats = firebase_service.get_collection_stats('players')
        print(f"\n📈 Database Stats:")
        print(f"Total players: {player_stats.get('total', 0)}")
        print(f"Active players: {player_stats.get('active', 0)}")
        print(f"Inactive players: {player_stats.get('inactive', 0)}")
        
        if results['players_synced'] > 0 or results['manager_synced']:
            print("\n🎉 Sync completed successfully!")
            return True
        else:
            print("\n⚠️  Sync completed with no new data.")
            return False
            
    except Exception as e:
        print(f"\n❌ Sync failed: {str(e)}")
        return False

def test_api_connection():
    """Test API-Football connection"""
    print("🔍 Testing API-Football connection...")
    
    try:
        # Test with a simple request
        squad = data_loader.get_chelsea_squad()
        if squad:
            print(f"✅ API connection successful. Found {len(squad)} players.")
            return True
        else:
            print("❌ API connection failed. No data returned.")
            return False
    except Exception as e:
        print(f"❌ API connection failed: {str(e)}")
        return False

def test_firebase_connection():
    """Test Firebase connection"""
    print("🔍 Testing Firebase connection...")
    
    try:
        if firebase_service.db:
            # Try to get collection stats
            stats = firebase_service.get_collection_stats('players')
            print(f"✅ Firebase connection successful. Players in database: {stats.get('total', 0)}")
            return True
        else:
            print("❌ Firebase connection failed. Not initialized.")
            return False
    except Exception as e:
        print(f"❌ Firebase connection failed: {str(e)}")
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Sync Chelsea FC squad data')
    parser.add_argument('--test-api', action='store_true', help='Test API-Football connection')
    parser.add_argument('--test-firebase', action='store_true', help='Test Firebase connection')
    parser.add_argument('--test-all', action='store_true', help='Test all connections')
    parser.add_argument('--force', action='store_true', help='Force sync even if recent data exists')
    
    args = parser.parse_args()
    
    if args.test_all or args.test_api:
        if not test_api_connection():
            sys.exit(1)
    
    if args.test_all or args.test_firebase:
        if not test_firebase_connection():
            sys.exit(1)
    
    if args.test_all:
        print("\n✅ All tests passed!")
        sys.exit(0)
    
    # Perform sync
    success = sync_squad_data()
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()

