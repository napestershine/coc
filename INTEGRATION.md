# Clash of Clans Account Manager - Integration Guide

## Overview

The Clash of Clans Account Manager is a Flutter mobile application that tracks multiple Clash of Clans player accounts. The app communicates directly with the official Clash of Clans API with no backend server required.

## Architecture

```
┌─────────────────────────────────┐
│   Flutter Mobile App            │
│   (iOS/Android)                 │
├─────────────────────────────────┤
│   Local State Management        │
│   - _playerTags: List<String>   │
│   - _playerData: List<COCAccount>
├─────────────────────────────────┤
│   HTTP Client (ApiService)      │
│   Bearer Token Authentication   │
├─────────────────────────────────┤
│   HTTPS Requests                │
│   https://api.clashofclans.com/v1
└─────────────────────────────────┘
```

## Project Structure

```
coc/
├── app/                          # Flutter Mobile App (ONLY)
│   ├── lib/
│   │   ├── main.dart            # App entry point & home screen
│   │   ├── services/
│   │   │   └── api_service.dart # HTTP client (direct API calls)
│   │   └── screens/
│   │       ├── player_search_screen.dart      # Add player UI
│   │       ├── account_details_screen.dart    # Account details
│   │       └── upgrades_screen.dart           # Track upgrades
│   ├── pubspec.yaml             # Flutter dependencies
│   └── test/
│       └── widget_test.dart
│
├── README.md                    # Project overview
├── SETUP.md                     # Setup instructions  
├── INTEGRATION.md               # This file (architecture guide)
├── LICENSE                      # License information
└── .gitignore                   # Git ignore configuration
```

## Features

### Core Features
- ✅ Add multiple Clash of Clans accounts by player tag
- ✅ Direct integration with official Clash of Clans API
- ✅ Display player statistics in real-time
- ✅ Track account upgrades (buildings, research, pets)
- ✅ Clan information display
- ✅ Combat statistics and achievements
- ✅ Manual refresh for current data
- ✅ Remove accounts from tracking
- ✅ Beautiful Material 3 design
- ✅ Error handling and user feedback

### Supported Statistics
- Town Hall level
- Trophies and best trophies
- War stars and attack/defense wins
- Clan information and role
- Experience level
- Heroes and spells information
- In-progress building/research/pet upgrades
- Time remaining for upgrades

## Clash of Clans API Endpoints

### Official API Used

Base URL: `https://api.clashofclans.com/v1`

**Endpoints called by the app:**

- `GET /players/{playerTag}` - Get player information
- `GET /clans/{clanTag}` - Get clan information

**Player Tag Format:**
```
#P92VQC8UG  (always starts with #)
```

**Authentication:**
```
Header: Authorization: Bearer YOUR_API_KEY
```

## Data Models

### COCAccount Model (Dart/Flutter)

```dart
class COCAccount {
  String playerTag                    // Player tag (e.g., #P92VQC8UG)
  String playerName                   // Player name
  int townHallLevel                   // Town Hall level (1-14+)
  int trophies                        // Current trophies
  int bestTrophies                    // Best trophies achieved
  int warStars                        // Total war stars
  String clanName                     // Current clan name
  String clanRank                     // Rank within clan
  int attackWins                      // Total attack wins
  int defenseWins                     // Total defense wins
  Map<String, dynamic> playerInfo     // Full player data from API
  Map<String, dynamic> clanInfo       // Full clan data from API
  DateTime fetchedAt                  // Time data was fetched
}
```

### Upgrade Model

```dart
class Upgrade {
  String name                         // Building/research/pet name
  String type                         // 'building', 'research', or 'pet'
  int level                           // Current level
  int nextLevel                       // Next level to upgrade to
  DateTime completeTime               // When upgrade finishes
  int timeRemaining                   // Seconds remaining
}
```

### Raw API Response Example

