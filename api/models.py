"""
Database models for CoC account management
"""
from datetime import datetime
from typing import List, Dict, Any

# In-memory storage (replace with actual database like SQLite/PostgreSQL)
accounts_db: Dict[int, Dict[str, Any]] = {}
account_counter = 1


class COCAccount:
    """Model for Clash of Code account"""
    
    def __init__(self, username: str, account_id: int = None):
        self.id = account_id
        self.username = username
        self.created_at = datetime.utcnow().isoformat()
        self.last_updated = datetime.utcnow().isoformat()
        self.stats = {
            "level": 0,
            "rank": "N/A",
            "clashes_count": 0,
            "wins": 0,
            "global_rank": "N/A"
        }
        self.current_clash = None
        self.is_online = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert account to dictionary"""
        return {
            "id": self.id,
            "username": self.username,
            "created_at": self.created_at,
            "last_updated": self.last_updated,
            "stats": self.stats,
            "current_clash": self.current_clash,
            "is_online": self.is_online
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'COCAccount':
        """Create account from dictionary"""
        account = COCAccount(data.get("username", ""), data.get("id"))
        account.stats = data.get("stats", {})
        account.current_clash = data.get("current_clash")
        account.is_online = data.get("is_online", False)
        return account


def create_account(username: str) -> Dict[str, Any]:
    """Create a new CoC account entry"""
    global account_counter
    account = COCAccount(username, account_counter)
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


def update_account_stats(account_id: int, stats: Dict[str, Any]) -> Dict[str, Any] | None:
    """Update account statistics"""
    if account_id not in accounts_db:
        return None
    
    account = accounts_db[account_id]
    account["stats"].update(stats)
    account["last_updated"] = datetime.utcnow().isoformat()
    return account
