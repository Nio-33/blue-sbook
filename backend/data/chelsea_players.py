"""
Sample Chelsea FC player data for development
This will be replaced with real API data later
"""

from datetime import datetime, date
import random

# Sample Chelsea FC players data (2024/25 season)
CHELSEA_PLAYERS = [
    {
        "player_id": "1",
        "name": "Cole Palmer",
        "birth_date": "2002-05-06",
        "age": 22,
        "jersey_number": 20,
        "position": "FWD",
        "nationality": "England",
        "signing_fee": "£42.5M",
        "weekly_salary": "£75,000",
        "years_at_club": "2023–Present",
        "date_joined": "2023-09-01",
        "contract_expires": "2030-06-30",
        "height": "185cm",
        "preferred_foot": "Left",
        "international_caps": 4,
        "previous_club": "Manchester City",
        "is_academy_graduate": False,
        "major_trophies": [],
        "image_url": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=300&h=300&fit=crop&crop=face",
        "fun_facts": [
            "Scored his first Chelsea goal vs Luton Town on August 25, 2023",
            "Former Manchester City academy product",
            "Youngest player to score 20+ goals in a Premier League season for Chelsea"
        ],
        "last_updated": datetime.now().isoformat(),
        "is_active": True
    },
    {
        "player_id": "2",
        "name": "Nicolas Jackson",
        "birth_date": "2001-06-20",
        "age": 23,
        "jersey_number": 15,
        "position": "FWD",
        "nationality": "Senegal",
        "signing_fee": "£32M",
        "weekly_salary": "£65,000",
        "years_at_club": "2023–Present",
        "date_joined": "2023-07-01",
        "contract_expires": "2031-06-30",
        "height": "191cm",
        "preferred_foot": "Right",
        "international_caps": 12,
        "previous_club": "Villarreal",
        "is_academy_graduate": False,
        "major_trophies": [],
        "image_url": "https://images.unsplash.com/photo-1594736797933-d0d501283bff?w=300&h=300&fit=crop&crop=face",
        "fun_facts": [
            "Signed from Villarreal in summer 2023",
            "First Senegalese player to score for Chelsea",
            "Speaks four languages fluently"
        ],
        "last_updated": datetime.now().isoformat(),
        "is_active": True
    },
    {
        "player_id": "3",
        "name": "Enzo Fernández",
        "birth_date": "2001-01-17",
        "age": 23,
        "jersey_number": 8,
        "position": "MID",
        "nationality": "Argentina",
        "signing_fee": "£106.8M",
        "weekly_salary": "£180,000",
        "years_at_club": "2023–Present",
        "date_joined": "2023-02-01",
        "contract_expires": "2032-06-30",
        "height": "178cm",
        "preferred_foot": "Right",
        "international_caps": 29,
        "previous_club": "Benfica",
        "is_academy_graduate": False,
        "major_trophies": ["FIFA World Cup 2022"],
        "image_url": "https://images.unsplash.com/photo-1552058544-f2b08422138a?w=300&h=300&fit=crop&crop=face",
        "fun_facts": [
            "Chelsea's record signing",
            "World Cup winner with Argentina in 2022",
            "Youngest player to captain Benfica in Champions League"
        ],
        "last_updated": datetime.now().isoformat(),
        "is_active": True
    },
    {
        "player_id": "4",
        "name": "Thiago Silva",
        "birth_date": "1984-09-22",
        "age": 40,
        "jersey_number": 6,
        "position": "DEF",
        "nationality": "Brazil",
        "signing_fee": "Free Transfer",
        "weekly_salary": "£110,000",
        "years_at_club": "2020–Present",
        "date_joined": "2020-08-28",
        "contract_expires": "2024-06-30",
        "height": "183cm",
        "preferred_foot": "Right",
        "international_caps": 113,
        "previous_club": "Paris Saint-Germain",
        "is_academy_graduate": False,
        "major_trophies": ["Champions League 2021", "Copa America 2019"],
        "image_url": "https://images.unsplash.com/photo-1607081692251-5f5f5f1b1c8a?w=300&h=300&fit=crop&crop=face",
        "fun_facts": [
            "One of the oldest outfield players in Premier League",
            "Won Champions League with Chelsea in 2021",
            "Former PSG and AC Milan captain"
        ],
        "last_updated": datetime.now().isoformat(),
        "is_active": True
    },
    {
        "player_id": "5",
        "name": "Robert Sánchez",
        "birth_date": "1997-11-18",
        "age": 27,
        "jersey_number": 1,
        "position": "GK",
        "nationality": "Spain",
        "signing_fee": "£25M",
        "weekly_salary": "£85,000",
        "years_at_club": "2023–Present",
        "date_joined": "2023-08-15",
        "contract_expires": "2030-06-30",
        "height": "197cm",
        "preferred_foot": "Right",
        "international_caps": 7,
        "previous_club": "Brighton & Hove Albion",
        "is_academy_graduate": False,
        "major_trophies": [],
        "image_url": "https://images.unsplash.com/photo-1518611012118-696072aa579a?w=300&h=300&fit=crop&crop=face",
        "fun_facts": [
            "Former Brighton goalkeeper",
            "First choice for Spain national team",
            "Known for his distribution and shot-stopping ability"
        ],
        "last_updated": datetime.now().isoformat(),
        "is_active": True
    },
    {
        "player_id": "6",
        "name": "Reece James",
        "birth_date": "1999-12-08",
        "age": 25,
        "jersey_number": 24,
        "position": "DEF",
        "nationality": "England",
        "signing_fee": "Academy Graduate",
        "weekly_salary": "£150,000",
        "years_at_club": "2019–Present",
        "date_joined": "2019-07-01",
        "contract_expires": "2028-06-30",
        "height": "180cm",
        "preferred_foot": "Right",
        "international_caps": 16,
        "previous_club": "Chelsea Academy",
        "is_academy_graduate": True,
        "major_trophies": ["Champions League 2021", "UEFA Super Cup 2021"],
        "image_url": "https://images.unsplash.com/photo-1508056564-7cf2dcaa3c4b?w=300&h=300&fit=crop&crop=face",
        "fun_facts": [
            "Chelsea academy graduate and club captain",
            "One of the fastest players in the Premier League",
            "Can play as right-back or right wing-back"
        ],
        "last_updated": datetime.now().isoformat(),
        "is_active": True
    },
    {
        "player_id": "7",
        "name": "Christopher Nkunku",
        "birth_date": "1997-11-14",
        "age": 27,
        "jersey_number": 18,
        "position": "FWD",
        "nationality": "France",
        "signing_fee": "£52M",
        "weekly_salary": "£195,000",
        "years_at_club": "2023–Present",
        "date_joined": "2023-07-01",
        "contract_expires": "2029-06-30",
        "height": "175cm",
        "preferred_foot": "Right",
        "international_caps": 6,
        "previous_club": "RB Leipzig",
        "is_academy_graduate": False,
        "major_trophies": [],
        "image_url": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=300&h=300&fit=crop&crop=face",
        "fun_facts": [
            "Former RB Leipzig star striker",
            "Can play multiple positions across the front line",
            "Scored 35 goals in his final season at Leipzig"
        ],
        "last_updated": datetime.now().isoformat(),
        "is_active": True
    },
    {
        "player_id": "8",
        "name": "Moisés Caicedo",
        "birth_date": "2001-11-02",
        "age": 23,
        "jersey_number": 25,
        "position": "MID",
        "nationality": "Ecuador",
        "signing_fee": "£115M",
        "weekly_salary": "£150,000",
        "years_at_club": "2023–Present",
        "date_joined": "2023-08-14",
        "contract_expires": "2031-06-30",
        "height": "179cm",
        "preferred_foot": "Right",
        "international_caps": 43,
        "previous_club": "Brighton & Hove Albion",
        "is_academy_graduate": False,
        "major_trophies": [],
        "image_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=300&fit=crop&crop=face",
        "fun_facts": [
            "Second most expensive Chelsea signing",
            "Brighton's former record sale",
            "Youngest Ecuadorian to play in Premier League"
        ],
        "last_updated": datetime.now().isoformat(),
        "is_active": True
    },
    {
        "player_id": "9",
        "name": "Raheem Sterling",
        "birth_date": "1994-12-08",
        "age": 30,
        "jersey_number": 7,
        "position": "FWD",
        "nationality": "England",
        "signing_fee": "£47.5M",
        "weekly_salary": "£325,000",
        "years_at_club": "2022–Present",
        "date_joined": "2022-07-13",
        "contract_expires": "2027-06-30",
        "height": "170cm",
        "preferred_foot": "Right",
        "international_caps": 82,
        "previous_club": "Manchester City",
        "is_academy_graduate": False,
        "major_trophies": ["Premier League 2018", "Premier League 2019", "Premier League 2021", "Premier League 2022"],
        "image_url": "https://images.unsplash.com/photo-1560250097-0b93528c311a?w=300&h=300&fit=crop&crop=face",
        "fun_facts": [
            "Former Manchester City winger",
            "Over 100 caps for England",
            "Won 4 Premier League titles with City"
        ],
        "last_updated": datetime.now().isoformat(),
        "is_active": True
    },
    {
        "player_id": "10",
        "name": "Ben Chilwell",
        "birth_date": "1996-12-21",
        "age": 28,
        "jersey_number": 21,
        "position": "DEF",
        "nationality": "England",
        "signing_fee": "£50M",
        "weekly_salary": "£190,000",
        "years_at_club": "2020–Present",
        "date_joined": "2020-08-26",
        "contract_expires": "2027-06-30",
        "height": "178cm",
        "preferred_foot": "Left",
        "international_caps": 21,
        "previous_club": "Leicester City",
        "is_academy_graduate": False,
        "major_trophies": ["Champions League 2021", "UEFA Super Cup 2021"],
        "image_url": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=300&h=300&fit=crop&crop=face",
        "fun_facts": [
            "Former Leicester City left-back",
            "Champions League winner with Chelsea",
            "Known for his pace and attacking runs"
        ],
        "last_updated": datetime.now().isoformat(),
        "is_active": True
    }
]

