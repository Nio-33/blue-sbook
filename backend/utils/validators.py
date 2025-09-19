"""
Validation utilities for Blue's Book
Handles input validation and sanitization
"""

from typing import Dict, Any, Optional
import re

def validate_player_filters(filters: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and sanitize player filter parameters"""
    validated_filters = {}
    
    # Validate position filter
    if 'position' in filters and filters['position']:
        position = filters['position'].upper()
        valid_positions = ['GK', 'DEF', 'MID', 'FWD']
        if position in valid_positions:
            validated_filters['position'] = position
    
    # Validate is_active filter
    if 'is_active' in filters:
        if isinstance(filters['is_active'], bool):
            validated_filters['is_active'] = filters['is_active']
        elif isinstance(filters['is_active'], str):
            validated_filters['is_active'] = filters['is_active'].lower() == 'true'
    
    return validated_filters

def validate_search_query(query: str) -> bool:
    """Validate search query parameters"""
    if not query or not isinstance(query, str):
        return False
    
    # Check minimum length
    if len(query.strip()) < 2:
        return False
    
    # Check for potentially malicious content
    if re.search(r'[<>"\']', query):
        return False
    
    return True

def validate_player_data(player_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate player data before saving"""
    validated_data = {}
    
    # Required fields
    required_fields = ['name', 'position', 'jersey_number', 'nationality']
    for field in required_fields:
        if field in player_data and player_data[field]:
            validated_data[field] = str(player_data[field]).strip()
    
    # Validate position
    if 'position' in validated_data:
        position = validated_data['position'].upper()
        valid_positions = ['GK', 'DEF', 'MID', 'FWD']
        if position not in valid_positions:
            validated_data['position'] = 'MID'  # Default fallback
    
    # Validate jersey number
    if 'jersey_number' in validated_data:
        try:
            jersey_num = int(validated_data['jersey_number'])
            if 1 <= jersey_num <= 99:
                validated_data['jersey_number'] = jersey_num
            else:
                validated_data['jersey_number'] = 0
        except (ValueError, TypeError):
            validated_data['jersey_number'] = 0
    
    # Validate age
    if 'age' in player_data:
        try:
            age = int(player_data['age'])
            if 16 <= age <= 50:
                validated_data['age'] = age
        except (ValueError, TypeError):
            pass
    
    # Optional fields
    optional_fields = ['birth_date', 'image_url', 'signing_fee', 'weekly_salary', 'years_at_club']
    for field in optional_fields:
        if field in player_data and player_data[field]:
            validated_data[field] = str(player_data[field]).strip()
    
    # Validate fun facts
    if 'fun_facts' in player_data and isinstance(player_data['fun_facts'], list):
        fun_facts = []
        for fact in player_data['fun_facts']:
            if isinstance(fact, str) and len(fact.strip()) > 0:
                fun_facts.append(fact.strip())
        if fun_facts:
            validated_data['fun_facts'] = fun_facts
    
    # Set defaults
    validated_data['is_active'] = player_data.get('is_active', True)
    validated_data['last_updated'] = player_data.get('last_updated', '')
    
    return validated_data

def validate_manager_data(manager_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate manager data before saving"""
    validated_data = {}
    
    # Required fields
    required_fields = ['name', 'nationality']
    for field in required_fields:
        if field in manager_data and manager_data[field]:
            validated_data[field] = str(manager_data[field]).strip()
    
    # Optional fields
    optional_fields = ['age', 'photo']
    for field in optional_fields:
        if field in manager_data and manager_data[field]:
            validated_data[field] = str(manager_data[field]).strip()
    
    # Validate age
    if 'age' in manager_data:
        try:
            age = int(manager_data['age'])
            if 25 <= age <= 80:
                validated_data['age'] = age
        except (ValueError, TypeError):
            pass
    
    # Set defaults
    validated_data['last_updated'] = manager_data.get('last_updated', '')
    
    return validated_data

def sanitize_string(input_string: str) -> str:
    """Sanitize string input to prevent XSS and other attacks"""
    if not isinstance(input_string, str):
        return ""
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\']', '', input_string)
    
    # Limit length
    return sanitized[:500]

def validate_pagination_params(page: int, limit: int) -> tuple:
    """Validate pagination parameters"""
    # Ensure page is at least 1
    page = max(1, page) if isinstance(page, int) else 1
    
    # Ensure limit is between 1 and 100
    if isinstance(limit, int):
        limit = max(1, min(100, limit))
    else:
        limit = 20
    
    return page, limit

