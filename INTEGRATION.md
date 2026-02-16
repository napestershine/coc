# Clash of Clans Account Manager - Integration Guide

## Overview

The Clash of Clans Account Manager is a full-stack application for tracking multiple Clash of Clans player accounts. It consists of:

- **Backend**: Flask REST API (`/api`) - integrates with Clash of Clans official API
- **Frontend**: Flutter Mobile App (`/app`) - displays account data and statistics
- **Integration**: HTTP-based REST communication between backend and frontend
- **External API**: Official Clash of Clans API (https://api.clashofclans.com/v1)

---

## Project Structure

```
coc/
├── api/                          # Flask API Backend
│   ├── app.py                   # Main Flask application
│   ├── models.py                # Account models and database logic
│   ├── coc_service.py           # CoC data service (API integration)
│   ├── requirements.txt         # Python dependencies
│   ├── .env                     # Environment configuration
│   ├── .env.example
│   ├── API_DOCUMENTATION.md     # Complete API documentation
│   ├── run.sh / run.bat         # Startup scripts
│   └── README.md
│
├── app/                          # Flutter Mobile App
│   ├── lib/
│   │   ├── main.dart            # App entry point and home screen
│   │   ├── services/
│   │   │   └── api_service.dart # HTTP client for API communication
│   │   └── screens/
│   │       ├── add_account_screen.dart       # Add account UI
│   │       └── account_details_screen.dart   # Account details UI
│   ├── pubspec.yaml             # Flutter dependencies
│   ├── test/
│   │   └── widget_test.dart
│   └── run.sh / run.bat
│
└── INTEGRATION.md               # This file
```

---

## Features

### Backend API Features
- ✅ Track multiple Clash of Clans player accounts
- ✅ Fetch live player data from official Clash of Clans API
- ✅ Store comprehensive player statistics (TH level, trophies, war stars)
- ✅ Display clan information and membership details
- ✅ Track combat statistics (attacks, defenses, wins)
- ✅ Retrieve troop and hero information
- ✅ Automatic and manual data refresh
- ✅ Demo mode with mock data when API key not available
- ✅ Remove accounts from tracking

### Mobile App Features
- ✅ View all tracked Clash of Clans accounts
- ✅ Add new accounts by player tag (e.g., #P92VQC8UG)
- ✅ Display Town Hall level prominently on account cards
- ✅ View detailed account statistics and clan information
- ✅ See trophy count, war stars, and combat history
- ✅ Manual refresh for real-time data sync
- ✅ Delete accounts from tracking
- ✅ Beautiful Material 3 UI with proper spacing
- ✅ Error handling and user feedback

---

## API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check - verify API is running |
| GET | `/api/accounts` | List all tracked Clash of Clans accounts |
| POST | `/api/accounts` | Add new Clash of Clans player account |
| GET | `/api/accounts/<id>` | Get account details with player info |
| GET | `/api/accounts/<id>/stats` | Get comprehensive stats including clan/troop data |
| POST | `/api/accounts/<id>/refresh` | Refresh account data from official API |
| DELETE | `/api/accounts/<id>` | Delete account from tracking |

**Request Format for Adding Account:**
```json
{
  "player_tag": "#P92VQC8UG"
}
```

**Note:** Player tags start with `#` and are required for all operations.

For detailed API documentation, see [API_DOCUMENTATION.md](api/API_DOCUMENTATION.md)

---

## Data Models

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
