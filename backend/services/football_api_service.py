"""
API-Football Service for Real-Time Chelsea FC Data
Provides current season statistics, live match data, and real-time information
"""

import os
import requests
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

# Import cache service
try:
    from .cache_service import api_football_cache
except ImportError:
    import sys
    sys.path.append(os.path.dirname(__file__))
    from cache_service import api_football_cache

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FootballAPIService:
    def __init__(self):
        self.api_key = os.getenv('API_FOOTBALL_KEY')
        self.base_url = os.getenv('API_FOOTBALL_URL', 'https://api-football-v1.p.rapidapi.com/v3')
        self.chelsea_team_id = 40  # Chelsea FC team ID in API-Football
        
        # Headers for API requests
        self.headers = {
            'X-RapidAPI-Key': self.api_key,
            'X-RapidAPI-Host': 'api-football-v1.p.rapidapi.com'
        }
        
        if not self.api_key or self.api_key == 'your-api-football-key-here':
            logger.warning("API_FOOTBALL_KEY not found or not configured")
            
        # Current season (2024-25 Premier League)
        self.current_season = 2024
        self.premier_league_id = 39
        
    def is_available(self) -> bool:
        """Check if API-Football service is available"""
        return bool(self.api_key and self.api_key != 'your-api-football-key-here')
    
    def get_current_season_stats(self) -> Dict[str, Any]:
        """Get Chelsea's current season statistics with caching"""
        cache_key = f"chelsea_stats_{self.current_season}"
        
        # Try cache first
        cached_data = api_football_cache.get(cache_key)
        if cached_data:
            cached_data['from_cache'] = True
            return cached_data
        
        if not self.is_available():
            return {"error": "API-Football service not available", "available": False}
            
        try:
            # Get team statistics for current season
            url = f"{self.base_url}/teams/statistics"
            params = {
                'league': self.premier_league_id,
                'season': self.current_season,
                'team': self.chelsea_team_id
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                result = self._format_team_stats(data.get('response', {}))
                
                # Cache successful response for 30 minutes
                if result.get('available'):
                    api_football_cache.set(cache_key, result, ttl=1800)
                
                return result
            else:
                logger.error(f"API-Football team stats error: {response.status_code}")
                return {"error": f"API request failed with status {response.status_code}", "available": False}
                
        except requests.exceptions.RequestException as e:
            logger.error(f"API-Football request error: {str(e)}")
            return {"error": f"Request failed: {str(e)}", "available": False}
            
    def get_recent_matches(self, limit: int = 5) -> Dict[str, Any]:
        """Get Chelsea's recent match results"""
        if not self.is_available():
            return {"error": "API-Football service not available", "available": False}
            
        try:
            url = f"{self.base_url}/fixtures"
            params = {
                'team': self.chelsea_team_id,
                'last': limit,
                'timezone': 'Europe/London'
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._format_recent_matches(data.get('response', []))
            else:
                logger.error(f"API-Football recent matches error: {response.status_code}")
                return {"error": f"API request failed with status {response.status_code}", "available": False}
                
        except requests.exceptions.RequestException as e:
            logger.error(f"API-Football request error: {str(e)}")
            return {"error": f"Request failed: {str(e)}", "available": False}
    
    def get_next_matches(self, limit: int = 3) -> Dict[str, Any]:
        """Get Chelsea's upcoming fixtures"""
        if not self.is_available():
            return {"error": "API-Football service not available", "available": False}
            
        try:
            url = f"{self.base_url}/fixtures"
            params = {
                'team': self.chelsea_team_id,
                'next': limit,
                'timezone': 'Europe/London'
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._format_upcoming_matches(data.get('response', []))
            else:
                logger.error(f"API-Football upcoming matches error: {response.status_code}")
                return {"error": f"API request failed with status {response.status_code}", "available": False}
                
        except requests.exceptions.RequestException as e:
            logger.error(f"API-Football request error: {str(e)}")
            return {"error": f"Request failed: {str(e)}", "available": False}
    
    def get_league_standings(self) -> Dict[str, Any]:
        """Get current Premier League table with Chelsea's position"""
        if not self.is_available():
            return {"error": "API-Football service not available", "available": False}
            
        try:
            url = f"{self.base_url}/standings"
            params = {
                'league': self.premier_league_id,
                'season': self.current_season
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._format_league_standings(data.get('response', []))
            else:
                logger.error(f"API-Football standings error: {response.status_code}")
                return {"error": f"API request failed with status {response.status_code}", "available": False}
                
        except requests.exceptions.RequestException as e:
            logger.error(f"API-Football request error: {str(e)}")
            return {"error": f"Request failed: {str(e)}", "available": False}
    
    def get_current_squad_stats(self) -> Dict[str, Any]:
        """Get current squad with this season's player statistics"""
        if not self.is_available():
            return {"error": "API-Football service not available", "available": False}
            
        try:
            url = f"{self.base_url}/players"
            params = {
                'team': self.chelsea_team_id,
                'season': self.current_season,
                'league': self.premier_league_id
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._format_squad_stats(data.get('response', []))
            else:
                logger.error(f"API-Football squad stats error: {response.status_code}")
                return {"error": f"API request failed with status {response.status_code}", "available": False}
                
        except requests.exceptions.RequestException as e:
            logger.error(f"API-Football request error: {str(e)}")
            return {"error": f"Request failed: {str(e)}", "available": False}
    
    def _format_team_stats(self, data: Dict) -> Dict[str, Any]:
        """Format team statistics response"""
        if not data:
            return {"available": False, "error": "No data available"}
            
        try:
            team_info = data.get('team', {})
            league_info = data.get('league', {})
            fixtures = data.get('fixtures', {})
            goals = data.get('goals', {})
            
            return {
                "available": True,
                "team": {
                    "name": team_info.get('name', 'Chelsea'),
                    "founded": team_info.get('founded'),
                    "venue": team_info.get('venue', {}).get('name', 'Stamford Bridge')
                },
                "season": {
                    "year": league_info.get('season'),
                    "league": league_info.get('name', 'Premier League')
                },
                "performance": {
                    "matches_played": fixtures.get('played', {}).get('total', 0),
                    "wins": fixtures.get('wins', {}).get('total', 0),
                    "draws": fixtures.get('draws', {}).get('total', 0),
                    "losses": fixtures.get('loses', {}).get('total', 0),
                    "goals_for": goals.get('for', {}).get('total', {}).get('total', 0),
                    "goals_against": goals.get('against', {}).get('total', {}).get('total', 0),
                    "goal_difference": goals.get('for', {}).get('total', {}).get('total', 0) - goals.get('against', {}).get('total', {}).get('total', 0)
                },
                "form": data.get('form', ''),
                "last_updated": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error formatting team stats: {str(e)}")
            return {"available": False, "error": "Data formatting error"}
    
    def _format_recent_matches(self, matches: List) -> Dict[str, Any]:
        """Format recent matches response"""
        if not matches:
            return {"available": False, "error": "No recent matches available"}
            
        try:
            formatted_matches = []
            for match in matches[:5]:  # Last 5 matches
                fixture = match.get('fixture', {})
                teams = match.get('teams', {})
                goals = match.get('goals', {})
                
                formatted_matches.append({
                    "date": fixture.get('date'),
                    "opponent": teams.get('away', {}).get('name') if teams.get('home', {}).get('id') == self.chelsea_team_id else teams.get('home', {}).get('name'),
                    "home_away": "home" if teams.get('home', {}).get('id') == self.chelsea_team_id else "away",
                    "score": f"{goals.get('home', 0)}-{goals.get('away', 0)}",
                    "result": self._determine_result(match),
                    "venue": fixture.get('venue', {}).get('name'),
                    "competition": match.get('league', {}).get('name')
                })
            
            return {
                "available": True,
                "matches": formatted_matches,
                "total": len(formatted_matches),
                "last_updated": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error formatting recent matches: {str(e)}")
            return {"available": False, "error": "Data formatting error"}
    
    def _format_upcoming_matches(self, matches: List) -> Dict[str, Any]:
        """Format upcoming matches response"""
        if not matches:
            return {"available": False, "error": "No upcoming matches available"}
            
        try:
            formatted_matches = []
            for match in matches[:3]:  # Next 3 matches
                fixture = match.get('fixture', {})
                teams = match.get('teams', {})
                
                formatted_matches.append({
                    "date": fixture.get('date'),
                    "opponent": teams.get('away', {}).get('name') if teams.get('home', {}).get('id') == self.chelsea_team_id else teams.get('home', {}).get('name'),
                    "home_away": "home" if teams.get('home', {}).get('id') == self.chelsea_team_id else "away",
                    "venue": fixture.get('venue', {}).get('name'),
                    "competition": match.get('league', {}).get('name'),
                    "status": fixture.get('status', {}).get('long', 'Scheduled')
                })
            
            return {
                "available": True,
                "matches": formatted_matches,
                "total": len(formatted_matches),
                "last_updated": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error formatting upcoming matches: {str(e)}")
            return {"available": False, "error": "Data formatting error"}
    
    def _format_league_standings(self, standings_data: List) -> Dict[str, Any]:
        """Format league standings with focus on Chelsea's position"""
        if not standings_data:
            return {"available": False, "error": "No standings data available"}
            
        try:
            # Find Chelsea in the standings
            chelsea_position = None
            total_teams = 0
            
            for league in standings_data:
                for standing in league.get('league', {}).get('standings', []):
                    total_teams = len(standing)
                    for team in standing:
                        if team.get('team', {}).get('id') == self.chelsea_team_id:
                            chelsea_position = {
                                "position": team.get('rank'),
                                "points": team.get('points'),
                                "played": team.get('all', {}).get('played', 0),
                                "wins": team.get('all', {}).get('win', 0),
                                "draws": team.get('all', {}).get('draw', 0),
                                "losses": team.get('all', {}).get('lose', 0),
                                "goals_for": team.get('all', {}).get('goals', {}).get('for', 0),
                                "goals_against": team.get('all', {}).get('goals', {}).get('against', 0),
                                "goal_difference": team.get('goalsDiff', 0),
                                "form": team.get('form', '')
                            }
                            break
            
            return {
                "available": True,
                "chelsea_position": chelsea_position,
                "league": "Premier League",
                "season": self.current_season,
                "total_teams": total_teams,
                "last_updated": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error formatting league standings: {str(e)}")
            return {"available": False, "error": "Data formatting error"}
    
    def _format_squad_stats(self, players_data: List) -> Dict[str, Any]:
        """Format current squad statistics"""
        if not players_data:
            return {"available": False, "error": "No squad data available"}
            
        try:
            formatted_players = []
            top_scorers = []
            
            for player_data in players_data:
                player = player_data.get('player', {})
                statistics = player_data.get('statistics', [{}])[0] if player_data.get('statistics') else {}
                games = statistics.get('games', {})
                goals = statistics.get('goals', {})
                
                player_info = {
                    "name": player.get('name'),
                    "age": player.get('age'),
                    "position": statistics.get('games', {}).get('position'),
                    "appearances": games.get('appearences', 0),
                    "goals": goals.get('total') or 0,
                    "assists": statistics.get('goals', {}).get('assists') or 0,
                    "minutes_played": games.get('minutes') or 0
                }
                
                formatted_players.append(player_info)
                
                # Track top scorers
                if player_info["goals"] > 0:
                    top_scorers.append({
                        "name": player_info["name"],
                        "goals": player_info["goals"],
                        "position": player_info["position"]
                    })
            
            # Sort top scorers
            top_scorers.sort(key=lambda x: x["goals"], reverse=True)
            
            return {
                "available": True,
                "squad_size": len(formatted_players),
                "top_scorers": top_scorers[:5],
                "season": self.current_season,
                "last_updated": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error formatting squad stats: {str(e)}")
            return {"available": False, "error": "Data formatting error"}
    
    def _determine_result(self, match: Dict) -> str:
        """Determine match result from Chelsea's perspective"""
        try:
            teams = match.get('teams', {})
            goals = match.get('goals', {})
            
            chelsea_is_home = teams.get('home', {}).get('id') == self.chelsea_team_id
            home_goals = goals.get('home', 0)
            away_goals = goals.get('away', 0)
            
            if chelsea_is_home:
                if home_goals > away_goals:
                    return "win"
                elif home_goals < away_goals:
                    return "loss"
                else:
                    return "draw"
            else:
                if away_goals > home_goals:
                    return "win"
                elif away_goals < home_goals:
                    return "loss"
                else:
                    return "draw"
        except:
            return "unknown"
    
    def get_comprehensive_current_data(self) -> Dict[str, Any]:
        """Get all current Chelsea data in one call"""
        if not self.is_available():
            return {
                "available": False,
                "error": "API-Football service not available - API key not configured",
                "note": "Using historical data only"
            }
        
        try:
            # Get all current data
            current_stats = self.get_current_season_stats()
            recent_matches = self.get_recent_matches(3)
            next_matches = self.get_next_matches(2)
            league_position = self.get_league_standings()
            
            return {
                "available": True,
                "current_season": current_stats,
                "recent_matches": recent_matches,
                "upcoming_fixtures": next_matches,
                "league_position": league_position,
                "data_timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting comprehensive data: {str(e)}")
            return {
                "available": False,
                "error": f"Failed to fetch current data: {str(e)}"
            }