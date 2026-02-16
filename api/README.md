# CoC Flask API

A Flask RESTful API for the Clash of Code project.

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the API

```bash
# Development mode
python app.py

# The API will be available at http://localhost:5000
```

## API Endpoints

### GET /
Returns welcome message and API version.

### GET /api/health
Returns health status of the API.

### GET /api/data
Returns a list of sample data items.

### POST /api/data
Accepts JSON data and returns confirmation.

**Example:**
```bash
curl -X POST http://localhost:5000/api/data \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Item"}'
```

## Environment Variables

Copy `.env.example` to `.env` and update as needed:

```bash
cp .env.example .env
```

## Project Structure

- `app.py` - Main Flask application
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variables template
