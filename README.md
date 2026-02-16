# Clash of Code Account Manager

A full-stack application to track and manage multiple Clash of Code accounts in one place.

## 🎯 Features

- ✅ Track multiple CoC accounts simultaneously
- ✅ View real-time account statistics and rankings
- ✅ Check online/offline status
- ✅ Monitor clash history and performance
- ✅ Beautiful Material 3 mobile interface
- ✅ Fast and responsive REST API
- ✅ Easy account management (add/delete)

## 🏗️ Project Structure

```
coc/
├── api/          # Flask REST API Backend
├── app/          # Flutter Mobile App
└── docs/         # Documentation
```

## 🚀 Quick Start

### Start the API

```bash
cd api
# Install dependencies
pip install -r requirements.txt

# Run server
python app.py
```

API runs at: `http://localhost:5000`

### Start the Flutter App

```bash
cd app
# Get dependencies
flutter pub get

# Run app
flutter run
```

## 📱 App Usage

1. **Add Account**: Tap the **+** button and enter CoC username
2. **View Details**: Tap any account to see full statistics
3. **Refresh Data**: Pull to refresh or tap refresh button
4. **Delete Account**: Long press and select delete

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/accounts` | List all accounts |
| POST | `/api/accounts` | Add new account |
| GET | `/api/accounts/<id>` | Get account details |
| POST | `/api/accounts/<id>/refresh` | Refresh account |
| DELETE | `/api/accounts/<id>` | Delete account |

[Full API Documentation](./api/API_DOCUMENTATION.md)

## 📖 Documentation

- [API Documentation](./api/API_DOCUMENTATION.md) - Complete API reference
- [Integration Guide](./INTEGRATION.md) - Full setup and architecture
- [Setup Guide](./SETUP.md) - Detailed setup instructions

## 🧠 Tech Stack

**Backend:**
- Flask (Python REST API)
- Python 3.8+
- HTTP requests to Clash of Code

**Frontend:**
- Flutter 3.0+
- Dart
- Material 3 Design

**Integration:**
- HTTP-based API communication
- JSON data format

## 💻 Requirements

### Backend
- Python 3.8+
- pip

### Frontend
- Flutter SDK 3.0+
- Dart SDK

## 📋 Account Statistics Tracked

- Player Level
- Rank and Global Rank
- Total Clashes Played
- Total Wins
- Win Rate
- Country
- Online Status
- Last Updated Time

## 🔄 Data Flow

```
Flutter App → HTTP → Flask API → CoC Service → CoC
    ↑                ↓                          ↓
    ← HTTP Response ← Process Data ← Fetch Data
```

## ⚙️ Configuration

### API Configuration

Edit `api/.env`:
```
FLASK_ENV=development
FLASK_DEBUG=True
```

### App Configuration

Edit `app/lib/services/api_service.dart`:
```dart
const String API_BASE_URL = 'http://localhost:5000';
```

For remote servers:
```dart
const String API_BASE_URL = 'http://192.168.x.x:5000';
```

## 🧪 Testing

### Test API
```bash
curl http://localhost:5000/api/health
```

### Test Add Account
```bash
curl -X POST http://localhost:5000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{"username": "player123"}'
```

## 🐛 Troubleshooting

**API won't start**
- Ensure port 5000 is not in use
- Check Python is installed: `python --version`

**App can't connect**
- Verify API is running
- Check URL in `api_service.dart`

## 📝 License

See [LICENSE](LICENSE) file.

## 💡 Support

For detailed documentation, see:
- [Setup Guide](./SETUP.md)
- [Integration Guide](./INTEGRATION.md)
- [API Documentation](./api/API_DOCUMENTATION.md)