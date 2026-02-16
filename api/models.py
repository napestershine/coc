"""
Database models for Clash of Clans account management
"""
from datetime import datetime
from typing import List, Dict, Any

# In-memory storage (replace with actual database like SQLite/PostgreSQL)
accounts_db: Dict[int, Dict[str, Any]] = {}
account_counter = 1


class ClashOfClansAccount:
    """Model for Clash of Clans account"""
    
    def __init__(self, player_tag: str, account_id: int = None):
        self.id = account_id
        self.player_tag = player_tag  # e.g., #P92VQC8UG
        self.created_at = datetime.utcnow().isoformat()
        self.last_updated = datetime.utcnow().isoformat()
        self.player_info = {
            "name": "Unknown",
            "town_hall_level": 0,
            "exp_level": 0,
            "trophies": 0,
            "best_trophies": 0,
            "war_stars": 0,
            "attack_wins": 0,
            "defense_wins": 0,
            "clan_name": "No Clan",
            "clan_rank": "N/A",
            "role": "N/A",
            "troops_trained": 0,
            "spells_trained": 0,
            "heroes_upgraded": 0,
            "threat_level": "N/A"
        }
        self.clan_info = None
        self.troop_stats = {}
        self.building_stats = {}
        self.is_online = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert account to dictionary"""
        return {
            "id": self.id,
            "player_tag": self.player_tag,
            "created_at": self.created_at,
            "last_updated": self.last_updated,
            "player_info": self.player_info,
            "clan_info": self.clan_info,
            "troop_stats": self.troop_stats,
            "building_stats": self.building_stats,
            "is_online": self.is_online
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'ClashOfClansAccount':
        """Create account from dictionary"""
        account = ClashOfClansAccount(data.get("player_tag", ""), data.get("id"))
        account.player_info = data.get("player_info", {})
        account.clan_info = data.get("clan_info")
        account.troop_stats = data.get("troop_stats", {})
        account.building_stats = data.get("building_stats", {})
        account.is_online = data.get("is_online", False)
        return account


def create_account(player_tag: str) -> Dict[str, Any]:
    """Create a new Clash of Clans account entry"""
    global account_counter
    account = ClashOfClansAccount(player_tag, account_counter)
    accounts_db[account_counter] = account.to_dict()
    account_counter += 1
    return accounts_db[account.id]


def get_account(account_id: int) -> Dict[str, Any] | None:
    """Get account by ID"""
    return accounts_db.get(account_id)


def get_all_accounts() -> List[Dict[str, Any]]:
    """Get all accounts"""
    return list(accounts_db.values())


def update_account(account_id: int, data: Dict[str, Any]) -> Dict[str, Any] | None:
    """Update account"""
    if account_id not in accounts_db:
        return None
    
    account = accounts_db[account_id]
    account.update(data)
    account["last_updated"] = datetime.utcnow().isoformat()
    return account


def delete_account(account_id: int) -> bool:
    """Delete account"""
    if account_id in accounts_db:
        del accounts_db[account_id]
        return True
    return False


def update_player_info(account_id: int, player_info: Dict[str, Any]) -> Dict[str, Any] | None:
    """Update player information"""
    if account_id not in accounts_db:
        return None
    
    account = accounts_db[account_id]
    account["player_info"].update(player_info)
    account["last_updated"] = datetime.utcnow().isoformat()
    return account


def update_clan_info(account_id: int, clan_info: Dict[str, Any]) -> Dict[str, Any] | None:
    """Update clan information"""
    if account_id not in accounts_db:
        return None
    
    account = accounts_db[account_id]
    account["clan_info"] = clan_info
    account["last_updated"] = datetime.utcnow().isoformat()
    return account


def update_troop_stats(account_id: int, troops: Dict[str, Any]) -> Dict[str, Any] | None:
    """Update troop statistics"""
    if account_id not in accounts_db:
        return None
    
    account = accounts_db[account_id]
    account["troop_stats"] = troops
    account["last_updated"] = datetime.utcnow().isoformat()
    return account