```json
{
  "tag": "#P92VQC8UG",
  "name": "Player_C8UG",
  "townHallLevel": 11,
  "trophies": 7503,
  "bestTrophies": 4577,
  "warStars": 281,
  "expLevel": 89,
  "clanRank": 34,
  "attackWins": 444,
  "defenseWins": 185,
  "clan": {
    "tag": "#9CYV8C",
    "name": "Dragon Force",
    "level": 19
  },
  "buildingsUnderConstruction": [
    {
      "name": "Barbarian King",
      "level": 49,
      "completeTime": "2025-02-17T10:30:00.000Z"
    }
  ],
  "researchUnderConstruction": [
    {
      "name": "Barbarian",
      "level": 8,
      "completeTime": "2025-02-17T12:45:00.000Z"
    }
  ]
}
```

## Setup Instructions

### Prerequisites

- Flutter 3.0+
- Dart SDK (included with Flutter)
- Git
- Clash of Clans API Key from https://developer.clashofclans.com/

### Step 1: Get Clash of Clans API Key

1. Go to https://developer.clashofclans.com/
2. Create an account
3. Create a new application/API key
4. Copy your API key to clipboard

### Step 2: Clone Repository

```bash
git clone <repository_url>
cd coc
```

### Step 3: Add API Key to Flutter App

Edit `app/lib/services/api_service.dart`:

```dart
const String COC_API_KEY = 'YOUR_API_KEY_HERE';
```

Replace `YOUR_API_KEY_HERE` with your actual API key from step 1.

### Step 4: Install Dependencies

```bash
cd app
flutter pub get
```

### Step 5: Run the App

```bash
flutter run
```

Or with a specific device:
```bash
flutter run -d <device_name>
```

## Usage

### Adding an Account

1. Launch the Flutter app
2. Tap the **+** button (Floating Action Button)
3. Enter your Clash of Clans player tag:
   - Format: `#XXXXXXXXXX` (numbers and letters)
   - Example: `#P92VQC8UG`
   - If you forget the `#`, it will be added automatically
4. Tap **Add Player**
5. Player data will be fetched from the official API
6. Account will appear in the main list

**Finding Your Player Tag:**
1. Open Clash of Clans game
2. Tap your profile icon
3. Go to Player Information
4. Your player tag is displayed at the top

### Viewing Account Details

1. Tap on any account card in the list
2. View player information:
   - **Town Hall Level** and **Trophies** (highlighted)
   - **Clan Information** (if in a clan)
   - **Combat Statistics** (attacks, defenses, war stars)
3. Tap **Refresh** button (top right) to update data
4. Tap **View Upgrades** to see buildings/research in progress

### Tracking Upgrades

1. On the account details screen, tap **View Upgrades**
2. View all in-progress upgrades:
   - **Buildings** - Town structures being upgraded
   - **Research** - Lab troops/spells being researched
   - **Pets** - Hero pets being upgraded
3. Time remaining counts down automatically
4. Tap **Refresh** to update times

### Removing an Account

1. On the home screen, swipe left on any account (if implemented)
2. Or tap the account and use the menu option to delete

## API Service Implementation

### Code Structure (app/lib/services/api_service.dart)

```dart
class ApiService {
  // Singleton instance
  static final ApiService _instance = ApiService._internal();
  
  factory ApiService() {
    return _instance;
  }
  
  ApiService._internal();
  
  // Get headers with Bearer token authentication
  static Map<String, String> _getHeaders() {
    return {
      'Authorization': 'Bearer $COC_API_KEY',
      'Content-Type': 'application/json',
    };
  }
  
  // Get player information
  Future<COCAccount?> getPlayer(String playerTag) async {
    final encodedTag = Uri.encodeComponent(playerTag);
    final response = await http.get(
      Uri.parse('https://api.clashofclans.com/v1/players/$encodedTag'),
      headers: _getHeaders(),
    ).timeout(const Duration(seconds: 10));
    
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return COCAccount.fromJson(data);
    }
    throw Exception('Failed to load player');
  }
  
  // Get clan information
  Future<Map<String, dynamic>?> getClan(String clanTag) async {
    final encodedTag = Uri.encodeComponent(clanTag);
    final response = await http.get(
      Uri.parse('https://api.clashofclans.com/v1/clans/$encodedTag'),
      headers: _getHeaders(),
    ).timeout(const Duration(seconds: 10));
    
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    throw Exception('Failed to load clan');
  }
  
  // Get upgrades in progress
  Future<Map<String, dynamic>?> getUpgrades(String playerTag) async {
    final account = await getPlayer(playerTag);
    if (account == null) return null;
    
    return {
      'buildings': _parseUpgrades(account.playerInfo['buildingsUnderConstruction']),
      'research': _parseUpgrades(account.playerInfo['researchUnderConstruction']),
      'pets': _parseUpgrades(account.playerInfo['petsUnderConstruction']),
    };
  }
}
```