# Current Chelsea manager
CHELSEA_MANAGER = {
    "manager_id": "1",
    "name": "Enzo Maresca",
    "birth_date": "1980-02-10",
    "age": 44,
    "nationality": "Italy",
    "years_at_club": "2024–Present",
    "previous_clubs": ["Leicester City", "Parma", "Manchester City (Assistant)"],
    "image_url": "https://images.unsplash.com/photo-1542909168-82c3e7fdca5c?w=300&h=300&fit=crop&crop=face",
    "achievements": [
        "Won Championship with Leicester City",
        "Former Manchester City assistant coach",
        "UEFA Pro License holder"
    ],
    "last_updated": datetime.now().isoformat(),
    "is_active": True
}

# Historical Chelsea managers
CHELSEA_MANAGERS_HISTORY = [
    {
        "manager_id": "1",
        "name": "Enzo Maresca",
        "birth_date": "1980-02-10",
        "age": 44,
        "nationality": "Italy",
        "years_at_club": "2024–Present",
        "previous_clubs": ["Leicester City", "Parma", "Manchester City (Assistant)"],
        "image_url": "https://images.unsplash.com/photo-1542909168-82c3e7fdca5c?w=300&h=300&fit=crop&crop=face",
        "achievements": [
            "Won Championship with Leicester City",
            "Former Manchester City assistant coach",
            "UEFA Pro License holder"
        ],
        "last_updated": datetime.now().isoformat(),
        "is_active": True
    },
    {
        "manager_id": "2",
        "name": "Mauricio Pochettino",
        "birth_date": "1972-03-02",
        "age": 52,
        "nationality": "Argentina",
        "years_at_club": "2023–2024",
        "previous_clubs": ["Southampton", "Tottenham Hotspur", "Paris Saint-Germain"],
        "image_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=300&fit=crop&crop=face",
        "achievements": [
            "Reached Champions League final with Tottenham",
            "Won Ligue 1 with PSG",
            "Developed young talent at multiple clubs"
        ],
        "last_updated": datetime.now().isoformat(),
        "is_active": False
    },
    {
        "manager_id": "3",
        "name": "Frank Lampard",
        "birth_date": "1978-06-20",
        "age": 46,
        "nationality": "England",
        "years_at_club": "2019–2021, 2023 (Interim)",
        "previous_clubs": ["Derby County", "Everton"],
        "image_url": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=300&h=300&fit=crop&crop=face",
        "achievements": [
            "Chelsea legend as a player",
            "Reached Champions League Round of 16",
            "Developed academy players at Chelsea"
        ],
        "last_updated": datetime.now().isoformat(),
        "is_active": False
    },
    {
        "manager_id": "4",
        "name": "Graham Potter",
        "birth_date": "1975-05-20",
        "age": 49,
        "nationality": "England",
        "years_at_club": "2022–2023",
        "previous_clubs": ["Brighton & Hove Albion", "Swansea City", "Östersunds FK"],
        "image_url": "https://images.unsplash.com/photo-1560250097-0b93528c311a?w=300&h=300&fit=crop&crop=face",
        "achievements": [
            "Led Brighton to their highest Premier League finish",
            "Known for innovative tactical approach",
            "UEFA Pro License holder"
        ],
        "last_updated": datetime.now().isoformat(),
        "is_active": False
    },
    {
        "manager_id": "5",
        "name": "Thomas Tuchel",
        "birth_date": "1973-08-29",
        "age": 51,
        "nationality": "Germany",
        "years_at_club": "2021–2022",
        "previous_clubs": ["Paris Saint-Germain", "Borussia Dortmund", "Mainz 05"],
        "image_url": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=300&h=300&fit=crop&crop=face",
        "achievements": [
            "Won Champions League with Chelsea (2021)",
            "Won FIFA Club World Cup",
            "Won UEFA Super Cup"
        ],
        "last_updated": datetime.now().isoformat(),
        "is_active": False
    },
    {
        "manager_id": "6",
        "name": "Antonio Conte",
        "birth_date": "1969-07-31",
        "age": 55,
        "nationality": "Italy",
        "years_at_club": "2016–2018",
        "previous_clubs": ["Juventus", "Italy National Team", "Inter Milan"],
        "image_url": "https://images.unsplash.com/photo-1552058544-f2b08422138a?w=300&h=300&fit=crop&crop=face",
        "achievements": [
            "Won Premier League with Chelsea (2017)",
            "Won FA Cup with Chelsea (2018)",
            "Won Serie A with Juventus (3 times)"
        ],
        "last_updated": datetime.now().isoformat(),
        "is_active": False
    },
    {
        "manager_id": "7",
        "name": "José Mourinho",
        "birth_date": "1963-01-26",
        "age": 61,
        "nationality": "Portugal",
        "years_at_club": "2004–2007, 2013–2015",
        "previous_clubs": ["Porto", "Inter Milan", "Real Madrid", "Manchester United", "Tottenham", "AS Roma"],
        "image_url": "https://images.unsplash.com/photo-1508056564-7cf2dcaa3c4b?w=300&h=300&fit=crop&crop=face",
        "achievements": [
            "Won Premier League with Chelsea (2005, 2006, 2015)",
            "Won Champions League with Porto and Inter Milan",
            "Won League Cup with Chelsea (2005, 2007, 2015)"
        ],
        "last_updated": datetime.now().isoformat(),
        "is_active": False
    },
    {
        "manager_id": "8",
        "name": "Carlo Ancelotti",
        "birth_date": "1959-06-10",
        "age": 65,
        "nationality": "Italy",
        "years_at_club": "2009–2011",
        "previous_clubs": ["AC Milan", "Real Madrid", "Bayern Munich", "Napoli", "Everton"],
        "image_url": "https://images.unsplash.com/photo-1607081692251-5f5f5f1b1c8a?w=300&h=300&fit=crop&crop=face",
        "achievements": [
            "Won Premier League with Chelsea (2010)",
            "Won FA Cup with Chelsea (2010)",
            "Won Champions League with AC Milan and Real Madrid"
        ],
        "last_updated": datetime.now().isoformat(),
        "is_active": False
    },
    {
        "manager_id": "9",
        "name": "Claudio Ranieri",
        "birth_date": "1951-10-20",
        "age": 73,
        "nationality": "Italy",
        "years_at_club": "2000–2004",
        "previous_clubs": ["Leicester City", "AS Roma", "Valencia", "Atletico Madrid", "Watford"],
        "image_url": "https://images.unsplash.com/photo-1518611012118-696072aa579a?w=300&h=300&fit=crop&crop=face",
        "achievements": [
            "Reached Champions League semi-final with Chelsea",
            "Won Premier League with Leicester City",
            "Built foundation for Chelsea's future success"
        ],
        "last_updated": datetime.now().isoformat(),
        "is_active": False
    },
    {
        "manager_id": "10",
        "name": "Gianluca Vialli",
        "birth_date": "1964-07-09",
        "age": 58,
        "nationality": "Italy",
        "years_at_club": "1998–2000",
        "previous_clubs": ["Watford (as player-manager)"],
        "image_url": "https://images.unsplash.com/photo-1594736797933-d0d501283bff?w=300&h=300&fit=crop&crop=face",
        "achievements": [
            "Won FA Cup with Chelsea (2000)",
            "Won UEFA Cup Winners' Cup (1998)",
            "Chelsea legend as both player and manager"
        ],
        "last_updated": datetime.now().isoformat(),
        "is_active": False
    }
]

