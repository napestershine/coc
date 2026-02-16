# Clash of Code (CoC) - Full Stack Project

A complete full-stack application with Flutter frontend and Flask backend API.

## Project Structure

```
coc/
├── app/           # Flutter mobile/web application
├── api/           # Flask REST API backend
└── README.md      # This file
```

## Quick Start

### API Setup (Flask)

```bash
cd api

# Install dependencies
pip install -r requirements.txt

# Run the API server
python app.py
# or
./run.sh  # On macOS/Linux
run.bat   # On Windows
```

The API will be available at `http://localhost:5000`

### App Setup (Flutter)

```bash
cd app

# Get dependencies
flutter pub get

# Run the app
flutter run
# or
./run.sh  # On macOS/Linux
run.bat   # On Windows
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

### Endpoints

- `GET /` - Welcome message
- `GET /api/health` - Health check
- `GET /api/data` - Get sample data
- `POST /api/data` - Create new data

## App Development

The Flutter app is structured with:
- Material 3 design
- HTTP client for API communication
- Unit and widget tests
- Support for Android, iOS, and Web

## Project Files

### API
- `app.py` - Main Flask application
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variables template
- `run.sh` / `run.bat` - Start scripts

### App
- `lib/main.dart` - Main application entry point
- `pubspec.yaml` - Flutter dependencies and configuration
- `test/widget_test.dart` - Widget tests
- `run.sh` / `run.bat` - Start scripts

## Development

### API Development

To modify API endpoints, edit `api/app.py`:

```python
@app.route('/api/endpoint', methods=['GET', 'POST'])
def endpoint():
    return jsonify({'response': 'data'})
```

### App Development

To modify the app UI, edit `app/lib/main.dart`.

To add packages, add them to `app/pubspec.yaml` and run `flutter pub get`.

## Testing

### API
```bash
cd api
python -m pytest
```

### App
```bash
cd app
flutter test
```

## Building for Production

### App - Build APK
```bash
cd app
flutter build apk
```

### App - Build iOS
```bash
cd app
flutter build ios
```

### App - Build Web
```bash
cd app
flutter build web
```

## Environment Configuration

Copy the example environment file:

```bash
cp api/.env.example api/.env
```

Edit `api/.env` with your configuration.

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
