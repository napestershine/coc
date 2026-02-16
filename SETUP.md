# Clash of Clans Account Manager - Setup Guide

A Flutter mobile application to track multiple Clash of Clans accounts. The app calls the official Clash of Clans API directly with no backend server required.

## Project Structure

```
coc/
├── app/           # Flutter mobile application
├── README.md      # Project overview and features
├── SETUP.md       # This setup guide
├── INTEGRATION.md # Architecture and integration details
├── LICENSE        # License information
└── .gitignore     # Git ignore configuration
```

## Quick Start

### Prerequisites

- Flutter 3.0+
- Dart SDK (included with Flutter)
- Git
- Clash of Clans API Key (see below)

### 1. Get Clash of Clans API Key

1. Visit https://developer.clashofclans.com/
2. Login or create an account
3. Create a new application
4. Generate an API key
5. Copy your API key (you'll need it in step 3)

### 2. Update API Key in App

Edit `app/lib/services/api_service.dart` and replace:

```dart
const String COC_API_KEY = 'YOUR_API_KEY_HERE';
```

with your actual API key from step 1.

### 3. Run Flutter App

```bash
# Navigate to app directory
cd app

# Get Flutter dependencies
flutter pub get

# Run the app
flutter run
```

## Prerequisites

- Flutter SDK (3.0.0+)
- Dart SDK (included with Flutter)
- Android SDK (for Android development)
- Xcode (for iOS development on macOS)

## App Architecture

The Flutter app uses:
- Material 3 design system
- HTTP client (Singleton ApiService) for direct Clash of Clans API calls
- Local in-memory account management
- Screens: PlayerSearchScreen, AccountDetailsScreen, UpgradesScreen
- Account list with real-time statistics
- Support for Android and iOS

## How It Works

1. **Add Account**: Enter a player tag (e.g., #P92VQC8UG) in PlayerSearchScreen
2. **Fetch Data**: App calls Clash of Clans API directly with your API key
3. **Display Info**: Show player stats including:
   - Town Hall level
   - Trophies
   - Clan information
   - Combat statistics
4. **Track Upgrades**: View buildings, research, and pets currently under construction
5. **Refresh**: Pull latest data anytime with the refresh button

## Project Files

### App (`/app`)
- `lib/main.dart` - App entry point and home screen (player list management)
- `lib/services/api_service.dart` - HTTP client for Clash of Clans API (direct calls)
- `lib/screens/player_search_screen.dart` - Add new player UI with tag validation
- `lib/screens/account_details_screen.dart` - View player statistics
- `lib/screens/upgrades_screen.dart` - Track buildings/research/pets in progress
- `pubspec.yaml` - Flutter dependencies

## Development

### Modify API Integration

Edit `app/lib/services/api_service.dart` to:
- Change the Clash of Clans API endpoint (currently https://api.clashofclans.com/v1)
- Add new API methods (getWarLog, getClanWarLeague, etc.)
- Modify response parsing

### Modify UI

Edit files in `app/lib/`:
- Main layout: `main.dart`
- Player search: `screens/player_search_screen.dart`
- Player details: `screens/account_details_screen.dart`
- Upgrades view: `screens/upgrades_screen.dart`

### Add Packages

Edit `app/pubspec.yaml` and run:
```bash
cd app
flutter pub get
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

## Troubleshooting

### App won't start
- Ensure `flutter doctor` shows no errors
- Run `flutter clean && flutter pub get`
- Check Flutter version: `flutter --version` (should be 3.0+)

### "Invalid API Key" error
- Verify API key in `.dart` file is correct
- Check API key is still active at https://developer.clashofclans.com/
- Try regenerating the API key

### "Player not found" error
- Verify player tag format (should start with #)
- Ensure tag exists in official Clash of Clans game

## Contributing

1. Create a feature branch from `main`
2. Make your changes
3. Test thoroughly on both Android and iOS
4. Submit a pull request

## License

See LICENSE file for details.