def get_all_players():
    """Return all Chelsea players"""
    return CHELSEA_PLAYERS

def get_player_by_id(player_id):
    """Get a specific player by ID"""
    for player in CHELSEA_PLAYERS:
        if player["player_id"] == str(player_id):
            return player
    return None

def get_random_player():
    """Get a random player from the squad"""
    return random.choice(CHELSEA_PLAYERS)

def search_players(query):
    """Search players by name"""
    query = query.lower()
    results = []
    for player in CHELSEA_PLAYERS:
        if query in player["name"].lower():
            results.append(player)
    return results

def filter_players_by_position(position):
    """Filter players by position"""
    if not position:
        return CHELSEA_PLAYERS
    return [p for p in CHELSEA_PLAYERS if p["position"] == position]

def sort_players(players, sort_by="jersey_number"):
    """Sort players by specified field"""
    if sort_by == "jersey_number":
        return sorted(players, key=lambda x: x["jersey_number"])
    elif sort_by == "name":
        return sorted(players, key=lambda x: x["name"])
    elif sort_by == "age":
        return sorted(players, key=lambda x: x["age"])
    elif sort_by == "position":
        return sorted(players, key=lambda x: x["position"])
    return players

def get_current_manager():
    """Get current Chelsea manager"""
    return CHELSEA_MANAGER

