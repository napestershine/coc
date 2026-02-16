@echo off
REM Start the Flutter app on Windows

setlocal enabledelayedexpansion

echo Starting CoC Flutter App...

where flutter >nul 2>&1
if %errorlevel% neq 0 (
    echo Flutter is not installed. Please install Flutter SDK first.
    echo Visit: https://flutter.dev/docs/get-started/install
    exit /b 1
)

echo Getting dependencies...
flutter pub get

echo Running Flutter app...
flutter run

endlocal
