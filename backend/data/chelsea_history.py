"""
Comprehensive Chelsea FC Historical Database
Contains accurate facts, trophies, timelines, and achievements for AI context
"""

from datetime import datetime
from typing import Dict, List, Any

# Complete Chelsea FC Trophy Timeline (1905-2025)
CHELSEA_TROPHIES = {
    "major_trophies": {
        "premier_league": [
            {"year": "2004-05", "manager": "José Mourinho", "points": 95},
            {"year": "2005-06", "manager": "José Mourinho", "points": 91},
            {"year": "2009-10", "manager": "Carlo Ancelotti", "points": 86},
            {"year": "2014-15", "manager": "José Mourinho", "points": 87},
            {"year": "2016-17", "manager": "Antonio Conte", "points": 93},
            {"year": "2020-21", "manager": "Thomas Tuchel", "points": 67}
        ],
        "champions_league": [
            {
                "year": 2012,
                "final": "Chelsea 1-1 Bayern Munich (4-3 pens)",
                "venue": "Allianz Arena, Munich",
                "manager": "Roberto Di Matteo",
                "key_players": ["Didier Drogba", "Petr Čech", "Frank Lampard"],
                "winning_penalty": "Didier Drogba"
            },
            {
                "year": 2021,
                "final": "Chelsea 1-0 Manchester City",
                "venue": "Estádio do Dragão, Porto",
                "manager": "Thomas Tuchel",
                "scorer": "Kai Havertz",
                "key_players": ["N'Golo Kanté", "Thiago Silva", "Mason Mount"]
            }
        ],
        "fifa_club_world_cup": [
            {
                "year": 2025,
                "final": "Chelsea vs PSG",
                "venue": "TBD",
                "manager": "TBD",
                "scorers": ["TBD"],
                "significance": "Chelsea's first FIFA Club World Cup title"
            }
        ],
        "uefa_europa_league": [
            {
                "year": 2013,
                "final": "Chelsea 2-1 Benfica",
                "venue": "Amsterdam Arena",
                "manager": "Rafael Benítez",
                "scorers": ["Fernando Torres", "Branislav Ivanović"]
            },
            {
                "year": 2019,
                "final": "Chelsea 4-1 Arsenal",
                "venue": "Olympic Stadium, Baku",
                "manager": "Maurizio Sarri",
                "scorers": ["Olivier Giroud (2)", "Pedro", "Eden Hazard"]
            }
        ],
        "uefa_cup_winners_cup": [
            {"year": 1971, "final": "Chelsea 1-1, 2-1 Real Madrid", "venue": "Athens & Piraeus"},
            {"year": 1998, "final": "Chelsea 1-0 Stuttgart", "venue": "Stockholm"}
        ]
    },
    "domestic_trophies": {
        "fa_cup": [
            1970, 1997, 2000, 2007, 2009, 2010, 2012, 2018
        ],
        "league_cup": [
            1965, 1998, 2005, 2007, 2015
        ],
        "community_shield": [
            1955, 2000, 2005, 2009
        ]
    },
    "recent_achievements": {
        "last_major_trophy": {
            "trophy": "FIFA Club World Cup",
            "year": 2025,
            "date": "2025",
            "opponent": "PSG",
            "significance": "Most recent major trophy - Chelsea's first FIFA Club World Cup victory"
        },
        "last_trophy_overall": {
            "trophy": "FIFA Club World Cup",
            "year": 2025,
            "opponent": "PSG",
            "manager": "TBD"
        }
    }
}

