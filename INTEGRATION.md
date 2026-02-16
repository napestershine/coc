# CoC Account Manager - Integration Guide

## Overview

The CoC Account Manager is a full-stack application for tracking multiple Clash of Code accounts. It consists of:

- **Backend**: Flask REST API (`/api`) - manages account data
- **Frontend**: Flutter Mobile App (`/app`) - displays and manages accounts
- **Integration**: HTTP-based communication between backend and frontend

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
- ✅ Add multiple CoC accounts to track
- ✅ Fetch real-time player data from Clash of Code
- ✅ Store account statistics (level, rank, clashes, wins)
- ✅ Get current clash information
- ✅ Retrieve clash history
- ✅ Automatic data refresh
- ✅ Remove accounts from tracking

### Mobile App Features
- ✅ View all tracked accounts
- ✅ Add new accounts with username
- ✅ View detailed account statistics
- ✅ See online/offline status
- ✅ Manual refresh for account data
- ✅ Delete accounts
- ✅ Beautiful Material 3 UI
- ✅ Error handling and user feedback

---

## API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/accounts` | List all accounts |
| POST | `/api/accounts` | Add new account |
| GET | `/api/accounts/<id>` | Get account details |
| GET | `/api/accounts/<id>/stats` | Get account statistics |
| POST | `/api/accounts/<id>/refresh` | Refresh account data |
| DELETE | `/api/accounts/<id>` | Delete account |

For detailed API documentation, see [API_DOCUMENTATION.md](api/API_DOCUMENTATION.md)

---

## Data Models

### COCAccount Model

```dart
class COCAccount {
  int id                          // Unique account ID
  String username                 // CoC username
  Map<String, dynamic> stats      // Account statistics
  String createdAt                // Creation timestamp
  String lastUpdated              // Last update timestamp
  bool isOnline                   // Online status
}
```

### Account Statistics

```json
{
  "level": 25,                    // Player level
  "rank": "#1523",                // Rank number
  "global_rank": "#45231",        // Global rank
  "clashes_count": 156,           // Total clashes played
  "wins": 89,                     // Total wins
  "win_rate": "57%",              // Win percentage
  "country": "US",                // Country
  "bio": "CoC Player"             // Player bio
}
```

---

## Setup Instructions

### Prerequisites

#### For API
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

#### For App
- Flutter SDK (3.0.0 or higher)
- Dart SDK
- Android Studio or VS Code with Flutter extension

### Step 1: Setup API Backend

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

# Copy environment file
cp .env.example .env

# Start the server
python app.py
```

The API will be available at `http://localhost:5000`

### Step 2: Setup Flutter App

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

### Step 3: Configuration

Update `app/lib/services/api_service.dart` if using a different API URL:

```dart
const String API_BASE_URL = 'http://YOUR_API_URL:5000';
```

For remote server:
```dart
const String API_BASE_URL = 'http://192.168.x.x:5000';  // Your server IP
```

---

## Usage

### Adding an Account

1. Launch the Flutter app
2. Tap the **+** button or **Add Account** button
3. Enter your Clash of Code username
4. Tap **Add Account**
5. Account will be fetched and displayed

### Viewing Account Details

1. Tap on any account card in the list
2. View detailed statistics:
   - Level, Rank, Global Rank
   - Total Clashes and Wins
   - Win Rate and Country
   - Online Status
3. Tap the **Refresh** button (top right) to get latest data

### Managing Accounts

- **Refresh Data**: Pull down on the account list or tap refresh on account details
- **Delete Account**: Long press account card and select "Delete"
- **View Details**: Tap any account card to see full details

---

## API Usage Examples

### Using cURL

```bash
# Add account
curl -X POST http://localhost:5000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{"username": "player123"}'

# List accounts
curl http://localhost:5000/api/accounts

# Get account details
curl http://localhost:5000/api/accounts/1

# Refresh account
curl -X POST http://localhost:5000/api/accounts/1/refresh

# Delete account
curl -X DELETE http://localhost:5000/api/accounts/1
```

### Using Flutter

```dart
// Import API service
import 'services/api_service.dart';

// Add account
final account = await ApiService().addAccount('player123');

// Get all accounts
final accounts = await ApiService().getAccounts();

// Get account details
final details = await ApiService().getAccountDetails(accountId);

// Refresh account
final updated = await ApiService().refreshAccount(accountId);

// Delete account
final success = await ApiService().deleteAccount(accountId);
```

---

## Network Communication

### Request-Response Flow