## Network Communication Flow

### Adding a Player

```
User enters player tag (#P92VQC8UG)
    ↓
PlayerSearchScreen validates format
    ↓
_addPlayer() called in main.dart
    ↓
_loadPlayerData(playerTag) called
    ↓
ApiService().getPlayer(playerTag) called
    ↓
HTTP GET to https://api.clashofclans.com/v1/players/%23P92VQC8UG
with Authorization: Bearer COC_API_KEY header
    ↓
Response parsed into COCAccount object
    ↓
_playerData[index] = account
setState() called
    ↓
PlayerCard widget updated on screen
```

### Data Refresh

```
User taps refresh button
    ↓
_refreshAccount() called (details screen)
OR
_refreshUpgrades() called (upgrades screen)
    ↓
ApiService().getPlayer(playerTag) called
    ↓
HTTP GET to CoC API
    ↓
Updated data displayed
    ↓
SnackBar shows "Account refreshed"
```

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "Unauthorized" (401) | Invalid or expired API key | Regenerate at https://developer.clashofclans.com/ |
| "Not Found" (404) | Invalid player tag | Verify tag format: #XXXXXXXXXX |
| "Connection timeout" | Official API unavailable | Check internet connection |
| "Invalid player tag format" | Wrong format entered | Use format: #P92VQC8UG |

### Error Handling in App

```dart
Future<void> _loadPlayerData(String playerTag) async {
  try {
    final account = await ApiService().getPlayer(playerTag);
    if (account != null) {
      setState(() {
        _playerData[index] = account;
      });
    }
  } catch (e) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Error: ${e.toString()}')),
    );
  }
}
```

## Data Storage

### Current Implementation: Session-Based (In-Memory)

- Players stored in `_playerTags` list during app session
- Data lost when app closes
- Suitable for quick lookups and real-time updates

### Recommended: Persistent Storage

For production, implement SharedPreferences:

```dart
import 'package:shared_preferences/shared_preferences.dart';

Future<void> _savePlayerTags(List<String> tags) async {
  final prefs = await SharedPreferences.getInstance();
  await prefs.setStringList('player_tags', tags);
}

Future<List<String>> _loadPlayerTags() async {
  final prefs = await SharedPreferences.getInstance();
  return prefs.getStringList('player_tags') ?? [];
}
```

Add to `pubspec.yaml`:
```yaml
dependencies:
  shared_preferences: ^2.0.0
```

## Performance Considerations

### Current Optimizations
- ✅ Singleton ApiService pattern (reuse HTTP client)
- ✅ Timeout handling (10 seconds per request)
- ✅ Efficient JSON parsing with native Dart

### Potential Improvements
- [ ] Implement response caching with TTL
- [ ] Add request batching for multiple players
- [ ] Implement local database with Hive/Sqflite
- [ ] Add pagination for large data sets
- [ ] Background refresh using WorkManager
- [ ] Image caching for badges/crests

## Troubleshooting

### App Won't Connect to API

```bash
# Check internet connection
# On physical device, verify WiFi is connected
# On emulator, check WiFi is available to virtual machine
```

### "Invalid API Key" Error

```
1. Copy API key exactly from developer.clashofclans.com
2. Replace YOUR_API_KEY_HERE in api_service.dart
3. Rebuild and restart app
4. Check for trailing spaces in key
```

### Player Tag Not Found