# Key Historical Periods and Facts
CHELSEA_HISTORY = {
    "founding": {
        "year": 1905,
        "founder": "Henry Augustus Mears",
        "original_ground": "Stamford Bridge",
        "first_match": "September 2, 1905 vs Stockport County"
    },
    "eras": {
        "early_years": {
            "period": "1905-1960s",
            "highlights": ["First major trophy: League Championship 1955"]
        },
        "swinging_sixties": {
            "period": "1960s-1970s",
            "highlights": ["FA Cup 1970", "Cup Winners' Cup 1971", "First European trophy"]
        },
        "modern_era_beginning": {
            "period": "1990s-2003",
            "highlights": ["Cup Winners' Cup 1998", "FA Cup 1997, 2000"]
        },
        "abramovich_era": {
            "period": "2003-2022",
            "owner": "Roman Abramovich",
            "highlights": [
                "Transformed into global powerhouse",
                "21 major trophies",
                "Both Champions League titles",
                "5 Premier League titles",
                "Most successful period in club history"
            ]
        },
        "boehly_era": {
            "period": "2022-Present",
            "owner": "Todd Boehly consortium",
            "highlights": [
                "FIFA Club World Cup 2025 vs PSG (first trophy under new ownership)",
                "Record transfer spending",
                "Youth development focus"
            ]
        }
    },
    "stadium": {
        "name": "Stamford Bridge",
        "capacity": 40341,
        "opened": 1877,
        "address": "Fulham Road, London SW6 1HS",
        "nickname": "The Bridge"
    },
    "records": {
        "biggest_win": "Chelsea 13-0 Jeunesse Hautcharage (1971)",
        "record_signing": "Enzo Fernández (£106.8M, 2023)",
        "most_appearances": "Frank Lampard (648 appearances)",
        "top_scorer": "Frank Lampard (211 goals)",
        "longest_unbeaten_run": "40 games (2004-2005)"
    }
}

# Legendary Players by Era
CHELSEA_LEGENDS = {
    "all_time_greats": [
        {
            "name": "Frank Lampard",
            "position": "Midfielder",
            "period": "2001-2014",
            "achievements": ["Top scorer (211 goals)", "Most appearances (648)", "3 Premier League titles"],
            "significance": "Greatest Chelsea player of all time"
        },
        {
            "name": "John Terry",
            "position": "Defender",
            "period": "1998-2017",
            "achievements": ["Captain for 13 years", "5 Premier League titles", "Champions League 2012"],
            "significance": "Mr. Chelsea - ultimate club legend"
        },
        {
            "name": "Didier Drogba",
            "position": "Striker",
            "period": "2004-2012, 2014-2015",
            "achievements": ["Champions League final hero", "4 Premier League titles", "Big game player"],
            "significance": "Scored in 9 finals, ultimate clutch performer"
        },
        {
            "name": "Petr Čech",
            "position": "Goalkeeper",
            "period": "2004-2015",
            "achievements": ["Champions League 2012", "Premier League record 24 clean sheets"],
            "significance": "Greatest goalkeeper in Premier League history"
        }
    ],
    "current_stars": [
        {
            "name": "Thiago Silva",
            "position": "Defender",
            "achievements": ["Champions League 2021", "FIFA Club World Cup 2025"],
            "significance": "Leadership and experience"
        },
        {
            "name": "N'Golo Kanté",
            "position": "Midfielder", 
            "achievements": ["Champions League 2021", "World Cup 2018"],
            "significance": "Engine of the team"
        }
    ]
}

# Managerial History
CHELSEA_MANAGERS = {
    "legendary_managers": [
        {
            "name": "José Mourinho",
            "periods": ["2004-2007", "2013-2015"],
            "achievements": ["3 Premier League titles", "Unbeaten home record", "Special One era"],
            "significance": "Most successful manager in modern Chelsea history"
        },
        {
            "name": "Carlo Ancelotti",
            "period": "2009-2011",
            "achievements": ["Premier League 2009-10", "FA Cup 2010", "Double winner"],
            "significance": "Beautiful football and domestic double"
        },
        {
            "name": "Antonio Conte",
            "period": "2016-2018",
            "achievements": ["Premier League 2016-17", "FA Cup 2018", "3-4-3 formation master"],
            "significance": "Tactical revolution and Premier League record 30 wins"
        },
        {
            "name": "Thomas Tuchel",
            "period": "2021-2022",
            "achievements": ["Champions League 2021"],
            "significance": "Immediate impact - Champions League in 5 months"
        }
    ],
    "current_manager": {
        "name": "Enzo Maresca",
        "period": "2024-Present",
        "previous_club": "Leicester City",
        "style": "Possession-based football",
        "appointment_date": "June 2024"
    }
}

# Current Squad Information (2024-25)
CURRENT_SEASON = {
    "season": "2024-25",
    "manager": "Enzo Maresca",
    "league_position": "Top 6 contender",
    "key_transfers": [
        {"player": "Enzo Fernández", "fee": "£106.8M", "type": "Record signing"},
        {"player": "Mykhailo Mudryk", "fee": "£62M", "position": "Winger"},
        {"player": "Cole Palmer", "fee": "£42.5M", "position": "Forward"}
    ],
    "stadium_capacity": 40341,
    "ownership": "Todd Boehly consortium (2022-Present)"
}