```
Flutter App
    |
    | HTTP Request (JSON)
    V
Flask API
    |
    | Fetch/Process Data
    | (Query CoC, update stats)
    V
    | HTTP Response (JSON)
    |
    V
Flutter App (Update UI)
```

### API Service Details

- **Base URL**: `http://localhost:5000`
- **Timeout**: 10 seconds per request
- **Content-Type**: `application/json`
- **Methods**: GET, POST, DELETE

---

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| Connection refused | API not running | Start API: `python app.py` |
| Username not found | Invalid username | Check username spelling |
| Network timeout | API slow/unavailable | Increase timeout or restart API |
| 400 Bad Request | Missing fields | Ensure username is provided |
| 404 Not Found | Invalid account ID | Verify account exists |

### Error Handling in App

```dart
Future<List<COCAccount>> getAccounts() async {
  try {
    // API call
    final response = await http.get(...);
    
    if (response.statusCode == 200) {
      // Success
      return accounts;
    }
    return [];
  } catch (e) {
    // Handle error
    print('Error: $e');
    return [];
  }
}
```

---

## Database Schema

Currently uses in-memory storage. For production:

### Suggested SQLite Schema

```sql
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    level INTEGER DEFAULT 0,
    rank TEXT,
    global_rank TEXT,
    clashes_count INTEGER DEFAULT 0,
    wins INTEGER DEFAULT 0,
    win_rate TEXT,
    country TEXT,
    bio TEXT,
    is_online BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE clash_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    mode TEXT,
    language TEXT,
    score INTEGER,
    result TEXT,
    clash_date TIMESTAMP,
    FOREIGN KEY(account_id) REFERENCES accounts(id)
);
```

---

## Performance Considerations

### Current Implementation
- In-memory storage (fast but not persistent)
- Mock data for demo purposes
- Single-threaded API

### Production Improvements
- [ ] Implement SQLite or PostgreSQL
- [ ] Add request caching
- [ ] Implement rate limiting
- [ ] Add background refresh tasks
- [ ] Use connection pooling
- [ ] Add API authentication
- [ ] Implement pagination for large datasets

---

## Security Considerations

### Current Status
- ⚠️ No authentication
- ⚠️ No HTTPS
- ⚠️ No input validation
- ⚠️ No SQL protection

### Production Recommendations
- [ ] Implement JWT authentication
- [ ] Use HTTPS/TLS
- [ ] Add input validation and sanitization
- [ ] Use parameterized queries for database
- [ ] Implement CORS properly
- [ ] Add rate limiting
- [ ] Log security events

---

## Troubleshooting

### API Won't Start

```bash
# Check if port 5000 is in use
lsof -i :5000

# Kill process on port 5000 (Linux/macOS)
kill -9 $(lsof -t -i:5000)

# Try different port
# Edit app.py: app.run(port=8000)
```

### Flutter App Can't Connect

- Check API is running: `curl http://localhost:5000/api/health`
- Check URL in `api_service.dart`
- Check network connectivity
- For emulator on Windows/Linux: use `10.0.2.2` instead of `localhost`

### Account Not Found

- Verify username is spelled correctly
- Check CoC API availability
- Try again (may be temporary issue)

---

## Development Workflow

### Making Changes

1. **Backend Changes**:
   ```bash
   # Edit api/app.py or api/coc_service.py
   # Restart Flask: python app.py
   ```

2. **Frontend Changes**:
   ```bash
   # Edit app/lib/main.dart or screens
   # App auto-reloads in debug mode
   # Or run: flutter run
   ```

### Testing

#### API Testing
```bash
# Test endpoints
curl -X GET http://localhost:5000/api/accounts
```

#### App Testing
```bash
# Run tests
flutter test

# Run with instrumentation
flutter test -v
```

---

## Future Enhancements

### Planned Features
- [ ] Real-time notifications for clash start
- [ ] Push notifications for account events
- [ ] Leaderboard view and rankings
- [ ] Advanced statistics and charts
- [ ] Clash predictions and analysis
- [ ] Dark mode support
- [ ] Multi-language support
- [ ] Offline mode with sync
- [ ] Team/group account tracking
- [ ] Performance analytics

### API Improvements
- [ ] GraphQL support
- [ ] WebSocket for real-time updates
- [ ] Advanced caching layer
- [ ] Machine learning for predictions
- [ ] Export/import account data

---

## Support

For issues or questions:

1. Check [API_DOCUMENTATION.md](api/API_DOCUMENTATION.md) for API details
2. Review error messages and logs
3. Check Flutter console for app errors
4. Verify network connectivity
5. Restart API and app

---

## License

See LICENSE file in project root.
