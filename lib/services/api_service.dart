import 'package:http/http.dart' as http;
import 'dart:convert';
import '../models/coc_account.dart';

/// Singleton HTTP client for Clash of Clans API
/// Replace with your actual API key from https://developer.clashofclans.com/
const String COC_API_KEY = 'YOUR_API_KEY_HERE';
const String COC_API_BASE_URL = 'https://api.clashofclans.com/v1';

class ApiService {
  static final ApiService _instance = ApiService._internal();

  factory ApiService() {
    return _instance;
  }

  ApiService._internal();

  /// Build authorization headers with API key
  Map<String, String> _getHeaders() => {
    'Authorization': 'Bearer $COC_API_KEY',
    'Content-Type': 'application/json',
  };

  /// Fetch player information from Clash of Clans API
  /// 
  /// Parameters:
  /// - [playerTag]: Player tag (e.g., '#P92VQC8UG')
  /// 
  /// Returns: COCAccount object or null if error occurs
  Future<COCAccount?> getPlayer(String playerTag) async {
    try {
      // Ensure tag starts with #
      if (!playerTag.startsWith('#')) {
        playerTag = '#$playerTag';
      }

      // URL encode the tag for API call
      final encodedTag = Uri.encodeComponent(playerTag);
      final url = Uri.parse('$COC_API_BASE_URL/players/$encodedTag');

      final response = await http.get(url, headers: _getHeaders()).timeout(
        const Duration(seconds: 10),
        onTimeout: () => throw Exception('Request timeout'),
      );

      if (response.statusCode == 200) {
        final json = jsonDecode(response.body);
        return COCAccount.fromJson(json);
      } else if (response.statusCode == 404) {
        throw Exception('Player not found');
      } else if (response.statusCode == 403) {
        throw Exception('Invalid API key or insufficient permissions');
      } else {
        throw Exception('Failed to fetch player: ${response.statusCode}');
      }
    } catch (e) {
      print('Error fetching player: $e');
      return null;
    }
  }

  /// Fetch clan information from Clash of Clans API
  /// 
  /// Parameters:
  /// - [clanTag]: Clan tag (e.g., '#2P8G2GYQG')
  /// 
  /// Returns: Map containing clan data or null if error occurs
  Future<Map<String, dynamic>?> getClan(String clanTag) async {
    try {
      // Ensure tag starts with #
      if (!clanTag.startsWith('#')) {
        clanTag = '#$clanTag';
      }

      // URL encode the tag for API call
      final encodedTag = Uri.encodeComponent(clanTag);
      final url = Uri.parse('$COC_API_BASE_URL/clans/$encodedTag');

      final response = await http.get(url, headers: _getHeaders()).timeout(
        const Duration(seconds: 10),
        onTimeout: () => throw Exception('Request timeout'),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else if (response.statusCode == 404) {
        throw Exception('Clan not found');
      } else {
        throw Exception('Failed to fetch clan: ${response.statusCode}');
      }
    } catch (e) {
      print('Error fetching clan: $e');
      return null;
    }
  }

  /// Extract upgrade information from player data
  /// 
  /// Parameters:
  /// - [playerTag]: Player tag to fetch upgrades for
  /// 
  /// Returns: Map with upgrade data (buildingsUnderConstruction, researchUnderConstruction, etc.)
  Future<Map<String, dynamic>?> getUpgrades(String playerTag) async {
    try {
      final player = await getPlayer(playerTag);
      if (player != null) {
        return {
          'buildingsUnderConstruction': player.buildingsUnderConstruction ?? [],
          'researchUnderConstruction': player.researchUnderConstruction ?? [],
          'petsUnderConstruction': player.petsUnderConstruction ?? [],
        };
      }
      return null;
    } catch (e) {
      print('Error fetching upgrades: $e');
      return null;
    }
  }

  /// Validate player tag format
  /// 
  /// Parameters:
  /// - [playerTag]: Tag to validate
  /// 
  /// Returns: true if valid, false otherwise
  bool isValidPlayerTag(String playerTag) {
    // Player tags: # followed by 8-9 alphanumeric characters
    final pattern = RegExp(r'^#[A-Z0-9]{8,9}$');
    
    String normalizedTag = playerTag.toUpperCase();
    if (!normalizedTag.startsWith('#')) {
      normalizedTag = '#$normalizedTag';
    }
    
    return pattern.hasMatch(normalizedTag);
  }
}