```
1. Verify tag starts with # (app adds it automatically)
2. Check tag exists in official Clash of Clans game
3. Player account may be inactive or deleted
4. Try refreshing (sometimes takes a moment to update)
```

### No Internet Connection

```
1. Check WiFi/network is working
2. Verify app has internet permission (AndroidManifest.xml)
3. Check firewall isn't blocking HTTPS traffic
4. Try a different network or hotspot
```

## Development Workflow

### Making Changes to API Integration

1. Edit `app/lib/services/api_service.dart`
2. Add new methods or modify existing ones
3. Run `flutter hot reload` or `flutter run` to test
4. Check console for errors

### Making UI Changes

1. Edit screens in `app/lib/screens/`
2. Or main layout in `app/lib/main.dart`
3. Flutter hot reload automatically updates UI
4. Test on multiple screen sizes

### Adding New Packages

1. Edit `app/pubspec.yaml`
2. Add package under `dependencies:`
3. Run: `flutter pub get`
4. Import and use in code

## Clash of Clans API Documentation

For complete API reference, see:
https://developer.clashofclans.com/#/documentation

### Key Endpoints

- `/players/{playerTag}` - Complete player data
- `/clans/{clanTag}` - Complete clan data
- `/playerranks/globalranks` - Global leaderboard
- `/clanranks/globalranks` - Clan leaderboard

### Authentication

Clash of Clans API uses Bearer token authentication:

```
Authorization: Bearer YOUR_API_KEY
```

### Rate Limiting

- Requests are rate-limited by Clash of Clans
- Recommended: cache data for 5 minutes minimum
- Refresh manually when needed

## Future Enhancements

### Planned Features
- [ ] Persistent player storage (SharedPreferences)
- [ ] War log history tracking
- [ ] Player comparison view
- [ ] Push notifications for upgrade completion
- [ ] Dark mode support
- [ ] Multiple language support
- [ ] Offline mode with cached data
- [ ] Clan roster view
- [ ] War predictions

### Performance Improvements
- [ ] Response caching system
- [ ] Lazy loading for clans
- [ ] Image caching
- [ ] Background sync

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

For issues:
1. Check error message in app
2. Verify API key is valid
3. Check player tag format
4. Review this documentation
5. Check console logs for details

## License

This project is provided under the terms in the LICENSE file.



### COCAccount Model (Dart/Flutter)

```dart
class COCAccount {
  int id                              // Unique account ID
  String playerTag                    // Clash of Clans player tag (e.g., #P92VQC8UG)
  Map<String, dynamic> playerInfo     // Player statistics
  Map<String, dynamic> clanInfo       // Clan information
  String createdAt                    // Creation timestamp
  String lastUpdated                  // Last update timestamp
  
  // Computed properties:
  String playerName                   // Player name from playerInfo
  int townHallLevel                   // Town Hall level (1-14+)
  int trophies                        // Current trophy count
  int warStars                        // Total war stars
  String clanName                     // Clan name from playerInfo
  String clanRank                     // Clan rank from playerInfo
  int attackWins                      // Total attack victories
  int defenseWins                     // Total defense victories
}
```

### Player Info Object

```json
{
  "name": "Player_C8UG",
  "town_hall_level": 11,
  "trophies": 7503,
  "best_trophies": 4577,
  "war_stars": 281,
  "exp_level": 89,
  "attack_wins": 444,
  "defense_wins": 185,
  "clan_name": "Dragon Force",
  "clan_rank": "#34",
  "role": "leader",
  "troops_trained": 19,
  "spells_trained": 4,
  "heroes_upgraded": 4,
  "threat_level": "Critical"
}
```

### Clan Info Object

```json
{
  "name": "Dragon Force Clan",
  "tag": "#P92VQC8UG",
  "members": 18,
  "clan_level": 19,
  "clan_points": 27693,
  "war_wins": 80,
  "war_losses": 69,
  "war_draws": 17,
  "badge_url": "https://cdn.clashcdn.com/clan_badge.png"
}
```

---

## Setup Instructions

