# Clash of Clans Tracker - Architecture Overview

## ✨ Current Architecture (Simplified)

### Flutter-Only Design Pattern

The application uses a **direct REST client** architecture where the Flutter app communicates directly with the official Clash of Clans API with no middleware layer.

```
┌─────────────────────────────────────┐
│       Flutter App (iOS/Android)     │
│                                     │
│  ┌──────────────────────────────┐   │
│  │   Screens                    │   │
│  │ - main.dart (home + list)    │   │
│  │ - player_search_screen.dart  │   │
│  │ - account_details_screen.dart│   │
│  │ - upgrades_screen.dart       │   │
│  └──────────────────────────────┘   │
│                                     │
│  ┌──────────────────────────────┐   │
│  │   Local State Management     │   │
│  │ - _playerTags: List<String>  │   │
│  │ - _playerData: List<COCAccount>
│  └──────────────────────────────┘   │
│                                     │
│  ┌──────────────────────────────┐   │
│  │   ApiService (Singleton)     │   │
│  │ - getPlayer(playerTag)       │   │
│  │ - getClan(clanTag)           │   │
│  │ - getUpgrades(playerTag)     │   │
│  └──────────────────────────────┘   │
└──────────────────────────────────────┘
                  ↓
        HTTP + Bearer Token Auth
                  ↓
    https://api.clashofclans.com/v1
    (Official Clash of Clans API)
```

## 🏗️ Previous Architecture (Removed)

### Flask Backend Pattern (Deprecated)

Previously, the architecture had an unnecessary middleware layer:

```
Flutter App → Flask Backend → Clash of Clans API
```

**Why Removed:**
- ✅ Flask backend added complexity
- ✅ No persistence across restarts anyway
- ✅ Official Clash of Clans API already publicly available
- ✅ Removed 1 moving part, simpler deployment
- ✅ Reduced latency (no middleware hop)

**Deleted Files:**
- `/workspaces/coc/api/` - entire directory
- `app.py`, `coc_service.py`, `models.py`
- `requirements.txt`, `.env`, `.env.example`

## 📱 Current Data Flow

### Adding a Player

```
User Input
  ↓
PlayerSearchScreen (input validation)
  ↓
main.dart: _addPlayer()
  ↓
main.dart: _loadPlayerData(playerTag)
  ↓
ApiService.getPlayer(playerTag)
  ↓
HTTP GET /players/{playerTag}
  ↓
Parse COCAccount from JSON response
  ↓
Display in PlayerCard widget
```

### Fetching Upgrade Status

```
User taps "View Upgrades"
  ↓
UpgradesScreen opened
  ↓
_refreshUpgrades() called
  ↓
ApiService.getUpgrades(playerTag)
  ↓
HTTP GET /players/{playerTag}
  ↓
Extract: buildingsUnderConstruction, researchUnderConstruction, petsUnderConstruction
  ↓
Display with auto-updating countdown timers
```

## 📦 File Structure

```
coc/
├── app/
│   ├── lib/
│   │   ├── main.dart                          # Home screen + local player management
│   │   ├── services/
│   │   │   └── api_service.dart               # HTTP client (Direct CoC API calls)
│   │   └── screens/
│   │       ├── player_search_screen.dart      # NEW: Input validation for player tags
│   │       ├── account_details_screen.dart    # Player stats display
│   │       └── upgrades_screen.dart           # Track buildings/research/pets
│   ├── pubspec.yaml                           # Dependencies (http, flutter, etc.)
│   └── test/
│       └── widget_test.dart
│
├── README.md                                  # Project overview
├── SETUP.md                                   # Setup instructions (Flutter-only)
├── INTEGRATION.md                             # Architecture & API integration
├── ARCHITECTURE.md                            # This file
├── LICENSE
└── .gitignore
```

## 🔑 Key Components

### ApiService (app/lib/services/api_service.dart)

**Singleton HTTP client** providing access to Clash of Clans API:

```dart
// Get player info (calls official API)
Future<COCAccount?> getPlayer(String playerTag)

// Get clan info (calls official API)
Future<Map<String, dynamic>?> getClan(String clanTag)

// Extract upgrades from player data
Future<Map<String, dynamic>?> getUpgrades(String playerTag)
```

**Authentication:**
```dart
Map<String, String> _getHeaders() => {
  'Authorization': 'Bearer $COC_API_KEY',
  'Content-Type': 'application/json',
}
```