def get_all_managers():
    """Return all Chelsea managers (historical and current)"""
    return CHELSEA_MANAGERS_HISTORY

def get_manager_by_id(manager_id):
    """Get a specific manager by ID"""
    for manager in CHELSEA_MANAGERS_HISTORY:
        if manager["manager_id"] == str(manager_id):
            return manager
    return None

def search_managers(query):
    """Search managers by name"""
    query = query.lower()
    results = []
    for manager in CHELSEA_MANAGERS_HISTORY:
        if query in manager["name"].lower():
            results.append(manager)
    return results

def get_managers_by_status(is_active=None):
    """Filter managers by active status"""
    if is_active is None:
        return CHELSEA_MANAGERS_HISTORY
    return [m for m in CHELSEA_MANAGERS_HISTORY if m["is_active"] == is_active]

# Advanced statistics calculation functions
def calculate_advanced_statistics():
    """Calculate comprehensive squad statistics"""
    players = get_all_players()
    
    stats = {
        'basic_metrics': calculate_basic_metrics(players),
        'financial_analysis': calculate_financial_analysis(players),
        'squad_demographics': calculate_squad_demographics(players),
        'tactical_analysis': calculate_tactical_analysis(players),
        'contract_timeline': calculate_contract_timeline(players),
        'performance_metrics': calculate_performance_metrics(players)
    }
    
    return stats