def get_comprehensive_context() -> str:
    """Generate comprehensive Chelsea FC context for AI"""
    context = f"""
    COMPREHENSIVE CHELSEA FC KNOWLEDGE BASE - UPDATED {datetime.now().year}
    
    === CRITICAL RECENT FACTS ===
    - LAST MAJOR TROPHY: FIFA Club World Cup 2025 (defeated PSG)
    - This was Chelsea's FIRST FIFA Club World Cup title
    - Won in 2025 under current management
    - Historic victory against PSG in 2025
    
    === COMPLETE MAJOR TROPHY COUNT ===
    Premier League: 6 titles (2004-05, 2005-06, 2009-10, 2014-15, 2016-17, 2020-21)
    Champions League: 2 titles (2012, 2021)
    FIFA Club World Cup: 1 title (2025) ← MOST RECENT MAJOR TROPHY
    UEFA Europa League: 2 titles (2013, 2019)
    UEFA Cup Winners' Cup: 2 titles (1971, 1998)
    FA Cup: 8 titles (1970, 1997, 2000, 2007, 2009, 2010, 2012, 2018)
    League Cup: 5 titles (1965, 1998, 2005, 2007, 2015)
    
    === CURRENT INFORMATION (2024-25) ===
    Manager: Enzo Maresca (June 2024-Present)
    Stadium: Stamford Bridge (capacity: 40,341)
    Owner: Todd Boehly consortium (May 2022-Present)
    League: Premier League
    Nickname: The Blues
    Colors: Blue and White
    Founded: 1905
    
    === HISTORICAL ERAS ===
    1. Early Years (1905-1960s): Foundation and first success
    2. Swinging Sixties (1960s-70s): First European trophy (1971)
    3. Modern Revival (1990s-2003): Cup Winners' Cup 1998
    4. Abramovich Era (2003-2022): Golden period - 21 major trophies
    5. Boehly Era (2022-Present): New ownership, FIFA Club World Cup 2025 vs PSG
    
    === ACCURACY REQUIREMENTS ===
    - Always mention FIFA Club World Cup 2025 vs PSG as the most recent major trophy
    - Be precise with dates and facts
    - When unsure about recent events, acknowledge limitations
    - Cross-reference trophy counts with this database
    """
    
    return context

def get_trophy_timeline() -> List[Dict[str, Any]]:
    """Get chronological trophy timeline"""
    timeline = []
    
    # Add all trophies in chronological order
    for category, trophies in CHELSEA_TROPHIES.items():
        if isinstance(trophies, dict):
            for trophy_type, wins in trophies.items():
                if isinstance(wins, list):
                    for win in wins:
                        if isinstance(win, dict) and 'year' in win:
                            timeline.append({
                                'year': win['year'],
                                'trophy': trophy_type.replace('_', ' ').title(),
                                'details': win
                            })
                        elif isinstance(win, (int, str)):
                            timeline.append({
                                'year': win,
                                'trophy': trophy_type.replace('_', ' ').title(),
                                'details': {}
                            })
    
    # Sort by year
    timeline.sort(key=lambda x: int(str(x['year'])[:4]))
    return timeline

def verify_trophy_fact(question: str, answer: str) -> Dict[str, Any]:
    """Verify trophy-related facts against database"""
    question_lower = question.lower()
    answer_lower = answer.lower()
    
    verification = {
        "is_accurate": True,
        "corrections": [],
        "confidence": "high"
    }
    
    # Check for "last trophy" questions
    if "last" in question_lower and "trophy" in question_lower:
        if ("fifa club world cup" not in answer_lower or "2025" not in answer_lower) and not ("psg" in answer_lower or "paris saint-germain" in answer_lower):
            verification["is_accurate"] = False
            verification["corrections"].append({
                "error": "Incorrect last trophy information",
                "correction": "Chelsea's last major trophy was the FIFA Club World Cup in 2025, defeating PSG.",
                "date": "2025"
            })
    
    # Check Champions League facts
    if "champions league" in question_lower:
        if "2012" in answer_lower and "2021" not in answer_lower:
            verification["corrections"].append({
                "note": "Don't forget Chelsea won Champions League twice: 2012 AND 2021"
            })
    
    return verification