# Clash of Clans Account Manager API Documentation

## Overview

The Clash of Clans Account Manager API is a Flask-based REST API that integrates with the official Clash of Clans API to track and manage multiple player accounts.

- **Framework**: Flask 3.0.0
- **Python**: 3.8+
- **External API**: [Clash of Clans Official API](https://api.clashofclans.com/v1)

## Base URL

```
http://localhost:5000
```

## Authentication

The backend API currently requires no authentication for local use. However, it uses a Bearer token to authenticate with the official Clash of Clans API.

### Setting Up Clash of Clans API Key

1. Visit [developer.clashofclans.com](https://developer.clashofclans.com)
2. Create an account and register an application
3. Generate an API token
4. Add to `api/.env`:
   ```
   COC_API_KEY=your_api_key_here
   ```
5. Without an API key, the system runs in **demo mode** with generated mock data

## Response Format

All endpoints return JSON responses with the following structure:

**Success Response:**
```json
{
  "success": true,
  "data": {},
  "message": "Optional message"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Error message",
  "status": 400
}
```

## Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created
- `400 Bad Request` - Invalid request
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## General Endpoints

### Health Check

**GET** `/api/health`

Check if the API is running and healthy.

**Response:**
```json
{
  "status": "healthy",
  "service": "clash-of-clans-api",
  "version": "2.0.0"
}
```

---

## Account Management Endpoints

### List All Accounts

**GET** `/api/accounts`

Retrieve all tracked Clash of Clans accounts.

**Response:**
```json
{
  "success": true,
  "count": 2,
  "data": [
    {
      "id": 1,
      "player_tag": "#P92VQC8UG",
      "player_info": {
        "name": "Player_C8UG",
        "town_hall_level": 11,
        "trophies": 7503,
        "best_trophies": 4577,
        "war_stars": 281,
        "exp_level": 89,
        "attack_wins": 444,
        "defense_wins": 185,
        "clan_name": "Dragon Force",
        "clan_rank": "#34",
        "role": "leader",
        "troops_trained": 19,
        "spells_trained": 4,
        "heroes_upgraded": 4,
        "threat_level": "Critical"
      },
      "clan_info": {
        "name": "Demo Clan",
        "tag": "#P92VQC8UG",
        "badge_url": "https://via.placeholder.com/64"
      },
      "created_at": "2026-02-16T15:42:59.204322",
      "last_updated": "2026-02-16T15:42:59.204358"
    }
  ]
}
```

---

### Add New Account

**POST** `/api/accounts`

Add a new Clash of Clans player account to track.

**Request Body:**
```json
{
  "player_tag": "#P92VQC8UG"
}
```

**Player Tag Format:**
- Must be alphanumeric string starting with `#`
- Example: `#P92VQC8UG`
- Find in-game under Profile → Player Information

**Response (Success - 201):**
```json
{
  "success": true,
  "message": "Account #P92VQC8UG added successfully",
  "data": {
    "id": 1,
    "player_tag": "#P92VQC8UG",
    "player_info": {
      "name": "Player_C8UG",
      "town_hall_level": 11,
      "trophies": 7503,
      "best_trophies": 4577,
      "war_stars": 281,
      "exp_level": 89,
      "attack_wins": 444,
      "defense_wins": 185,
      "clan_name": "Dragon Force",
      "clan_rank": "#34",
      "role": "leader",
      "troops_trained": 19,
      "spells_trained": 4,
      "heroes_upgraded": 4,
      "threat_level": "Critical"
    },
    "clan_info": {
      "name": "Demo Clan",
      "tag": "#P92VQC8UG",
      "badge_url": "https://via.placeholder.com/64"
    },
    "created_at": "2026-02-16T15:42:59.204322",
    "last_updated": "2026-02-16T15:42:59.204358"
  }
}
```

**Error Cases:**
- Invalid player tag format: `400 Bad Request`
- Player not found in API: `404 Not Found`
- API key invalid: `401 Unauthorized`

---

### Get Account Details

**GET** `/api/accounts/<id>`

Get detailed information for a specific account. Automatically refreshes data from Clash of Clans API.

**Path Parameters:**
- `id` (integer): Account ID

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "player_tag": "#P92VQC8UG",
    "player_info": {
      "name": "Player_C8UG",
      "town_hall_level": 11,
      "trophies": 7503,
      "best_trophies": 4577,
      "war_stars": 281,
      "exp_level": 89,
      "attack_wins": 444,
      "defense_wins": 185,
      "clan_name": "Dragon Force",
      "clan_rank": "#34",
      "role": "leader",
      "troops_trained": 19,
      "spells_trained": 4,
      "heroes_upgraded": 4,
      "threat_level": "Critical"
    },
    "clan_info": {
      "name": "Demo Clan",
      "tag": "#P92VQC8UG",
      "badge_url": "https://via.placeholder.com/64"
    },
    "created_at": "2026-02-16T15:42:59.204322",
    "last_updated": "2026-02-16T15:42:59.204358"
  }
}
```

---

### Get Account Statistics

**GET** `/api/accounts/<id>/stats`

Get comprehensive statistics including clan information and troop data.

**Path Parameters:**
- `id` (integer): Account ID

**Response:**
```json
{
  "success": true,
  "data": {
    "account_id": 1,
    "player_tag": "#P92VQC8UG",
    "player_info": {
      "name": "Player_C8UG",
      "town_hall_level": 11,
      "trophies": 7503,
      "best_trophies": 4577,
      "war_stars": 281,
      "exp_level": 89,
      "attack_wins": 444,
      "defense_wins": 185,
      "clan_name": "Dragon Force",
      "clan_rank": "#34",
      "role": "leader",
      "troops_trained": 19,
      "spells_trained": 4,
      "heroes_upgraded": 4,
      "threat_level": "Critical"
    },
    "clan_info": {
      "name": "Dragon Force Clan",
      "tag": "#P92VQC8UG",
      "members": 18,
      "clan_level": 19,
      "clan_points": 27693,
      "is_open": false,
      "description": "Join us for epic wars and donations!",
      "war_frequency": "never",
      "war_wins": 80,
      "war_losses": 69,
      "war_draws": 17,
      "badge_url": "https://via.placeholder.com/64"
    },
    "troops": [
      {
        "name": "Barbarian",
        "level": 1,
        "max_level": 10
      },
      {
        "name": "Archer",
        "level": 7,
        "max_level": 10
      },
      {
        "name": "Giant",
        "level": 5,
        "max_level": 10
      }
    ]
  }
}
```

**Clan Info Fields:**
- `clan_level` - Current clan level (1-24)
- `clan_points` - Clan trophy points
- `members` - Number of members in clan
- `war_wins` - Total clan war victories
- `war_losses` - Total clan war defeats
- `war_draws` - Total clan war draws
- `war_frequency` - War activity level

---

### Refresh Account Data

**POST** `/api/accounts/<id>/refresh`

Force immediate refresh of account data from Clash of Clans API.

**Path Parameters:**
- `id` (integer): Account ID

**Response:**
```json
{
  "success": true,
  "message": "Account data refreshed successfully",
  "data": {
    "id": 1,
    "player_tag": "#P92VQC8UG",
    "player_info": {
      "name": "Player_C8UG",
      "town_hall_level": 11,
      "trophies": 7503
    },
    "last_updated": "2026-02-16T15:43:00.000000"
  }
}
```

---

### Delete Account

**DELETE** `/api/accounts/<id>`

Remove an account from tracking. Data is permanently deleted.

**Path Parameters:**
- `id` (integer): Account ID

**Response:**
```json
{
  "success": true,
  "message": "Account deleted successfully"
}
```

---

## Data Fields Reference

### Player Info Object

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Player name |
| `town_hall_level` | integer | Town Hall level (1-14+) |
| `trophies` | integer | Current trophy count |
| `best_trophies` | integer | Highest trophy count reached |
| `war_stars` | integer | Total war stars earned |
| `exp_level` | integer | Experience level |
| `attack_wins` | integer | Total attack victories |
| `defense_wins` | integer | Total defense victories |
| `clan_name` | string | Current clan name or null |
| `clan_rank` | string | Rank within clan (e.g., "#34") or null |
| `role` | string | Clan role: "leader", "coLeader", "member", "elder" |
| `troops_trained` | integer | Number of unique troops trained |
| `spells_trained` | integer | Number of unique spells trained |
| `heroes_upgraded` | integer | Number of heroes with levels > 0 |
| `threat_level` | string | Player threat level based on Town Hall |

### Clan Info Object

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Clan name |
| `tag` | string | Clan tag (e.g., "#P92VQC8UG") |
| `members` | integer | Number of members in clan |
| `clan_level` | integer | Clan level (1-24) |
| `clan_points` | integer | Clan trophy points |
| `is_open` | boolean | Recruitment status |
| `description` | string | Clan description |
| `war_frequency` | string | War activity frequency |
| `war_wins` | integer | Total war victories |
| `war_losses` | integer | Total war losses |
| `war_draws` | integer | Total war draws |
| `badge_url` | string | URL to clan badge image |

### Troop Object

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Troop name (e.g., "Barbarian") |
| `level` | integer | Current troop level |
| `max_level` | integer | Maximum troop level for Town Hall |

---

## Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "error": "Invalid player tag format",
  "status": 400
}
```