def calculate_basic_metrics(players):
    """Calculate enhanced basic metrics"""
    total_players = len(players)
    average_age = round(sum(p.get('age', 0) for p in players) / total_players, 1)
    nationalities = len(set(p['nationality'] for p in players))
    
    # Calculate total transfer value
    total_value = 0
    for player in players:
        if player.get('signing_fee') and '£' in player['signing_fee'] and 'Free' not in player['signing_fee'] and 'Academy' not in player['signing_fee']:
            value = float(player['signing_fee'].replace('£', '').replace('M', ''))
            total_value += value
    
    # Calculate weekly wage bill
    weekly_wages = 0
    for player in players:
        if player.get('weekly_salary'):
            wage = float(player['weekly_salary'].replace('£', '').replace(',', ''))
            weekly_wages += wage
    
    # Count academy graduates
    academy_graduates = len([p for p in players if p.get('is_academy_graduate', False)])
    
    # Count international players
    international_players = len([p for p in players if p.get('international_caps', 0) > 0])
    
    # Calculate average market value per player
    avg_market_value = round(total_value / total_players, 1) if total_players > 0 else 0
    
    return {
        'total_players': total_players,
        'average_age': average_age,
        'total_value': round(total_value, 1),
        'nationalities': nationalities,
        'academy_graduates': academy_graduates,
        'international_players': international_players,
        'weekly_wage_bill': weekly_wages,
        'avg_market_value': avg_market_value
    }

