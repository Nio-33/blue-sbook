"""
Randomizer utilities for Blue's Book
Handles random player selection and fun fact generation
"""

import random
from typing import List, Dict, Optional
from datetime import datetime, timedelta

class PlayerRandomizer:
    """Utility class for random player operations"""
    
    def __init__(self):
        """Initialize randomizer"""
        self.last_random_date = None
        self.cached_random_player = None
    
    def get_random_player_of_day(self, all_players: List[Dict]) -> Optional[Dict]:
        """Get random player of the day (changes daily)"""
        if not all_players:
            return None
        
        # Check if we need to generate a new random player
        today = datetime.now().date()
        
        if (self.last_random_date != today or 
            self.cached_random_player is None):
            
            # Filter active players
            active_players = [p for p in all_players if p.get('is_active', True)]
            
            if active_players:
                self.cached_random_player = random.choice(active_players)
                self.last_random_date = today
        
        return self.cached_random_player
    
    def get_random_players(self, all_players: List[Dict], count: int = 3) -> List[Dict]:
        """Get multiple random players"""
        if not all_players:
            return []
        
        # Filter active players
        active_players = [p for p in all_players if p.get('is_active', True)]
        
        if not active_players:
            return []
        
        # Return random sample without replacement
        return random.sample(active_players, min(count, len(active_players)))
    
    def get_random_by_position(self, all_players: List[Dict], position: str) -> Optional[Dict]:
        """Get random player from specific position"""
        if not all_players:
            return None
        
        # Filter by position and active status
        position_players = [
            p for p in all_players 
            if p.get('position') == position and p.get('is_active', True)
        ]
        
        if position_players:
            return random.choice(position_players)
        
        return None
    
    def get_random_by_nationality(self, all_players: List[Dict], nationality: str) -> Optional[Dict]:
        """Get random player from specific nationality"""
        if not all_players:
            return None
        
        # Filter by nationality and active status
        nationality_players = [
            p for p in all_players 
            if p.get('nationality', '').lower() == nationality.lower() and p.get('is_active', True)
        ]
        
        if nationality_players:
            return random.choice(nationality_players)
        
        return None

class FunFactGenerator:
    """Utility class for generating fun facts about players"""
    
    def __init__(self):
        """Initialize fun fact generator"""
        self.fact_templates = {
            'debut': [
                "Made their Chelsea debut on {date}",
                "First appearance for the Blues was on {date}",
                "Debuted for Chelsea on {date}"
            ],
            'goals': [
                "Scored their first Chelsea goal on {date}",
                "First goal for the Blues came on {date}",
                "Opened their Chelsea account on {date}"
            ],
            'achievements': [
                "Won {trophy} with Chelsea",
                "Part of the {trophy} winning squad",
                "Helped Chelsea lift the {trophy}"
            ],
            'records': [
                "Holds the record for {record}",
                "Set a new Chelsea record for {record}",
                "Achieved {record} for the Blues"
            ],
            'general': [
                "Current Chelsea FC player",
                "Part of the 2024-25 squad",
                "Professional footballer for Chelsea",
                "Represents {nationality} internationally",
                "Wears the number {jersey_number} shirt"
            ]
        }
    
    def generate_fun_facts(self, player_data: Dict) -> List[str]:
        """Generate fun facts for a player"""
        facts = []
        
        # Add general facts
        general_facts = self.fact_templates['general'].copy()
        
        # Customize general facts with player data
        for i, fact in enumerate(general_facts):
            if '{nationality}' in fact and player_data.get('nationality'):
                general_facts[i] = fact.format(nationality=player_data['nationality'])
            elif '{jersey_number}' in fact and player_data.get('jersey_number'):
                general_facts[i] = fact.format(jersey_number=player_data['jersey_number'])
        
        # Select random general facts
        facts.extend(random.sample(general_facts, min(2, len(general_facts))))
        
        # Add position-specific facts
        position_facts = self._get_position_facts(player_data.get('position', ''))
        if position_facts:
            facts.append(random.choice(position_facts))
        
        # Add age-specific facts
        age_facts = self._get_age_facts(player_data.get('age', 0))
        if age_facts:
            facts.append(random.choice(age_facts))
        
        # Ensure we have at least 3 facts
        while len(facts) < 3:
            facts.append(random.choice(self.fact_templates['general']))
        
        # Limit to 5 facts maximum
        return facts[:5]
    
    def _get_position_facts(self, position: str) -> List[str]:
        """Get position-specific fun facts"""
        position_facts = {
            'GK': [
                "Goalkeeper for Chelsea FC",
                "Last line of defense for the Blues",
                "Keeps clean sheets for Chelsea"
            ],
            'DEF': [
                "Defender for Chelsea FC",
                "Protects the Chelsea goal",
                "Solid at the back for the Blues"
            ],
            'MID': [
                "Midfielder for Chelsea FC",
                "Controls the midfield for the Blues",
                "Links defense and attack for Chelsea"
            ],
            'FWD': [
                "Forward for Chelsea FC",
                "Scores goals for the Blues",
                "Leads the attack for Chelsea"
            ]
        }
        
        return position_facts.get(position, [])
    
    def _get_age_facts(self, age: int) -> List[str]:
        """Get age-specific fun facts"""
        if age < 20:
            return ["Young talent at Chelsea", "Rising star for the Blues"]
        elif age < 25:
            return ["Young player with potential", "Developing talent at Chelsea"]
        elif age < 30:
            return ["In their prime at Chelsea", "Experienced player for the Blues"]
        else:
            return ["Veteran player for Chelsea", "Experienced leader for the Blues"]

class SquadRandomizer:
    """Utility class for random squad operations"""
    
    def __init__(self):
        """Initialize squad randomizer"""
        self.formation_templates = [
            {'name': '4-3-3', 'positions': ['GK', 'DEF', 'DEF', 'DEF', 'DEF', 'MID', 'MID', 'MID', 'FWD', 'FWD', 'FWD']},
            {'name': '4-4-2', 'positions': ['GK', 'DEF', 'DEF', 'DEF', 'DEF', 'MID', 'MID', 'MID', 'MID', 'FWD', 'FWD']},
            {'name': '3-5-2', 'positions': ['GK', 'DEF', 'DEF', 'DEF', 'MID', 'MID', 'MID', 'MID', 'MID', 'FWD', 'FWD']},
            {'name': '4-2-3-1', 'positions': ['GK', 'DEF', 'DEF', 'DEF', 'DEF', 'MID', 'MID', 'MID', 'MID', 'MID', 'FWD']}
        ]
    
    def get_random_formation(self) -> Dict:
        """Get random formation template"""
        return random.choice(self.formation_templates)
    
    def create_random_squad(self, all_players: List[Dict]) -> List[Dict]:
        """Create random squad based on formation"""
        if not all_players:
            return []
        
        formation = self.get_random_formation()
        squad = []
        
        # Group players by position
        players_by_position = {}
        for player in all_players:
            if player.get('is_active', True):
                position = player.get('position', 'MID')
                if position not in players_by_position:
                    players_by_position[position] = []
                players_by_position[position].append(player)
        
        # Select players for each position in formation
        for position in formation['positions']:
            if position in players_by_position and players_by_position[position]:
                selected_player = random.choice(players_by_position[position])
                squad.append(selected_player)
        
        return squad

# Global instances
player_randomizer = PlayerRandomizer()
fun_fact_generator = FunFactGenerator()
squad_randomizer = SquadRandomizer()

