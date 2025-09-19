"""
Formatting utilities for Blue's Book
Handles data formatting and response structure
"""

from typing import Dict, Any, Optional
from datetime import datetime
import re

def format_player_response(player_data: Dict[str, Any], detailed: bool = False) -> Dict[str, Any]:
    """Format player data for API response"""
    if not player_data:
        return {}
    
    # Basic player information
    formatted = {
        'player_id': player_data.get('player_id', ''),
        'name': player_data.get('name', ''),
        'age': player_data.get('age', 0),
        'position': player_data.get('position', ''),
        'jersey_number': player_data.get('jersey_number', 0),
        'nationality': player_data.get('nationality', ''),
        'image_url': player_data.get('image_url', ''),
        'is_active': player_data.get('is_active', True)
    }
    
    # Add detailed information if requested
    if detailed:
        formatted.update({
            'birth_date': player_data.get('birth_date', ''),
            'signing_fee': player_data.get('signing_fee', 'Unknown'),
            'weekly_salary': player_data.get('weekly_salary', 'Unknown'),
            'years_at_club': player_data.get('years_at_club', 'Unknown'),
            'fun_facts': player_data.get('fun_facts', []),
            'last_updated': player_data.get('last_updated', ''),
            'api_source': player_data.get('api_source', 'unknown')
        })
    
    return formatted

def format_manager_response(manager_data: Dict[str, Any]) -> Dict[str, Any]:
    """Format manager data for API response"""
    if not manager_data:
        return {}
    
    return {
        'name': manager_data.get('name', ''),
        'age': manager_data.get('age', 0),
        'nationality': manager_data.get('nationality', ''),
        'photo': manager_data.get('photo', ''),
        'last_updated': manager_data.get('last_updated', '')
    }

def format_search_result(data: Dict[str, Any], result_type: str) -> Dict[str, Any]:
    """Format search result data"""
    if result_type == 'player':
        return {
            'id': data.get('player_id', ''),
            'name': data.get('name', ''),
            'type': 'player',
            'position': data.get('position', ''),
            'jersey_number': data.get('jersey_number', 0),
            'image_url': data.get('image_url', ''),
            'nationality': data.get('nationality', '')
        }
    elif result_type == 'manager':
        return {
            'id': 'current_manager',
            'name': data.get('name', ''),
            'type': 'manager',
            'nationality': data.get('nationality', ''),
            'photo': data.get('photo', '')
        }
    else:
        return data

def format_transfer_fee(amount: int) -> str:
    """Format transfer fee in readable format"""
    if amount == 0:
        return "Free Transfer"
    elif amount >= 1000000:
        return f"£{amount/1000000:.1f}M"
    elif amount >= 1000:
        return f"£{amount/1000:.0f}K"
    else:
        return f"£{amount:,}"

def format_salary_range(min_salary: int, max_salary: int) -> str:
    """Format salary range"""
    if min_salary == max_salary:
        return f"£{min_salary:,}"
    else:
        return f"£{min_salary:,}-£{max_salary:,}"

def format_date(date_string: str) -> str:
    """Format date string for display"""
    if not date_string:
        return "Unknown"
    
    try:
        # Try to parse various date formats
        date_formats = [
            '%Y-%m-%d',
            '%d/%m/%Y',
            '%m/%d/%Y',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%dT%H:%M:%SZ'
        ]
        
        for fmt in date_formats:
            try:
                dt = datetime.strptime(date_string, fmt)
                return dt.strftime('%B %d, %Y')
            except ValueError:
                continue
        
        return date_string
    except:
        return "Unknown"

def format_years_at_club(start_date: str, end_date: str = None) -> str:
    """Format years at club string"""
    if not start_date:
        return "Unknown"
    
    try:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        start_year = start_dt.year
        
        if end_date:
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            end_year = end_dt.year
            return f"{start_year}–{end_year}"
        else:
            return f"{start_year}–Present"
    except:
        return "Unknown"

def format_position_display(position: str) -> str:
    """Format position for display"""
    position_map = {
        'GK': 'Goalkeeper',
        'DEF': 'Defender',
        'MID': 'Midfielder',
        'FWD': 'Forward'
    }
    return position_map.get(position, position)

def format_fun_fact(fact: str) -> str:
    """Format fun fact for display"""
    if not fact:
        return ""
    
    # Capitalize first letter
    fact = fact.strip()
    if fact:
        fact = fact[0].upper() + fact[1:]
    
    # Ensure it ends with a period
    if not fact.endswith(('.', '!', '?')):
        fact += '.'
    
    return fact

def format_api_response(success: bool, data: Any = None, error: str = None, 
                       query_time: str = None, **kwargs) -> Dict[str, Any]:
    """Format standard API response"""
    response = {
        'success': success,
        'timestamp': datetime.now().isoformat()
    }
    
    if success:
        response['data'] = data
        if query_time:
            response['query_time'] = query_time
    else:
        response['error'] = error or 'Unknown error'
    
    # Add any additional fields
    response.update(kwargs)
    
    return response

def format_error_response(error_message: str, error_code: int = 500) -> tuple:
    """Format error response with status code"""
    return {
        'success': False,
        'error': error_message,
        'timestamp': datetime.now().isoformat()
    }, error_code

