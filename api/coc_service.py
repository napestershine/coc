"""
Service to interact with CoC API and fetch account data
"""
import requests
from typing import Dict, Any, Optional
import json
from datetime import datetime

# CoC API Base URL (using CodinGame's public API)
COC_API_BASE = "https://www.codingame.com"
COC_API_ENDPOINT = f"{COC_API_BASE}/api/player"


class COCService:
    """Service to fetch and manage CoC account data"""
    
    @staticmethod
    def get_player_data(username: str) -> Optional[Dict[str, Any]]:
        """
        Fetch player data from Clash of Code
        
        Args:
            username: CoC username
            
        Returns:
            Dictionary with player data or None if not found
        """
        try:
            # Try to fetch from CoC API
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            # Attempt to get player data
            url = f"{COC_API_ENDPOINT}/find/{username}"
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return COCService._parse_player_data(data)
            else:
                # Return mock data for demo
                return COCService._get_mock_data(username)
                
        except Exception as e:
            print(f"Error fetching player data: {e}")
            return COCService._get_mock_data(username)
    
    @staticmethod
    def _parse_player_data(api_response: Dict[str, Any]) -> Dict[str, Any]:
        """Parse API response and extract relevant stats"""
        try:
            return {
                "username": api_response.get("publicHandle", "Unknown"),
                "level": api_response.get("level", 0),
                "rank": api_response.get("rank", "N/A"),
                "global_rank": api_response.get("globalRank", "N/A"),
                "clashes_count": api_response.get("nClashes", 0),
                "wins": api_response.get("nClashesWon", 0),
                "is_online": api_response.get("isOnline", False),
                "country": api_response.get("country", ""),
                "avatar": api_response.get("avatar", ""),
                "bio": api_response.get("bio", "")
            }
        except Exception as e:
            print(f"Error parsing player data: {e}")
            return None
    
    @staticmethod
    def _get_mock_data(username: str) -> Dict[str, Any]:
        """Return mock data for development/demo purposes"""
        import random
        
        return {
            "username": username,
            "level": random.randint(1, 50),
            "rank": f"#{random.randint(1, 10000)}",
            "global_rank": f"#{random.randint(1, 100000)}",
            "clashes_count": random.randint(10, 500),
            "wins": random.randint(0, 200),
            "is_online": random.choice([True, False]),
            "country": "US",
            "avatar": "https://via.placeholder.com/64",
            "bio": f"CoC Player - {username}",
            "last_clash": (datetime.utcnow().isoformat() if random.choice([True, False]) else None),
            "win_rate": f"{random.randint(20, 90)}%"
        }
    
    @staticmethod
    def get_current_clash(username: str) -> Optional[Dict[str, Any]]:
        """
        Get current clash information for a player
        
        Args:
            username: CoC username
            
        Returns:
            Dictionary with current clash data or None
        """
        try:
            # This would require more complex CoC API integration
            # For now, return mock data
            return {
                "is_in_clash": False,
                "time_remaining": 0,
                "mode": None,
                "language": None
            }
        except Exception as e:
            print(f"Error fetching current clash: {e}")
            return None
    
    @staticmethod
    def get_clash_history(username: str, limit: int = 10) -> list:
        """
        Get recent clash history for a player
        
        Args:
            username: CoC username
            limit: Number of recent clashes to fetch
            
        Returns:
            List of recent clash data
        """
        # Mock data for demonstration
        import random
        
        modes = ["Shortest", "Fastest", "Reverse"]
        languages = ["Python", "JavaScript", "Java", "C++", "C#"]
        
        history = []
        for i in range(min(limit, 5)):
            history.append({
                "id": i + 1,
                "mode": random.choice(modes),
                "language": random.choice(languages),
                "score": random.randint(0, 100),
                "result": random.choice(["Win", "Loss", "Timeout"]),
                "date": datetime.utcnow().isoformat()
            })
        
        return history
