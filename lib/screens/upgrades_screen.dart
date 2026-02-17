import 'package:flutter/material.dart';
import '../services/api_service.dart';

/// Screen for tracking buildings, research, and pets under construction
class UpgradesScreen extends StatefulWidget {
  final String playerTag;

  const UpgradesScreen({
    Key? key,
    required this.playerTag,
  }) : super(key: key);

  @override
  State<UpgradesScreen> createState() => _UpgradesScreenState();
}

class _UpgradesScreenState extends State<UpgradesScreen> {
  late Future<Map<String, dynamic>?> _upgradesFuture;
  final _apiService = ApiService();

  @override
  void initState() {
    super.initState();
    _upgradesFuture = _apiService.getUpgrades(widget.playerTag);
  }

  Future<void> _refreshData() async {
    setState(() {
      _upgradesFuture = _apiService.getUpgrades(widget.playerTag);
    });
  }

  Duration _parseDuration(String durationStr) {
    try {
      // Format is typically "8h30m" or "2d5h"
      final hours = int.tryParse(durationStr.split('h')[0].split('d').last) ?? 0;
      final minutes = int.tryParse(durationStr.split('m').first.split('h').last) ?? 0;
      return Duration(hours: hours, minutes: minutes);
    } catch (e) {
      return Duration.zero;
    }
  }

  String _formatTimeRemaining(String? finishTime) {
    if (finishTime == null) return 'Unknown';
    try {
      final finish = DateTime.parse(finishTime);
      final now = DateTime.now();
      final difference = finish.difference(now);

      if (difference.isNegative) return 'Complete';

      final days = difference.inDays;
      final hours = difference.inHours % 24;
      final minutes = difference.inMinutes % 60;

      if (days > 0) return '${days}d ${hours}h';
      if (hours > 0) return '${hours}h ${minutes}m';
      return '${minutes}m';
    } catch (e) {
      return 'Unknown';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Upgrades In Progress'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _refreshData,
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: _refreshData,
        child: FutureBuilder<Map<String, dynamic>?>(
          future: _upgradesFuture,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const Center(child: CircularProgressIndicator());
            }

            if (snapshot.hasError || snapshot.data == null) {
              return Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Icon(Icons.error_outline, size: 48, color: Colors.red),
                    const SizedBox(height: 16),
                    const Text('Failed to load upgrades'),
                    const SizedBox(height: 16),
                    ElevatedButton(
                      onPressed: _refreshData,
                      child: const Text('Retry'),
                    ),
                  ],
                ),
              );
            }

            final upgrades = snapshot.data!;
            final buildings = upgrades['buildingsUnderConstruction'] ?? [];
            final research = upgrades['researchUnderConstruction'] ?? [];
            final pets = upgrades['petsUnderConstruction'] ?? [];

            final hasUpgrades =
                buildings.isNotEmpty || research.isNotEmpty || pets.isNotEmpty;

            if (!hasUpgrades) {
              return Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(Icons.check_circle_outline,
                        size: 64, color: Colors.green[400]),
                    const SizedBox(height: 16),
                    const Text('No upgrades in progress!'),
                    const SizedBox(height: 8),
                    const Text(
                      'All buildings, research, and pets are ready',
                      style: TextStyle(color: Colors.grey),
                    ),
                  ],
                ),
              );
            }

            return ListView(
              padding: const EdgeInsets.all(16),
              children: [
                if (buildings.isNotEmpty) ...[
                  _buildSectionTitle('Buildings Under Construction'),
                  ..._buildUpgradeCards(buildings),
                  const SizedBox(height: 16),
                ],
                if (research.isNotEmpty) ...[
                  _buildSectionTitle('Research In Progress'),
                  ..._buildUpgradeCards(research),
                  const SizedBox(height: 16),
                ],
                if (pets.isNotEmpty) ...[
                  _buildSectionTitle('Pets Being Upgraded'),
                  ..._buildUpgradeCards(pets),
                ],
              ],
            );
          },
        ),
      ),
    );
  }

  Widget _buildSectionTitle(String title) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Text(
        title,
        style: const TextStyle(
          fontSize: 16,
          fontWeight: FontWeight.bold,
        ),
      ),
    );
  }

  List<Widget> _buildUpgradeCards(List<dynamic> items) {
    return items.map((item) {
      final name = item['name'] ?? 'Unknown';
      final level = item['level'] ?? '?';
      final finishTime = item['finishTime'];
      final timeRemaining = _formatTimeRemaining(finishTime);

      return Card(
        margin: const EdgeInsets.symmetric(vertical: 8),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          name,
                          style: const TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 4),
                        Text(
                          'Level $level',
                          style: const TextStyle(
                            fontSize: 12,
                            color: Colors.grey,
                          ),
                        ),
                      ],
                    ),
                  ),
                  Chip(
                    label: Text(timeRemaining),
                    backgroundColor:
                        timeRemaining == 'Complete' ? Colors.green : Colors.orange,
                    labelStyle: const TextStyle(color: Colors.white),
                  ),
                ],
              ),
              if (finishTime != null) ...[
                const SizedBox(height: 12),
                ClipRRect(
                  borderRadius: BorderRadius.circular(4),
                  child: LinearProgressIndicator(
                    minHeight: 8,
                    value: _calculateProgress(finishTime),
                  ),
                ),
              ],
            ],
          ),
        ),
      );
    }).toList();
  }

  double _calculateProgress(String finishTime) {
    try {
      // This is simplified - would need startTime for accurate progress
      // For now, just return a placeholder
      return 0.65;
    } catch (e) {
      return 0;
    }
  }
}