### Main Screen (app/lib/main.dart)

**Home screen with local player management:**

- `_playerTags`: List of player tags (in-memory)
- `_playerData`: List of fetched account data (in-memory)
- `_addPlayer()`: Navigate to PlayerSearchScreen
- `_loadPlayerData()`: Fetch from API
- `_removePlayer()`: Delete from list

### Player Search Screen (app/lib/screens/player_search_screen.dart)

**Input validation for player tags:**

- Validates alphanumeric format
- Auto-adds `#` prefix
- Shows 4-step guide for finding player tag in-game
- Returns to main.dart via Navigator.pop()

### Account Details Screen (app/lib/screens/account_details_screen.dart)

**Display player statistics:**

- Town Hall level
- Trophies
- Clan information
- Combat statistics
- Manual refresh button
- "View Upgrades" button

### Upgrades Screen (app/lib/screens/upgrades_screen.dart)

**Track in-progress upgrades:**

- Buildings, Research, Pets
- Auto-updating countdown timers
- Refresh every 10 seconds
- Time remaining display

## 🔄 State Management

**Simple, session-based approach:**

```dart
// In main.dart _HomeScreenState:
List<String> _playerTags = [];           // Player tags
List<COCAccount?> _playerData = [];      // Corresponding account data
bool _isLoading = false;                 // Loading state

// When user adds a player:
_playerTags.add(playerTag);
_playerData.add(null);                   // Placeholder while loading
_loadPlayerData(index, playerTag);       // Fetch from API

// When data arrives:
_playerData[index] = fetchedAccount;     // Update
setState(() {});                         // Redraw UI
```

## 🌐 API Integration

**Official Clash of Clans API:**
- Base: https://api.clashofclans.com/v1
- Auth: Bearer token (COC_API_KEY)
- Methods used: GET /players/{tag}, GET /clans/{tag}

**Requests:**
```http
GET /players/%23P92VQC8UG HTTP/1.1
Host: api.clashofclans.com
Authorization: Bearer YOUR_API_KEY
```

**Response:** Full player JSON with stats, clan info, upgrades

## 📊 Data Models

### COCAccount (Dart Model)

```dart
class COCAccount {
  String playerTag;
  String playerName;
  int townHallLevel;
  int trophies;
  int warStars;
  String clanName;
  String clanRank;
  // ... more fields
  
  // Computed from API response
  static COCAccount fromJson(Map<String, dynamic> json)
}
```

### Upgrade Model

```dart
buildingsUnderConstruction: [
  {name: "Barbarian King", level: 49, completeTime: "2025-02-17T10:30:00Z"}
]
researchUnderConstruction: [
  {name: "Barbarian", level: 8, completeTime: "2025-02-17T12:45:00Z"}
]
petsUnderConstruction: [
  {name: "Phoenix", level: 2, completeTime: "2025-02-17T15:00:00Z"}
]
```

## 🚀 Deployment

**No server needed!** Just Flutter app + API key:

1. Build Flutter app (.apk, .ipa, or web)
2. Insert COC_API_KEY in `api_service.dart`
3. Deploy app to users
4. App calls official Clash of Clans API directly

## ✅ Benefits of Current Architecture

| Aspect | Benefit |
|--------|---------|
| Simplicity | No backend to maintain |
| Speed | Direct API calls, no middleware latency |
| Scalability | No server resource constraints |
| Reliability | One less moving part |
| Cost | Zero server hosting costs |
| Deployment | Just distribute the app |

## 🔒 Security Notes

- API key stored in app binary (not ideal for production)
- Consider: Move to secure backend auth in future
- Current: Suitable for personal/demo apps
- Production: Use proper backend with API key management

## 📚 Documentation

- [SETUP.md](SETUP.md) - Setup instructions
- [INTEGRATION.md](INTEGRATION.md) - Detailed integration guide
- [README.md](README.md) - Project overview

## 🎯 Next Steps (Optional Enhancements)

1. **Persistent Storage**: Add SharedPreferences for saved players
2. **Caching**: Cache API responses for 5+ minutes
3. **Background Sync**: Periodic background refresh
4. **Production Security**: Backend proxy for API key
5. **Notifications**: Alert on upgrade completion

---

**Architecture Last Updated:** 2025-02-17  
**Current Status:** Simplified, Flutter-only direct API architecture