### 404 Not Found
```json
{
  "success": false,
  "error": "Account not found",
  "status": 404
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "error": "Internal server error",
  "status": 500
}
```

---

## Common Use Cases

### Get All Player Names and Town Hall Levels
```bash
curl http://localhost:5000/api/accounts | jq '.data[] | {name: .player_info.name, th: .player_info.town_hall_level}'
```

### Get Highest Trophy Players
```bash
curl http://localhost:5000/api/accounts | jq '.data | sort_by(.player_info.trophies) | reverse[] | {name: .player_info.name, trophies: .player_info.trophies}'
```

### Get Clan Information for an Account
```bash
curl http://localhost:5000/api/accounts/1/stats | jq '.data.clan_info'
```

### Refresh All Accounts
```bash
for id in $(curl -s http://localhost:5000/api/accounts | jq '.data[].id'); do
  curl -X POST http://localhost:5000/api/accounts/$id/refresh
done
```

---

## Rate Limiting

The official Clash of Clans API allows:
- 30 requests per 1 second maximum
- 300,000 requests per 24 hours

The local API does not currently enforce rate limiting, but exceeding the official API limits will result in errors.

---

## Demo Mode

When `COC_API_KEY` is not set, the API runs in **demo mode** and generates realistic mock data. This is useful for:
- Testing without an API key
- Development
- UI testing

Mock data includes:
- Realistic Town Hall levels (5-13)
- Trophy counts (1000-7500)
- War statistics
- Clan information
- Troop data

---

## Troubleshooting

### "Invalid player tag format" Error
- Ensure player tag starts with `#`
- Player tag must be alphanumeric only
- Example: `#P92VQC8UG` ✓

### "Player not found" Error
- Verify player tag is correct
- Check Clash of Clans API key if using live data
- Player may have changed tag (inactive players are archived)

### Slow Response Times
- First request for a player requires fetching from external API
- Subsequent requests for same player are faster (local cache)
- Use `/refresh` endpoint for guaranteed fresh data

### Empty Clan Info
- Player must be in a clan to return clan data
- `clan_name`, `clan_rank`, `role` will be null if not in clan

---

## Version History

### v2.0.0 (Current)
- Clash of Clans API integration
- Player tag-based tracking
- Comprehensive player statistics
- Clan information and war data
- Mock data generation for demo mode

---

## Support

For issues or questions:
1. Check the [main README](../README.md)
2. Review the [Integration Guide](../INTEGRATION.md)
3. Verify API is running: `curl http://localhost:5000/api/health`
