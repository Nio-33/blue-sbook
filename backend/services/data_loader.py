"""
Data loader service for Blue's Book
Handles API-Football integration and data synchronization
"""

import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import time
from config import Config
from services.firebase_service import firebase_service

class DataLoader:
    """Service class for loading and syncing data from API-Football"""
    
    def __init__(self):
        """Initialize data loader"""
        self.api_key = Config.API_FOOTBALL_KEY
        self.base_url = Config.API_FOOTBALL_URL
        self.headers = {
            'X-RapidAPI-Key': self.api_key,
            'X-RapidAPI-Host': 'api-football-v1.p.rapidapi.com'
        }
        self.team_id = Config.CHELSEA_TEAM_ID
        self.league_id = Config.CHELSEA_LEAGUE_ID
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Make API request to API-Football"""
        try:
            url = f"{self.base_url}/{endpoint}"
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"API request failed: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error making API request: {e}")
            return None
    
    def get_chelsea_squad(self) -> List[Dict]:
        """Get current Chelsea FC squad from API-Football"""
        try:
            params = {
                'team': self.team_id,
                'season': 2024  # Current season
            }
            
            response = self._make_request('players/squads', params)
            
            if response and 'response' in response:
                squad_data = response['response'][0]['players']
                return self._process_squad_data(squad_data)
            
            return []
        except Exception as e:
            print(f"Error getting Chelsea squad: {e}")
            return []
    
    def _process_squad_data(self, raw_players: List[Dict]) -> List[Dict]:
        """Process raw player data from API-Football"""
        processed_players = []
        
        for player in raw_players:
            try:
                # Extract basic information
                player_data = {
                    'player_id': str(player['id']),
                    'name': player['name'],
                    'age': player['age'],
                    'position': self._map_position(player['position']),
                    'jersey_number': player['number'],
                    'nationality': player['nationality'],
                    'is_active': True,
                    'last_updated': datetime.now().isoformat(),
                    'api_source': 'api-football'
                }
                
                # Add birth date if available
                if 'birth' in player and 'date' in player['birth']:
                    player_data['birth_date'] = player['birth']['date']
                
                # Add image URL (placeholder for now)
                player_data['image_url'] = self._get_player_image_url(player['id'])
                
                # Add fun facts (will be populated separately)
                player_data['fun_facts'] = self._get_fun_facts(player['id'])
                
                # Add transfer information (if available)
                transfer_info = self._get_transfer_info(player['id'])
                if transfer_info:
                    player_data.update(transfer_info)
                
                processed_players.append(player_data)
                
            except Exception as e:
                print(f"Error processing player {player.get('name', 'Unknown')}: {e}")
                continue
        
        return processed_players
    
    def _map_position(self, position: str) -> str:
        """Map API-Football position to our position categories"""
        position_mapping = {
            'Goalkeeper': 'GK',
            'Defender': 'DEF',
            'Midfielder': 'MID',
            'Attacker': 'FWD',
            'Forward': 'FWD'
        }
        return position_mapping.get(position, 'MID')
    
    def _get_player_image_url(self, player_id: int) -> str:
        """Get player image URL (placeholder implementation)"""
        # In a real implementation, you would:
        # 1. Check if image exists in Firebase Storage
        # 2. If not, fetch from TheSportsDB or other sources
        # 3. Upload to Firebase Storage
        return f"https://via.placeholder.com/300x400/1e40af/ffffff?text=Player+{player_id}"
    
    def _get_fun_facts(self, player_id: int) -> List[str]:
        """Get fun facts for a player (placeholder implementation)"""
        # In a real implementation, you would:
        # 1. Query additional APIs for player statistics
        # 2. Generate facts based on achievements, records, etc.
        # 3. Store curated facts in database
        return [
            "Current Chelsea FC player",
            "Part of the 2024-25 squad",
            "Professional footballer"
        ]
    
    def _get_transfer_info(self, player_id: int) -> Optional[Dict]:
        """Get transfer information for a player"""
        try:
            params = {
                'player': player_id,
                'season': 2024
            }
            
            response = self._make_request('transfers', params)
            
            if response and 'response' in response:
                transfers = response['response']
                if transfers:
                    latest_transfer = transfers[0]
                    return {
                        'signing_fee': self._format_transfer_fee(latest_transfer.get('amount', 0)),
                        'years_at_club': self._calculate_years_at_club(latest_transfer.get('date', '')),
                        'weekly_salary': self._estimate_salary(player_id)
                    }
        except Exception as e:
            print(f"Error getting transfer info for player {player_id}: {e}")
        
        return None
    
    def _format_transfer_fee(self, amount: int) -> str:
        """Format transfer fee in readable format"""
        if amount == 0:
            return "Free Transfer"
        elif amount >= 1000000:
            return f"£{amount/1000000:.1f}M"
        elif amount >= 1000:
            return f"£{amount/1000:.0f}K"
        else:
            return f"£{amount:,}"
    
    def _calculate_years_at_club(self, transfer_date: str) -> str:
        """Calculate years at club from transfer date"""
        try:
            if not transfer_date:
                return "Unknown"
            
            transfer_dt = datetime.strptime(transfer_date, '%Y-%m-%d')
            now = datetime.now()
            years = now.year - transfer_dt.year
            
            if years == 0:
                return "2024–Present"
            else:
                return f"{transfer_dt.year}–Present"
        except:
            return "Unknown"
    
    def _estimate_salary(self, player_id: int) -> str:
        """Estimate player salary (placeholder implementation)"""
        # In a real implementation, you would:
        # 1. Query salary databases
        # 2. Use market value estimates
        # 3. Apply position-based salary ranges
        return "£50,000-£100,000"  # Placeholder range
    
    def get_current_manager(self) -> Optional[Dict]:
        """Get current Chelsea manager from API-Football"""
        try:
            params = {
                'team': self.team_id,
                'season': 2024
            }
            
            response = self._make_request('coachs', params)
            
            if response and 'response' in response:
                coach_data = response['response'][0]
                return {
                    'name': coach_data['name'],
                    'age': coach_data['age'],
                    'nationality': coach_data['nationality'],
                    'photo': coach_data.get('photo', ''),
                    'last_updated': datetime.now().isoformat()
                }
        except Exception as e:
            print(f"Error getting current manager: {e}")
        
        return None
    
    def sync_all_data(self) -> Dict:
        """Sync all data from API-Football to Firebase"""
        sync_results = {
            'players_synced': 0,
            'players_errors': 0,
            'manager_synced': False,
            'manager_errors': 0,
            'sync_time': datetime.now().isoformat()
        }
        
        try:
            # Sync players
            print("Syncing Chelsea squad...")
            squad_data = self.get_chelsea_squad()
            
            for player in squad_data:
                try:
                    if firebase_service.save_player(player['player_id'], player):
                        sync_results['players_synced'] += 1
                    else:
                        sync_results['players_errors'] += 1
                except Exception as e:
                    print(f"Error saving player {player.get('name', 'Unknown')}: {e}")
                    sync_results['players_errors'] += 1
            
            # Sync manager
            print("Syncing current manager...")
            manager_data = self.get_current_manager()
            if manager_data:
                if firebase_service.save_manager(manager_data):
                    sync_results['manager_synced'] = True
                else:
                    sync_results['manager_errors'] += 1
            
            print(f"Sync completed: {sync_results['players_synced']} players, {sync_results['manager_synced']} manager")
            
        except Exception as e:
            print(f"Error during sync: {e}")
        
        return sync_results
    
    def get_player_statistics(self, player_id: int) -> Optional[Dict]:
        """Get detailed statistics for a specific player"""
        try:
            params = {
                'player': player_id,
                'season': 2024
            }
            
            response = self._make_request('players/statistics', params)
            
            if response and 'response' in response:
                return response['response'][0]
        except Exception as e:
            print(f"Error getting player statistics: {e}")
        
        return None

# Global data loader instance
data_loader = DataLoader()

