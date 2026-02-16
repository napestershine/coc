#!/bin/bash
# Start the Flutter app

echo "Starting CoC Flutter App..."
cd "$(dirname "$0")"

if ! command -v flutter &> /dev/null; then
    echo "Flutter is not installed. Please install Flutter SDK first."
    echo "Visit: https://flutter.dev/docs/get-started/install"
    exit 1
fi

echo "Getting dependencies..."
flutter pub get

echo "Running Flutter app..."
flutter run
