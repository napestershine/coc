# CoC Account Manager API Documentation

## Overview

The CoC Account Manager API is a Flask-based REST API that allows you to track and manage multiple Clash of Code accounts in one place.

## Base URL

```
http://localhost:5000
```

## Authentication

Currently, no authentication is required. In production, implement JWT or similar authentication.

## General Endpoints

### Health Check

**GET** `/api/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "coc-api",
  "version": "1.0.0"
}
```

---

## Account Management Endpoints

### List All Accounts

**GET** `/api/accounts`

Get all managed Clash of Code accounts.

**Response:**
```json
{
  "success": true,
  "count": 2,
  "data": [
    {
      "id": 1,
      "username": "player123",
      "created_at": "2024-02-16T12:30:45.123456",
      "last_updated": "2024-02-16T15:45:20.654321",
      "stats": {
        "level": 25,
        "rank": "#1523",
        "global_rank": "#45231",
        "clashes_count": 156,
        "wins": 89,
        "win_rate": "57%",
        "country": "US",
        "bio": "CoC Player - player123"
      },
      "current_clash": null,
      "is_online": true
    }
  ]
}
```

---

### Add New Account

**POST** `/api/accounts`

Add a new Clash of Code account to track.

**Request Body:**
```json
{
  "username": "player123"
}
```

**Response (Success - 201):**
```json
{
  "success": true,
  "message": "Account player123 added successfully",
  "data": {
    "id": 1,
    "username": "player123",
    "created_at": "2024-02-16T12:30:45.123456",
    "last_updated": "2024-02-16T12:30:45.123456",
    "stats": {
      "level": 25,
      "rank": "#1523",
      "global_rank": "#45231",
      "clashes_count": 156,
      "wins": 89,
      "win_rate": "57%",
      "country": "US",
      "bio": "CoC Player - player123"
    },
    "current_clash": null,
    "is_online": true
  }
}
```

**Response (Error - 400/404):**
```json
{
  "success": false,
  "error": "Username is required"
}
```

---

### Get Account Details

**GET** `/api/accounts/<account_id>`

Get details of a specific account with latest data from CoC.

**URL Parameters:**
- `account_id` (required): Numeric ID of the account

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "player123",
    "created_at": "2024-02-16T12:30:45.123456",
    "last_updated": "2024-02-16T15:45:20.654321",
    "stats": {
      "level": 25,
      "rank": "#1523",
      "global_rank": "#45231",
      "clashes_count": 156,
      "wins": 89,
      "win_rate": "57%",
      "country": "US",
      "bio": "CoC Player - player123"
    },
    "current_clash": null,
    "is_online": true
  }
}
```

---

### Get Account Statistics

**GET** `/api/accounts/<account_id>/stats`

Get detailed statistics and clash history for an account.

**URL Parameters:**
- `account_id` (required): Numeric ID of the account

**Response:**
```json
{
  "success": true,
  "data": {
    "account_id": 1,
    "username": "player123",
    "stats": {
      "level": 25,
      "rank": "#1523",
      "global_rank": "#45231",
      "clashes_count": 156,
      "wins": 89,
      "win_rate": "57%",
      "country": "US",
      "bio": "CoC Player - player123"
    },
    "current_clash": {
      "is_in_clash": false,
      "time_remaining": 0,
      "mode": null,
      "language": null
    },
    "recent_clashes": [
      {
        "id": 1,
        "mode": "Shortest",
        "language": "Python",
        "score": 100,
        "result": "Win",
        "date": "2024-02-16T15:30:00.000000"
      }
    ]
  }
}
```

---

### Delete Account

**DELETE** `/api/accounts/<account_id>`

Remove an account from tracking.

**URL Parameters:**
- `account_id` (required): Numeric ID of the account

**Response:**
```json
{
  "success": true,
  "message": "Account player123 removed successfully"
}
```

---

### Refresh Account Data

**POST** `/api/accounts/<account_id>/refresh`

Manually refresh account data from CoC.

**URL Parameters:**
- `account_id` (required): Numeric ID of the account

**Response:**
```json
{
  "success": true,
  "message": "Account refreshed successfully",
  "data": {
    "id": 1,
    "username": "player123",
    "created_at": "2024-02-16T12:30:45.123456",
    "last_updated": "2024-02-16T15:45:20.654321",
    "stats": {
      "level": 25,
      "rank": "#1523",
      "global_rank": "#45231",
      "clashes_count": 157,
      "wins": 90,
      "win_rate": "57%",
      "country": "US",
      "bio": "CoC Player - player123"
    },
    "current_clash": null,
    "is_online": false
  }
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "error": "Username is required"
}
```

### 404 Not Found
```json
{
  "success": false,
  "error": "Account not found"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "error": "Internal server error"
}
```

---

## cURL Examples

### Add Account
```bash
curl -X POST http://localhost:5000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{"username": "player123"}'
```

### List Accounts
```bash
curl http://localhost:5000/api/accounts
```

### Get Account Details
```bash
curl http://localhost:5000/api/accounts/1
```

### Get Account Stats
```bash
curl http://localhost:5000/api/accounts/1/stats
```

### Refresh Account
```bash
curl -X POST http://localhost:5000/api/accounts/1/refresh
```

### Delete Account
```bash
curl -X DELETE http://localhost:5000/api/accounts/1
```

---

## Rate Limiting

Currently, no rate limiting is implemented. In production, implement rate limiting to prevent abuse.

---

## Future Enhancements

- [] Authentication & Authorization (JWT)
- [] Database persistence (SQLite/PostgreSQL)
- [] Real-time notifications for clash events
- [] Advanced filtering and sorting
- [] Clash statistics aggregation
- [] Leaderboard rankings
- [] Performance optimizations with caching
