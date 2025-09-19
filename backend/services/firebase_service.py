"""
Firebase service for Blue's Book
Handles Firestore database and Firebase Storage operations
"""

import firebase_admin
from firebase_admin import credentials, firestore, storage
from typing import Dict, List, Optional, Any
import json
import os
from config import Config

class FirebaseService:
    """Service class for Firebase operations"""
    
    def __init__(self):
        """Initialize Firebase service"""
        self.db = None
        self.bucket = None
        self._initialize_firebase()
    
    def _initialize_firebase(self):
        """Initialize Firebase Admin SDK"""
        try:
            # Check if Firebase is already initialized
            if not firebase_admin._apps:
                # Create credentials from environment variables
                cred_dict = {
                    "type": "service_account",
                    "project_id": Config.FIREBASE_PROJECT_ID,
                    "private_key_id": Config.FIREBASE_PRIVATE_KEY_ID,
                    "private_key": Config.FIREBASE_PRIVATE_KEY.replace('\\n', '\n'),
                    "client_email": Config.FIREBASE_CLIENT_EMAIL,
                    "client_id": Config.FIREBASE_CLIENT_ID,
                    "auth_uri": Config.FIREBASE_AUTH_URI,
                    "token_uri": Config.FIREBASE_TOKEN_URI,
                }
                
                cred = credentials.Certificate(cred_dict)
                firebase_admin.initialize_app(cred, {
                    'storageBucket': f"{Config.FIREBASE_PROJECT_ID}.appspot.com"
                })
            
            # Initialize Firestore and Storage
            self.db = firestore.client()
            self.bucket = storage.bucket()
            
        except Exception as e:
            print(f"Firebase initialization error: {e}")
            # For development, create a mock service
            self.db = None
            self.bucket = None
    
    # Player Operations
    def get_player(self, player_id: str) -> Optional[Dict]:
        """Get a single player by ID"""
        if not self.db:
            return None
        
        try:
            doc_ref = self.db.collection('players').document(player_id)
            doc = doc_ref.get()
            
            if doc.exists:
                return doc.to_dict()
            return None
        except Exception as e:
            print(f"Error getting player {player_id}: {e}")
            return None
    
    def get_all_players(self, filters: Optional[Dict] = None) -> List[Dict]:
        """Get all players with optional filters"""
        if not self.db:
            return []
        
        try:
            query = self.db.collection('players')
            
            # Apply filters
            if filters:
                if 'position' in filters:
                    query = query.where('position', '==', filters['position'])
                if 'is_active' in filters:
                    query = query.where('is_active', '==', filters['is_active'])
            
            # Execute query
            docs = query.stream()
            players = []
            
            for doc in docs:
                player_data = doc.to_dict()
                player_data['player_id'] = doc.id
                players.append(player_data)
            
            return players
        except Exception as e:
            print(f"Error getting players: {e}")
            return []
    
    def search_players(self, query: str, limit: int = 10) -> List[Dict]:
        """Search players by name"""
        if not self.db:
            return []
        
        try:
            # Get all players and filter by name (Firestore doesn't support full-text search)
            all_players = self.get_all_players({'is_active': True})
            
            # Filter by name containing query (case-insensitive)
            query_lower = query.lower()
            matching_players = [
                player for player in all_players
                if query_lower in player.get('name', '').lower()
            ]
            
            # Sort by relevance (exact matches first, then partial matches)
            matching_players.sort(key=lambda x: (
                not x.get('name', '').lower().startswith(query_lower),
                x.get('name', '')
            ))
            
            return matching_players[:limit]
        except Exception as e:
            print(f"Error searching players: {e}")
            return []
    
    def get_random_player(self) -> Optional[Dict]:
        """Get a random active player"""
        if not self.db:
            return None
        
        try:
            active_players = self.get_all_players({'is_active': True})
            if active_players:
                import random
                return random.choice(active_players)
            return None
        except Exception as e:
            print(f"Error getting random player: {e}")
            return None
    
    def save_player(self, player_id: str, player_data: Dict) -> bool:
        """Save or update a player"""
        if not self.db:
            return False
        
        try:
            doc_ref = self.db.collection('players').document(player_id)
            doc_ref.set(player_data)
            return True
        except Exception as e:
            print(f"Error saving player {player_id}: {e}")
            return False
    
    def update_player(self, player_id: str, updates: Dict) -> bool:
        """Update specific fields of a player"""
        if not self.db:
            return False
        
        try:
            doc_ref = self.db.collection('players').document(player_id)
            doc_ref.update(updates)
            return True
        except Exception as e:
            print(f"Error updating player {player_id}: {e}")
            return False
    
    # Manager Operations
    def get_current_manager(self) -> Optional[Dict]:
        """Get current Chelsea manager"""
        if not self.db:
            return None
        
        try:
            doc_ref = self.db.collection('managers').document('current')
            doc = doc_ref.get()
            
            if doc.exists:
                return doc.to_dict()
            return None
        except Exception as e:
            print(f"Error getting current manager: {e}")
            return None
    
    def save_manager(self, manager_data: Dict) -> bool:
        """Save current manager information"""
        if not self.db:
            return False
        
        try:
            doc_ref = self.db.collection('managers').document('current')
            doc_ref.set(manager_data)
            return True
        except Exception as e:
            print(f"Error saving manager: {e}")
            return False
    
    # Image Operations
    def upload_image(self, file_path: str, destination_path: str) -> Optional[str]:
        """Upload image to Firebase Storage"""
        if not self.bucket:
            return None
        
        try:
            blob = self.bucket.blob(destination_path)
            blob.upload_from_filename(file_path)
            
            # Make the blob publicly accessible
            blob.make_public()
            
            return blob.public_url
        except Exception as e:
            print(f"Error uploading image: {e}")
            return None
    
    def get_image_url(self, image_path: str) -> str:
        """Get public URL for an image"""
        if not self.bucket:
            return ""
        
        try:
            blob = self.bucket.blob(image_path)
            return blob.public_url
        except Exception as e:
            print(f"Error getting image URL: {e}")
            return ""
    
    # Utility Methods
    def get_collection_stats(self, collection_name: str) -> Dict:
        """Get statistics for a collection"""
        if not self.db:
            return {}
        
        try:
            collection_ref = self.db.collection(collection_name)
            docs = collection_ref.stream()
            
            total_docs = 0
            active_docs = 0
            
            for doc in docs:
                total_docs += 1
                data = doc.to_dict()
                if data.get('is_active', False):
                    active_docs += 1
            
            return {
                'total': total_docs,
                'active': active_docs,
                'inactive': total_docs - active_docs
            }
        except Exception as e:
            print(f"Error getting collection stats: {e}")
            return {}

# Global Firebase service instance
firebase_service = FirebaseService()