def calculate_financial_analysis(players):
    """Calculate detailed financial breakdown"""
    # Transfer spending by year
    spending_by_year = {}
    position_investment = {'GK': 0, 'DEF': 0, 'MID': 0, 'FWD': 0}
    free_transfers = 0
    paid_transfers = 0
    
    for player in players:
        # Year analysis
        if player.get('date_joined'):
            year = player['date_joined'][:4]
            if player.get('signing_fee') and '£' in player['signing_fee'] and 'Free' not in player['signing_fee'] and 'Academy' not in player['signing_fee']:
                value = float(player['signing_fee'].replace('£', '').replace('M', ''))
                spending_by_year[year] = spending_by_year.get(year, 0) + value
                position_investment[player['position']] += value
                paid_transfers += 1
            else:
                free_transfers += 1
    
    # Salary distribution
    salary_ranges = {'0-100k': 0, '100k-200k': 0, '200k+': 0}
    for player in players:
        if player.get('weekly_salary'):
            salary = float(player['weekly_salary'].replace('£', '').replace(',', ''))
            if salary <= 100000:
                salary_ranges['0-100k'] += 1
            elif salary <= 200000:
                salary_ranges['100k-200k'] += 1
            else:
                salary_ranges['200k+'] += 1
    
    return {
        'spending_by_year': spending_by_year,
        'position_investment': position_investment,
        'free_vs_paid': {'free': free_transfers, 'paid': paid_transfers},
        'salary_distribution': salary_ranges
    }

