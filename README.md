# Clash of Clans Account Manager

A full-stack application to track and manage multiple Clash of Clans player accounts in one place.

## 🎯 Features

- ✅ Track multiple Clash of Clans accounts simultaneously
- ✅ View Town Hall level, trophies, and war stats
- ✅ Monitor clan information and player rank
- ✅ Track attack and defense wins
- ✅ Beautiful Material 3 mobile interface
- ✅ Fast and responsive REST API
- ✅ Easy account management (add/delete)
- ✅ Real-time data sync with official Clash of Clans API

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

1. **Add Account**: Tap the **+** button and enter Clash of Clans player tag (e.g., #P92VQC8UG)
2. **View Details**: Tap any account to see full statistics including Town Hall, trophies, clan info
3. **Refresh Data**: Pull to refresh or tap refresh button to sync latest data
4. **Delete Account**: Use menu to remove account from tracker

## 🔄 Player Tag Format

- Player tags start with `#` followed by alphanumeric characters
- Example: `#P92VQC8UG`
- Find your tag in-game under Profile → Player Information

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
- Official Clash of Clans API (https://api.clashofclans.com/v1)
- HTTP-based REST API communication
- JSON data format

## 💻 Requirements

### Backend
- Python 3.8+
- pip
- COC API Key (optional for demo mode)

### Frontend
- Flutter SDK 3.0+
- Dart SDK

## 📋 Account Statistics Tracked

**Player Info:**
- Player Name and Tag
- Town Hall Level (TH1-TH14+)
- Trophies and Best Trophies
- Experience Level
- War Stars
- Attack Wins / Defense Wins
- Threat Level

**Clan Info:**
- Clan Name
- Clan Rank
- Member Role (Leader, Co-leader, Member, Elder)
- Clan Level

**Combat Stats:**
- Troops Trained Count
- Spells Trained Count
- Heroes Upgraded Count
- Attack/Defense History

## 🔄 Data Flow

```
Flutter App → HTTP → Flask API → Clash of Clans Service → Official CoC API
    ↑                ↓                                              ↓
    ← HTTP Response ← Process Data ← Get Player Data ← api.clashofclans.com
```

## ⚙️ Configuration

### API Configuration with Clash of Clans API Key

1. Get your API key from [developer.clashofclans.com](https://developer.clashofclans.com)
2. Create `api/.env` file:

```
COC_API_KEY=your_api_key_here
FLASK_ENV=development
FLASK_DEBUG=True
```

3. Without API key, the system runs in **demo mode** with generated mock data

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

### Test API is Healthy
```bash
curl http://localhost:5000/api/health
```

### Test Add Clash of Clans Account
```bash
curl -X POST http://localhost:5000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{"player_tag": "#P92VQC8UG"}'
```

### List All Accounts
```bash
curl http://localhost:5000/api/accounts
```

### Get Account Stats
```bash
curl http://localhost:5000/api/accounts/1/stats
```

## 🐛 Troubleshooting

**API won't start**
- Ensure port 5000 is not in use
- Check Python is installed: `python --version`
- Check requirements installed: `pip install -r requirements.txt`

**App can't connect**
- Verify API is running on correct port
- Check URL in `api_service.dart` matches your setup
- Ensure firewall allows connection

**Player tag format errors**
- Player tags must be in format: `#XXXXX` (alphanumeric)
- Get your tag from in-game profile
- App automatically adds `#` if you forget it

## 📝 License

See [LICENSE](LICENSE) file.

## 💡 Support

For detailed documentation, see:
- [Setup Guide](./SETUP.md)
- [Integration Guide](./INTEGRATION.md)
- [API Documentation](./api/API_DOCUMENTATION.md)