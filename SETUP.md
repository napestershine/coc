# Clash of Clans Account Manager - Setup Guide

A complete full-stack application to track multiple Clash of Clans accounts with a Flutter frontend and Flask backend API that integrates with the official Clash of Clans API.

## Project Structure

```
coc/
├── app/           # Flutter mobile application
├── api/           # Flask REST API backend  
├── README.md      # Project overview and features
├── SETUP.md       # This setup guide
├── INTEGRATION.md # Architecture and integration details
├── LICENSE        # License information
└── .gitignore     # Git ignore configuration
```

## Quick Start

### Prerequisites

- Python 3.8+ (for API)
- Flutter 3.0+ (for app)
- Dart SDK (included with Flutter)
- Git

### API Setup (Flask Backend)

```bash
# Navigate to API directory
cd api

# Create virtual environment
python -m venv venv

# Activate environment
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (optional - for API key)
cp .env.example .env
# Edit .env and add COC_API_KEY if you have one

# Run the API server
python app.py
```

The API will be available at `http://localhost:5000`

### App Setup (Flutter Frontend)

```bash
# Navigate to app directory
cd app

# Get Flutter dependencies
flutter pub get

# Run the app
flutter run
```

## Prerequisites

### For API
- Python 3.8 or higher
- pip (Python package manager)

### For App
- Flutter SDK (3.0.0+)
- Dart SDK
- Android SDK (for Android development)
- Xcode (for iOS development on macOS)

## API Documentation

### Base URL
```
http://localhost:5000
```

### Main Endpoints

- `GET /api/health` - Health check (verify API is running)
- `GET /api/accounts` - List all tracked Clash of Clans accounts
- `POST /api/accounts` - Add new account (requires player_tag)
- `GET /api/accounts/<id>` - Get account details
- `GET /api/accounts/<id>/stats` - Get detailed stats including clan info
- `POST /api/accounts/<id>/refresh` - Refresh account data from official API
- `DELETE /api/accounts/<id>` - Remove account from tracking

For detailed documentation, see [API_DOCUMENTATION.md](api/API_DOCUMENTATION.md)

## Getting Clash of Clans API Key (Optional)

For live data instead of demo mode:

1. Visit https://developer.clashofclans.com/
2. Create account and register application
3. Generate API token
4. Add to `.env`: `COC_API_KEY=your_token`

Without the key, the system generates realistic mock data for testing.

## App Architecture

The Flutter app is structured with:
- Material 3 design system
- HTTP client (Singleton ApiService) for API communication
- Separate screens: AddAccountScreen, AccountDetailsScreen
- Account list view with real-time statistics
- Support for Android and iOS

## Project Files

### API (`/api`)
- `app.py` - Main Flask REST API application
- `models.py` - ClashOfClansAccount data model
- `coc_service.py` - Clash of Clans API integration service
- `requirements.txt` - Python dependencies (Flask, requests, python-dotenv)
- `.env.example` - Environment variables template
- `.env` - API key configuration (create from example)
- `API_DOCUMENTATION.md` - Complete API endpoint documentation

### App (`/app`)
- `lib/main.dart` - App entry point and home screen with account list
- `lib/services/api_service.dart` - HTTP client for API communication
- `lib/screens/add_account_screen.dart` - Add new account UI
- `lib/screens/account_details_screen.dart` - View account statistics
- `pubspec.yaml` - Flutter dependencies (http, material, etc.)
- `test/widget_test.dart` - Widget tests

## Development

### API Development

To modify API endpoints or add features, edit `api/app.py`:

```python
@app.route('/api/accounts/<id>/custom', methods=['GET'])
def custom_endpoint(id):
    account = get_account(id)
    return jsonify({'custom': 'response'})
```

To modify data models, edit `api/models.py`.

To add Clash of Clans API features, edit `api/coc_service.py`.

### App Development

To modify the UI, edit files in `app/lib/`:
- Main layout: `main.dart`
- Add account: `screens/add_account_screen.dart`
- View details: `screens/account_details_screen.dart`

To add packages, edit `app/pubspec.yaml` and run:
```bash
cd app
flutter pub get
```

## Testing

### API Health Check
```bash
curl http://localhost:5000/api/health
```

### Add Test Account
```bash
curl -X POST http://localhost:5000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{"player_tag": "#P92VQC8UG"}'
```

### App Tests
```bash
cd app
flutter test
```

## Building for Production

### Android APK
```bash
cd app
flutter build apk --release
```

### iOS App
```bash
cd app
flutter build ios --release
```

### Web App
```bash
cd app
flutter build web --release
```

## Environment Configuration

The API uses environment variables. Create `api/.env`:

```bash
cp api/.env.example api/.env
```

Edit `api/.env` with:
```
COC_API_KEY=your_actual_api_key_from_developer_clashofclans_com
FLASK_ENV=development
FLASK_DEBUG=True
```

**Without COC_API_KEY:** System runs in demo mode with mock data.

## Troubleshooting

### Flask API not starting
- Ensure Python 3.8+ is installed
- Try: `python -m flask run`
- Check port 5000 is not in use

### Flutter issues
- Ensure `flutter --version` works
- Run `flutter doctor` to check environment
- Clear build: `flutter clean && flutter pub get`

## Contributing

1. Create a feature branch from `main`
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

See LICENSE file for details.