def calculate_squad_demographics(players):
    """Calculate demographic breakdown"""
    # Age distribution
    age_groups = {'20-25': 0, '25-30': 0, '30+': 0}
    for player in players:
        age = player.get('age', 0)
        if age <= 25:
            age_groups['20-25'] += 1
        elif age <= 30:
            age_groups['25-30'] += 1
        else:
            age_groups['30+'] += 1
    
    # Nationality breakdown
    nationality_breakdown = {}
    for player in players:
        nat = player['nationality']
        nationality_breakdown[nat] = nationality_breakdown.get(nat, 0) + 1
    
    # Experience levels (years at club)
    experience_levels = {'New (0-1y)': 0, 'Settled (1-3y)': 0, 'Veteran (3y+)': 0}
    for player in players:
        if player.get('date_joined'):
            years_diff = 2024 - int(player['date_joined'][:4])
            if years_diff <= 1:
                experience_levels['New (0-1y)'] += 1
            elif years_diff <= 3:
                experience_levels['Settled (1-3y)'] += 1
            else:
                experience_levels['Veteran (3y+)'] += 1
    
    return {
        'age_groups': age_groups,
        'nationality_breakdown': nationality_breakdown,
        'experience_levels': experience_levels
    }

def calculate_tactical_analysis(players):
    """Calculate tactical insights"""
    # Formation flexibility
    position_depth = {'GK': 0, 'DEF': 0, 'MID': 0, 'FWD': 0}
    for player in players:
        position_depth[player['position']] += 1
    
    # Preferred foot distribution
    foot_preference = {'Left': 0, 'Right': 0, 'Both': 0}
    for player in players:
        foot = player.get('preferred_foot', 'Right')
        foot_preference[foot] = foot_preference.get(foot, 0) + 1
    
    # Height analysis by position
    height_by_position = {}
    for player in players:
        if player.get('height'):
            pos = player['position']
            height_cm = int(player['height'].replace('cm', ''))
            if pos not in height_by_position:
                height_by_position[pos] = []
            height_by_position[pos].append(height_cm)
    
    # Calculate average height per position
    avg_height_by_position = {}
    for pos, heights in height_by_position.items():
        avg_height_by_position[pos] = round(sum(heights) / len(heights), 1)
    
    return {
        'position_depth': position_depth,
        'foot_preference': foot_preference,
        'avg_height_by_position': avg_height_by_position
    }

def calculate_contract_timeline(players):
    """Calculate contract and timeline analysis"""
    # Contract expiry timeline
    contract_years = {}
    for player in players:
        if player.get('contract_expires'):
            year = player['contract_expires'][:4]
            contract_years[year] = contract_years.get(year, 0) + 1
    
    # Squad stability (grouped by arrival periods)
    arrival_periods = {'Pre-2020': 0, '2020-2022': 0, '2023+': 0}
    for player in players:
        if player.get('date_joined'):
            year = int(player['date_joined'][:4])
            if year < 2020:
                arrival_periods['Pre-2020'] += 1
            elif year <= 2022:
                arrival_periods['2020-2022'] += 1
            else:
                arrival_periods['2023+'] += 1
    
    return {
        'contract_expiry_timeline': contract_years,
        'arrival_periods': arrival_periods
    }

def calculate_performance_metrics(players):
    """Calculate performance-based metrics"""
    # Trophy winners
    trophy_winners = 0
    total_trophies = 0
    for player in players:
        if player.get('major_trophies'):
            trophy_winners += 1
            total_trophies += len(player['major_trophies'])
    
    # International experience
    international_caps = sum(p.get('international_caps', 0) for p in players)
    avg_caps = round(international_caps / len(players), 1)
    
    # Previous club analysis
    previous_clubs = {}
    for player in players:
        if player.get('previous_club') and player['previous_club'] != 'Chelsea Academy':
            club = player['previous_club']
            previous_clubs[club] = previous_clubs.get(club, 0) + 1
    
    return {
        'trophy_winners': trophy_winners,
        'total_trophies': total_trophies,
        'international_caps': international_caps,
        'avg_international_caps': avg_caps,
        'previous_clubs': previous_clubs
    }