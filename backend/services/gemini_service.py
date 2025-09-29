"""
Gemini AI Service for Chelsea FC History Chat
Handles integration with Google's Gemini AI API for conversational responses
"""

import os
import json
import requests
import sys
from typing import Dict, List, Optional, Any
import logging

# Add data directory to path for importing Chelsea history
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data'))
from chelsea_history import get_comprehensive_context, verify_trophy_fact

# Import Football API service
try:
    from .football_api_service import FootballAPIService
except ImportError:
    # Handle relative import issue
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    from football_api_service import FootballAPIService

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent"
        
        # Enhanced logging for debugging
        if not self.api_key:
            logger.error("GEMINI_API_KEY not found in environment variables")
            logger.error("Please ensure your .env file contains a valid GEMINI_API_KEY")
        else:
            logger.info(f"GEMINI_API_KEY loaded successfully: {self.api_key[:10]}...")
            
        # Chelsea FC context for prompt engineering
        self.chelsea_context = self._load_chelsea_context()
        
        # Initialize Football API service for real-time data
        self.football_api = FootballAPIService()
    
    def _load_chelsea_context(self) -> str:
        """Load comprehensive Chelsea FC context for enhanced responses"""
        base_context = get_comprehensive_context()
        
        additional_instructions = """
        
        === RESPONSE GUIDELINES ===
        - ACCURACY IS PARAMOUNT: Always double-check trophy facts
        - For "last trophy" questions: ALWAYS mention FIFA Club World Cup 2025 vs PSG
        - Be specific with dates, managers, and match details
        - When discussing trophies, mention the complete count
        - If uncertain about recent events (2022+), acknowledge limitations
        - Use KTBFFH when appropriate
        - Keep responses engaging but factual (2-4 paragraphs)
        - Include specific years, venues, and key players when relevant
        
        === COMMON CORRECTIONS ===
        - Last major trophy: FIFA Club World Cup 2025 vs PSG (NOT Champions League 2021)
        - Champions League wins: 2012 AND 2021 (both important)
        - Current manager: Enzo Maresca (2024-Present)
        - Current owner: Todd Boehly consortium (2022-Present)
        
        Remember: You are the definitive source for Chelsea FC history. Accuracy builds trust with supporters!
        """
        
        return base_context + additional_instructions
    
    def _classify_query(self, user_message: str) -> Dict[str, Any]:
        """Classify query to determine if it needs real-time data"""
        message_lower = user_message.lower()
        
        # Keywords that suggest current season/real-time data needed
        current_keywords = [
            'current', 'this season', '2024', '2025', 'now', 'today', 'recent', 'last match', 
            'next match', 'upcoming', 'league position', 'table', 'standing', 'latest',
            'how is chelsea doing', 'performing this', 'recent form', 'last game',
            'next game', 'fixtures', 'current squad', 'playing today'
        ]
        
        # Keywords that suggest historical data
        historical_keywords = [
            'history', 'founded', 'trophy', 'won', 'champions league', 'premier league',
            'all time', 'ever', 'greatest', 'legendary', 'past', 'years ago',
            'first time', 'club world cup', 'mourinho', 'lampard', 'drogba'
        ]
        
        current_score = sum(1 for keyword in current_keywords if keyword in message_lower)
        historical_score = sum(1 for keyword in historical_keywords if keyword in message_lower)
        
        query_type = "current" if current_score > historical_score else "historical"
        
        # If it's current data query, try to get real-time data
        needs_real_time = query_type == "current"
        
        return {
            "type": query_type,
            "needs_real_time": needs_real_time,
            "current_score": current_score,
            "historical_score": historical_score,
            "confidence": max(current_score, historical_score) / (current_score + historical_score + 1)
        }
    
    def _get_real_time_context(self, user_message: str) -> str:
        """Get real-time Chelsea data for context enhancement"""
        if not self.football_api.is_available():
            return "\n=== REAL-TIME DATA STATUS ===\nReal-time data unavailable (API-Football key needed for current season stats)\nUsing historical data only\n"
        
        try:
            # Get comprehensive current data
            current_data = self.football_api.get_comprehensive_current_data()
            
            if not current_data.get("available", False):
                return f"\n=== REAL-TIME DATA STATUS ===\nReal-time data unavailable: {current_data.get('error', 'Unknown error')}\nUsing historical data only\n"
            
            # Format real-time context
            context_parts = ["\n=== CURRENT SEASON REAL-TIME DATA ==="]
            
            # Add current season stats
            if current_data.get("current_season", {}).get("available"):
                season_data = current_data["current_season"]
                perf = season_data.get("performance", {})
                context_parts.append(f"2024-25 Season Performance:")
                context_parts.append(f"- Matches played: {perf.get('matches_played', 0)}")
                context_parts.append(f"- Record: {perf.get('wins', 0)}W-{perf.get('draws', 0)}D-{perf.get('losses', 0)}L")
                context_parts.append(f"- Goals: {perf.get('goals_for', 0)} for, {perf.get('goals_against', 0)} against")
                context_parts.append(f"- Goal difference: {perf.get('goal_difference', 0)}")
            
            # Add league position
            if current_data.get("league_position", {}).get("available"):
                position_data = current_data["league_position"]["chelsea_position"]
                if position_data:
                    context_parts.append(f"Current Premier League Position: {position_data.get('position')}th")
                    context_parts.append(f"Points: {position_data.get('points')}")
                    context_parts.append(f"Recent form: {position_data.get('form', 'N/A')}")
            
            # Add recent matches
            if current_data.get("recent_matches", {}).get("available"):
                recent = current_data["recent_matches"]["matches"][:2]  # Last 2 matches
                context_parts.append("Recent Results:")
                for match in recent:
                    opponent = match.get("opponent", "Unknown")
                    score = match.get("score", "N/A")
                    result = match.get("result", "unknown").upper()
                    context_parts.append(f"- vs {opponent}: {score} ({result})")
            
            # Add upcoming fixtures
            if current_data.get("upcoming_fixtures", {}).get("available"):
                upcoming = current_data["upcoming_fixtures"]["matches"][:1]  # Next match
                context_parts.append("Next Fixture:")
                for match in upcoming:
                    opponent = match.get("opponent", "Unknown")
                    date = match.get("date", "TBD")
                    home_away = match.get("home_away", "unknown")
                    context_parts.append(f"- vs {opponent} ({home_away}) - {date}")
            
            context_parts.append(f"Data last updated: {current_data.get('data_timestamp', 'Unknown')}")
            context_parts.append("=== END REAL-TIME DATA ===\n")
            
            return "\n".join(context_parts)
            
        except Exception as e:
            logger.error(f"Error getting real-time context: {str(e)}")
            return f"\n=== REAL-TIME DATA ERROR ===\nFailed to fetch current data: {str(e)}\nUsing historical data only\n"
    
    def generate_response(self, user_message: str, chat_history: Optional[List[Dict]] = None) -> Dict:
        """
        Generate AI response using Gemini AI with smart data routing
        
        Args:
            user_message: User's question/message
            chat_history: Previous conversation context
            
        Returns:
            Dict with response data or error information
        """
        if not self.api_key:
            logger.error("Attempted to generate response without API key")
            return {
                'success': False,
                'error': 'Gemini API key not configured',
                'message': "I'm sorry, but the AI chat service is not currently available. The Gemini API key is not configured. Please check the server configuration.",
                'debug_info': {
                    'api_key_present': False,
                    'env_var_name': 'GEMINI_API_KEY'
                }
            }
        
        try:
            # Classify the query to determine data needs
            query_classification = self._classify_query(user_message)
            
            # Get real-time context if needed
            real_time_context = ""
            if query_classification["needs_real_time"]:
                real_time_context = self._get_real_time_context(user_message)
            
            # Prepare the prompt with enhanced context
            prompt = self._build_prompt(user_message, chat_history, real_time_context, query_classification)
            
            # Prepare request payload
            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "candidateCount": 1,
                    "maxOutputTokens": 500,
                    "topP": 0.8,
                    "topK": 10
                }
            }
            
            # Make API request
            headers = {
                'Content-Type': 'application/json',
                'x-goog-api-key': self.api_key
            }
            
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract response text
                if 'candidates' in data and len(data['candidates']) > 0:
                    candidate = data['candidates'][0]
                    if 'content' in candidate and 'parts' in candidate['content']:
                        ai_response = candidate['content']['parts'][0]['text']
                        
                        # Validate response for factual accuracy
                        validation = self._validate_response(user_message, ai_response)
                        
                        response_data = {
                            'success': True,
                            'message': ai_response.strip(),
                            'metadata': {
                                'model': 'gemini-2.0-flash-exp',
                                'prompt_tokens': len(prompt.split()),
                                'response_tokens': len(ai_response.split()),
                                'validation': validation,
                                'query_classification': query_classification,
                                'used_real_time_data': bool(real_time_context),
                                'api_football_available': self.football_api.is_available()
                            }
                        }
                        
                        # If validation found critical errors, add warning
                        if not validation.get('is_accurate', True):
                            response_data['warning'] = "Response may contain outdated information"
                            logger.warning(f"Potential factual errors detected: {validation.get('corrections', [])}")
                        
                        return response_data
                
                return {
                    'success': False,
                    'error': 'Invalid response format from Gemini API',
                    'message': "I'm sorry, I couldn't generate a proper response. Please try again."
                }
            
            else:
                logger.error(f"Gemini API error: {response.status_code} - {response.text}")
                return {
                    'success': False,
                    'error': f'API request failed with status {response.status_code}',
                    'message': "I'm experiencing technical difficulties. Please try again in a moment."
                }
                
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'Request timeout',
                'message': "The request took too long. Please try again."
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {str(e)}")
            return {
                'success': False,
                'error': f'Request failed: {str(e)}',
                'message': "I'm having trouble connecting to the AI service. Please try again."
            }
            
        except Exception as e:
            logger.error(f"Unexpected error in Gemini service: {str(e)}")
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}',
                'message': "Something went wrong. Please try again."
            }
    
    def _build_prompt(self, user_message: str, chat_history: Optional[List[Dict]] = None, 
                     real_time_context: str = "", query_classification: Optional[Dict] = None) -> str:
        """Build the complete prompt with context, real-time data, and history"""
        
        prompt_parts = [self.chelsea_context]
        
        # Add real-time context if available
        if real_time_context:
            prompt_parts.append(real_time_context)
        
        # Add query classification guidance
        if query_classification:
            query_type = query_classification.get("type", "unknown")
            prompt_parts.append(f"\n=== QUERY ANALYSIS ===")
            prompt_parts.append(f"Query type: {query_type}")
            if query_type == "current":
                prompt_parts.append("Focus on current season data and real-time information when available")
            else:
                prompt_parts.append("Focus on historical facts and comprehensive club heritage")
            prompt_parts.append("=== END ANALYSIS ===\n")
        
        # Add chat history for context
        if chat_history:
            prompt_parts.append("Previous conversation:")
            for msg in chat_history[-5:]:  # Only include last 5 messages
                role = "User" if msg.get('type') == 'user' else "Assistant"
                prompt_parts.append(f"{role}: {msg.get('message', '')}")
        
        # Add current user message
        prompt_parts.append(f"\nUser: {user_message}")
        prompt_parts.append("\nAssistant:")
        
        return "\n".join(prompt_parts)
    
    def get_suggested_questions(self) -> List[str]:
        """Return a list of suggested questions about Chelsea FC"""
        return [
            "When was Chelsea FC founded and by whom?",
            "Tell me about Chelsea's Champions League victories",
            "Who are Chelsea's greatest managers in history?",
            "What is the history of Stamford Bridge stadium?",
            "Who are the top goalscorers in Chelsea's history?",
            "Tell me about the Roman Abramovich era at Chelsea",
            "What trophies has Chelsea won?",
            "Who were the key players in Chelsea's 2012 Champions League win?",
            "What is the significance of 'KTBFFH' for Chelsea fans?",
            "Tell me about Chelsea's academy and youth development"
        ]
    
    def _validate_response(self, user_message: str, ai_response: str) -> Dict:
        """Validate AI response for factual accuracy"""
        try:
            return verify_trophy_fact(user_message, ai_response)
        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            return {"is_accurate": True, "corrections": [], "confidence": "unknown"}
    
    def validate_api_key(self) -> bool:
        """Validate if the Gemini API key is working"""
        if not self.api_key:
            return False
            
        try:
            test_response = self.generate_response("Hello")
            return test_response.get('success', False)
        except:
            return False