"""
Service to interact with Clash of Clans official API
https://developer.clashofclans.com/
"""
import requests
from typing import Dict, Any, Optional
import json
from datetime import datetime
import os

# Clash of Clans API
COC_API_BASE = "https://api.clashofclans.com/v1"
COC_API_KEY = os.getenv("COC_API_KEY", "")  # Set in .env file


class ClashOfClansService:
    """Service to fetch and manage Clash of Clans account data"""
    
    @staticmethod
    def _get_headers() -> Dict[str, str]:
        """Get headers for API requests"""
        return {
            "Authorization": f"Bearer {COC_API_KEY}",
            "Accept": "application/json"
        }
    
    @staticmethod
    def get_player_data(player_tag: str) -> Optional[Dict[str, Any]]:
        """
        Fetch player data from Clash of Clans API
        
        Args:
            player_tag: Player tag (e.g., #P92VQC8UG)
            
        Returns:
            Dictionary with player data or mock data if demo mode
        """
        try:
            # Validate player tag format
            if not player_tag.startswith("#"):
                player_tag = "#" + player_tag
            
            # Encode player tag for URL
            encoded_tag = player_tag.replace("#", "%23")
            
            # If API key is not set, use mock data
            if not COC_API_KEY:
                return ClashOfClansService._get_mock_player_data(player_tag)
            
            # Make API request
            url = f"{COC_API_BASE}/players/{encoded_tag}"
            headers = ClashOfClansService._get_headers()
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return ClashOfClansService._parse_player_data(data)
            elif response.status_code == 404:
                return None
            else:
                # Fallback to mock data on error
                return ClashOfClansService._get_mock_player_data(player_tag)
                
        except Exception as e:
            print(f"Error fetching player data: {e}")
            return ClashOfClansService._get_mock_player_data(player_tag)
    
    @staticmethod
    def _parse_player_data(api_response: Dict[str, Any]) -> Dict[str, Any]:
        """Parse API response and extract relevant stats"""
        try:
            clan_info = None
            if "clan" in api_response and api_response["clan"]:
                clan_info = {
                    "name": api_response["clan"].get("name", "N/A"),
                    "tag": api_response["clan"].get("tag", ""),
                    "badge_url": api_response["clan"].get("badgeUrls", {}).get("large", "")
                }
            
            return {
                "name": api_response.get("name", "Unknown"),
                "player_tag": api_response.get("tag", ""),
                "town_hall_level": api_response.get("townHallLevel", 0),
                "exp_level": api_response.get("expLevel", 0),
                "trophies": api_response.get("trophies", 0),
                "best_trophies": api_response.get("bestTrophies", 0),
                "war_stars": api_response.get("warStars", 0),
                "attack_wins": api_response.get("attackWins", 0),
                "defense_wins": api_response.get("defenseWins", 0),
                "clan_name": api_response.get("clan", {}).get("name", "No Clan"),
                "clan_rank": api_response.get("clanRank", "N/A"),
                "role": api_response.get("role", "N/A"),
                "troops_trained": len(api_response.get("troops", [])),
                "spells_trained": len(api_response.get("spells", [])),
                "heroes_upgraded": len(api_response.get("heroes", [])),
                "threat_level": "N/A",
                "clan_info": clan_info
            }
        except Exception as e:
            print(f"Error parsing player data: {e}")
            return None
    
    @staticmethod
    def _get_mock_player_data(player_tag: str) -> Dict[str, Any]:
        """Return mock Clash of Clans data for development/demo purposes"""
        import random
        
        th_levels = list(range(1, 17))
        roles = ["member", "elder", "co-leader", "leader"]
        
        return {
            "name": f"Player_{player_tag[-4:]}",
            "player_tag": player_tag,
            "town_hall_level": random.choice(th_levels),
            "exp_level": random.randint(1, 300),
            "trophies": random.randint(500, 8000),
            "best_trophies": random.randint(1000, 8500),
            "war_stars": random.randint(0, 500),
            "attack_wins": random.randint(0, 1000),
            "defense_wins": random.randint(0, 800),
            "clan_name": random.choice([
                "Dragon Force", "Elite Warriors", "Shadow Knights",
                "Gold Miners", "Fire Lords", "Ice Wizards"
            ]),
            "clan_rank": f"#{random.randint(1, 50)}",
            "role": random.choice(roles),
            "troops_trained": random.randint(0, 40),
            "spells_trained": random.randint(0, 15),
            "heroes_upgraded": random.randint(0, 6),
            "threat_level": random.choice(["Low", "Medium", "High", "Critical"]),
            "clan_info": {
                "name": "Demo Clan",
                "tag": "#P92VQC8UG",
                "badge_url": "https://via.placeholder.com/64"
            }
        }
    
    @staticmethod
    def get_clan_info(clan_tag: str) -> Optional[Dict[str, Any]]:
        """
        Get clan information
        
        Args:
            clan_tag: Clan tag (e.g., #P92VQC8UG)
            
        Returns:
            Dictionary with clan data or mock data
        """
        try:
            if not COC_API_KEY:
                return ClashOfClansService._get_mock_clan_data(clan_tag)
            
            if not clan_tag.startswith("#"):
                clan_tag = "#" + clan_tag
            
            encoded_tag = clan_tag.replace("#", "%23")
            url = f"{COC_API_BASE}/clans/{encoded_tag}"
            headers = ClashOfClansService._get_headers()
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "name": data.get("name", "Unknown"),
                    "tag": data.get("tag", ""),
                    "description": data.get("description", ""),
                    "clan_level": data.get("clanLevel", 0),
                    "clan_points": data.get("clanPoints", 0),
                    "members": data.get("members", 0),
                    "member_list": data.get("memberList", []),
                    "war_frequency": data.get("warFrequency", "N/A"),
                    "war_wins": data.get("warWins", 0),
                    "war_draws": data.get("warDraws", 0),
                    "war_losses": data.get("warLosses", 0),
                    "is_open": data.get("isOpen", False),
                    "badge_url": data.get("badgeUrls", {}).get("large", "")
                }
            else:
                return ClashOfClansService._get_mock_clan_data(clan_tag)
                
        except Exception as e:
            print(f"Error fetching clan info: {e}")
            return ClashOfClansService._get_mock_clan_data(clan_tag)
    
    @staticmethod
    def _get_mock_clan_data(clan_tag: str) -> Dict[str, Any]:
        """Return mock clan data"""
        import random
        
        return {
            "name": "Dragon Force Clan",
            "tag": clan_tag,
            "description": "Join us for epic wars and donations!",
            "clan_level": random.randint(1, 20),
            "clan_points": random.randint(10000, 100000),
            "members": random.randint(5, 50),
            "member_list": [],
            "war_frequency": random.choice(["always", "often", "sometimes", "rarely", "never"]),
            "war_wins": random.randint(0, 500),
            "war_draws": random.randint(0, 50),
            "war_losses": random.randint(0, 200),
            "is_open": random.choice([True, False]),
            "badge_url": "https://via.placeholder.com/64"
        }
    
    @staticmethod
    def get_troop_data(player_tag: str) -> Optional[Dict[str, Any]]:
        """Get troop information for a player"""
        try:
            if not COC_API_KEY:
                return ClashOfClansService._get_mock_troop_data()
            
            # Would require parsing from player data
            data = ClashOfClansService.get_player_data(player_tag)
            if data and "troops" in data:
                return {
                    "total_troops": len(data.get("troops", [])),
                    "troops": data.get("troops", [])
                }
            return ClashOfClansService._get_mock_troop_data()
            
        except Exception as e:
            print(f"Error fetching troop data: {e}")
            return ClashOfClansService._get_mock_troop_data()
    
    @staticmethod
    def _get_mock_troop_data() -> Dict[str, Any]:
        """Return mock troop data"""
        troop_names = [
            "Barbarian", "Archer", "Giant", "Goblin", "Wall Breaker",
            "Wizard", "Dragon", "P.E.K.K.A", "Hog Rider", "Balloon",
            "Baby Dragon", "Miner", "Electro Dragon", "Yeti", "Golem"
        ]
        
        troops = []
        for troop in troop_names[:8]:  # Random selection
            troops.append({
                "name": troop,
                "level": __import__("random").randint(1, 10),
                "max_level": 10
            })
        
        return {
            "total_troops": len(troops),
            "troops": troops
        }