### Prerequisites

#### For API
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)
- Clash of Clans API Key (optional - demo mode works without it)

#### For App
- Flutter SDK (3.0.0 or higher)
- Dart SDK (included with Flutter)
- Android Studio or VS Code with Flutter extension

### Step 1: Get Clash of Clans API Key (Optional)

If you want to use live data from the official Clash of Clans API:

1. Visit [developer.clashofclans.com](https://developer.clashofclans.com)
2. Create an account
3. Register an application
4. Generate an API token
5. Note your token for the next step

**Without API Key:** The system runs in demo mode with generated realistic mock data.

### Step 2: Setup API Backend

```bash
# Navigate to api directory
cd api

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux
source venv/bin/activate
# On Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# (Optional) Add your Clash of Clans API key to .env
# Edit .env and add:
# COC_API_KEY=your_api_key_here

# Start the server
python app.py
```

The API will be available at `http://localhost:5000`

### Step 3: Setup Flutter App

```bash
# Navigate to app directory
cd app

# Get dependencies
flutter pub get

# Connect a device or start an emulator
# For Android: android emulator or physical device
# For iOS: iOS simulator or physical device (macOS only)

# Run the app
flutter run
```

### Step 4: Configuration

Update `app/lib/services/api_service.dart` if using a different API URL:

```dart
const String API_BASE_URL = 'http://YOUR_API_URL:5000';
```

For remote server:
```dart
const String API_BASE_URL = 'http://192.168.x.x:5000';  // Your server IP
```

For production use, update to your domain:
```dart
const String API_BASE_URL = 'https://your-domain.com/api';
```

---

## Usage

### Adding an Account

1. Launch the Flutter app
2. Tap the **+** button (FAB) or **Add Account** button
3. Enter your Clash of Clans player tag (e.g., `#P92VQC8UG`)
   - If you forget the `#`, the app will add it automatically
4. Tap **Add Account**
5. Account will be fetched and displayed in the list
6. The app will show:
   - Player name
   - Town Hall level (displayed prominently)
   - Trophy count
   - Clan name

### Viewing Account Details

1. Tap on any account card in the list
2. View detailed statistics:
   - **Town Hall & Trophies**: Highlighted at the top
   - **Clan Info**: Clan name, rank, and role (if in a clan)
   - **Combat Stats**: Attack wins, defense wins, war stars, best trophies
   - **Details**: Experience level, troops trained, spells, heroes upgraded
   - **Threat Level**: Based on Town Hall level
3. Tap the **Refresh** button (top right) to get latest data from official API

### Finding Your Player Tag

In the Clash of Clans game:
1. Open the game
2. Tap on your profile icon
3. Go to Player Information
4. Your player tag is displayed at the top (format: `#XXXXX`)

### Managing Accounts

- **Refresh Data**: Pull down on the account list to refresh all accounts, or use the refresh button on individual account details
- **Delete Account**: Use the menu (three dots) next to an account and select "Delete"
- **View More Details**: Tap any account card to see comprehensive statistics including clan info and troop levels

### What Data is Tracked?

For each player account, the system tracks:
- **Basic**: Name, tag, experience level, threat level
- **Achievements**: Trophies, best trophies, war stars, attack/defense wins
- **Clan**: Name, rank within clan, role, clan level
- **Army**: Troops trained, spells trained, heroes upgraded (with levels)

---

## API Usage Examples

### Using cURL

```bash
# Health check
curl http://localhost:5000/api/health

# Add Clash of Clans account by player tag
curl -X POST http://localhost:5000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{"player_tag": "#P92VQC8UG"}'

# List all accounts
curl http://localhost:5000/api/accounts

# Get account details
curl http://localhost:5000/api/accounts/1

# Get account stats with clan info
curl http://localhost:5000/api/accounts/1/stats

# Refresh account data
curl -X POST http://localhost:5000/api/accounts/1/refresh

# Delete account
curl -X DELETE http://localhost:5000/api/accounts/1
```

### Using Flutter/Dart

```dart
// Import API service
import 'services/api_service.dart';

// Get API service singleton instance
final apiService = ApiService();

// Add Clash of Clans account
final account = await apiService.addAccount('#P92VQC8UG');

// Get all accounts
final accounts = await apiService.getAccounts();

// Get account details
final details = await apiService.getAccountDetails(accountId);

// Get account stats
final stats = await apiService.getAccountStats(accountId);

// Refresh account data
final updated = await apiService.refreshAccount(accountId);

// Delete account
final success = await apiService.deleteAccount(accountId);
```

---

## Network Communication

### Request-Response Flow

```
Flutter App (Add player #P92VQC8UG)
    |
    | HTTP POST /api/accounts
    | Body: {"player_tag": "#P92VQC8UG"}
    V
Flask API
    |
    | Check if COC_API_KEY is set
    | Fetch from Clash of Clans API or generate mock data
    | Store in memory
    V
    | HTTP 201 (Created)
    | Response: Account with player_info, clan_info
    |
    V
Flutter App (Display in account list)
```

### API Service Details

- **Base URL**: `http://localhost:5000`
- **Default Timeout**: 10 seconds per request
- **Content-Type**: `application/json`
- **HTTP Methods**: GET (read), POST (create/refresh), DELETE (remove)
- **Authentication**: None required locally, Bearer token for official Clash of Clans API

---

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| Connection refused | API not running | Run: `cd api && python app.py` |
| Invalid player tag format | Wrong tag format | Use format: `#P92VQC8UG` (# required) |
| Player not found | Invalid player tag | Verify player tag in Clash of Clans |
| Network timeout | API slow/unavailable | Check API is running, increase timeout |
| 400 Bad Request | Missing player_tag field | Ensure JSON has "player_tag" key |
| 404 Not Found | Invalid account ID | Verify account exists with: `curl http://localhost:5000/api/accounts` |
| 401 Unauthorized | Invalid COC API key | Update COC_API_KEY in `.env` file |

### Error Handling in App

```dart
Future<List<COCAccount>> getAccounts() async {
  try {
    final response = await http.get(
      Uri.parse('$API_BASE_URL/accounts'),
      headers: {'Content-Type': 'application/json'},
    ).timeout(const Duration(seconds: 10));
    
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return List<COCAccount>.from(
        data['data'].map((x) => COCAccount.fromJson(x))
      );
    }
    throw Exception('Failed to load accounts');
  } catch (e) {
    print('Error: $e');
    rethrow;
  }
}
```

---

## Data Storage

### Current Implementation: In-Memory Storage

The current system stores accounts in memory using Python dictionaries:

```python
accounts_db = {
    1: {
        'id': 1,
        'player_tag': '#P92VQC8UG',
        'player_info': {...},
        'clan_info': {...},
        'created_at': '2026-02-16T15:42:59',
        'last_updated': '2026-02-16T15:43:00'
    }
}
```

**Limitations:** Data is lost when API restarts.

### Recommended Database Schema (For Production)

#### SQLite Schema

```sql
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_tag TEXT NOT NULL UNIQUE,
    player_name TEXT,
    town_hall_level INTEGER,
    trophies INTEGER,
    best_trophies INTEGER,
    war_stars INTEGER,
    exp_level INTEGER,
    attack_wins INTEGER,
    defense_wins INTEGER,
    clan_name TEXT,
    clan_rank TEXT,
    clan_role TEXT,
    troops_trained INTEGER,
    spells_trained INTEGER,
    heroes_upgraded INTEGER,
    threat_level TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE clan_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    clan_tag TEXT,
    clan_level INTEGER,
    clan_points INTEGER,
    members INTEGER,
    war_wins INTEGER,
    war_losses INTEGER,
    war_draws INTEGER,
    FOREIGN KEY (account_id) REFERENCES accounts(id)
);

CREATE TABLE troops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    troop_name TEXT,
    troop_level INTEGER,
    max_level INTEGER,
    FOREIGN KEY (account_id) REFERENCES accounts(id)
);
```

---

## Performance Considerations

### Current Implementation
- In-memory storage (fast but not persistent)
- Mock data generation for demo mode
- Direct Clash of Clans API calls (no caching)
- Single-threaded Flask (development only)

### Production Improvements
- [ ] Implement SQLite or PostgreSQL for persistence
- [ ] Add request caching with TTL
- [ ] Implement rate limiting per client
- [ ] Add background refresh tasks
- [ ] Use connection pooling for database
- [ ] Add API authentication (JWT)
- [ ] Implement pagination for large datasets
- [ ] Use multi-threading/async workers (Gunicorn)
- [ ] Cache frequently accessed player data

---

## Demo Mode Features

When `COC_API_KEY` is not set:
- ✅ Generate realistic mock player data
- ✅ Simulate various Town Hall levels (5-13)
- ✅ Generate troupe levels and hero data
- ✅ Simulate clan memberships and war records
- ✅ Generate consistent data for multiple accounts
- ✅ Useful for UI testing and development

**To Enable:** Don't set `COC_API_KEY` in `.env`

---

## Troubleshooting

### API Won't Start

```bash
# Check if port 5000 is in use
lsof -i :5000

# Kill process on port 5000 (Linux/macOS)
kill -9 $(lsof -t -i:5000)

# Try different port
# Edit api/app.py: app.run(port=8000)

# Check Python version
python --version

# Check dependencies installed
pip list | grep flask
```

### Flutter App Can't Connect

- Check API is running: `curl http://localhost:5000/api/health`
- Check URL in `app/lib/services/api_service.dart`
- Check network connectivity
- For Android emulator: use `10.0.2.2` instead of `localhost`
- For iOS simulator: use `localhost` or device IP

### Player Tag Not Found

- Verify player tag includes the `#` symbol
- Check tag is correct from in-game profile
- Ensure Clash of Clans API key is valid (if using live API)
- Player may have changed name/tag - try refreshing

### Mock Data in Production

- Mock data is generated with `COC_API_KEY=` (empty)
- To use live data, set `COC_API_KEY=your_actual_key`
- Verify key at [developer.clashofclans.com](https://developer.clashofclans.com)

---

## Development Workflow

### Making Changes

1. **Backend Changes**:
   ```bash
   # Edit api/app.py, api/models.py, or api/coc_service.py
   # Restart Flask: python app.py
   # Changes take effect immediately on restart
   ```

2. **Frontend Changes**:
   ```bash
   # Edit app/lib/main.dart, screens, or services
   # App auto-reloads in debug mode
   # Or manual restart: flutter run
   ```

### Local Testing

#### API Testing with cURL
```bash
# Test health endpoint
curl -s http://localhost:5000/api/health | python -m json.tool

# Test add account
curl -X POST http://localhost:5000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{"player_tag": "#P92VQC8UG"}' | python -m json.tool
```

#### Flutter Testing
```bash
# Run all tests
flutter test

# Run with verbose output
flutter test -v

# Run specific test file
flutter test test/widget_test.dart
```

---

## Future Enhancements

### Planned Features
- [ ] Real-time clan war notifications
- [ ] Push notifications for important events
- [ ] Player comparison/leaderboard view
- [ ] Advanced statistics and charts
- [ ] War attack prediction analysis
- [ ] Dark mode support
- [ ] Multiple language translations
- [ ] Offline mode with automatic sync
- [ ] Team/clan account aggregation
- [ ] Player progress tracking over time

### Backend Improvements
- [ ] GraphQL API support
- [ ] WebSocket for real-time updates
- [ ] Advanced caching strategy
- [ ] Machine learning for war predictions
- [ ] Export/import player data (CSV/JSON)
- [ ] Webhook support for integrations

---

## Support & Resources

For help:
1. Check [API_DOCUMENTATION.md](api/API_DOCUMENTATION.md) for REST API reference
2. Review README.md for quick start
3. Check error messages in Flutter console and API logs
4. Verify Clash of Clans API key validity
5. Ensure network connectivity to official API

---

## License

This project is provided under the terms in the LICENSE file in the project root.
