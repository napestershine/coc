# CoC Flutter App

A Flutter application for the Clash of Code project.

## Getting Started

### Prerequisites
- Flutter SDK (3.0.0 or higher)
- Dart SDK
- An IDE (VS Code, Android Studio, or IntelliJ)

### Installation

```bash
# Install dependencies
flutter pub get

# Run the app
flutter run
```

### Building

```bash
# Build APK (Android)
flutter build apk

# Build iOS app
flutter build ios

# Build web
flutter build web
```

## Project Structure

- `lib/` - Application source code
- `test/` - Unit and widget tests
- `android/` - Android-specific code
- `ios/` - iOS-specific code
- `web/` - Web-specific code

## Features

- Counter demo application
- HTTP package for API communication
- Material 3 design

## API Integration

The app communicates with the Flask API at `http://localhost:5000`.
