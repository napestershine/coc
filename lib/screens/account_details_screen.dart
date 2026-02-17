import 'package:flutter/material.dart';
import '../models/coc_account.dart';
import '../services/api_service.dart';

/// Screen for displaying detailed player account statistics
class AccountDetailsScreen extends StatefulWidget {
  final String playerTag;

  const AccountDetailsScreen({
    Key? key,
    required this.playerTag,
  }) : super(key: key);

  @override
  State<AccountDetailsScreen> createState() => _AccountDetailsScreenState();
}

class _AccountDetailsScreenState extends State<AccountDetailsScreen> {
  late Future<COCAccount?> _playerFuture;
  final _apiService = ApiService();

  @override
  void initState() {
    super.initState();
    _playerFuture = _apiService.getPlayer(widget.playerTag);
  }

  Future<void> _refreshData() async {
    setState(() {
      _playerFuture = _apiService.getPlayer(widget.playerTag);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Player Details'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _refreshData,
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: _refreshData,
        child: FutureBuilder<COCAccount?>(
          future: _playerFuture,
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
                    const Text('Failed to load player details'),
                    const SizedBox(height: 16),
                    ElevatedButton(
                      onPressed: _refreshData,
                      child: const Text('Retry'),
                    ),
                  ],
                ),
              );
            }

            final player = snapshot.data!;

            return ListView(
              padding: const EdgeInsets.all(16),
              children: [
                // Header card with player name and tag
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          player.name,
                          style: Theme.of(context).textTheme.headlineSmall,
                        ),
                        const SizedBox(height: 4),
                        Text(
                          player.tag,
                          style: Theme.of(context).textTheme.bodySmall,
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 16),

                // Main stats grid
                _buildStatsGrid(context, player),
                const SizedBox(height: 16),

                // Combat stats
                _buildSectionCard(
                  context,
                  'Combat Statistics',
                  [
                    _buildStatRow('Attack Wins', '${player.attackWins}'),
                    _buildStatRow('Defense Wins', '${player.defenseWins}'),
                  ],
                ),
                const SizedBox(height: 16),

                // Donations
                _buildSectionCard(
                  context,
                  'Donations',
                  [
                    _buildStatRow('Donated', '${player.donations}'),
                    _buildStatRow('Received', '${player.donationsReceived}'),
                  ],
                ),
                const SizedBox(height: 16),

                // Clan info
                if (player.clanTag != 'N/A')
                  _buildSectionCard(
                    context,
                    'Clan Information',
                    [
                      _buildStatRow('Clan Tag', player.clanTag),
                      _buildStatRow('Role', player.role),
                    ],
                  ),
              ],
            );
          },
        ),
      ),
    );
  }

  Widget _buildStatsGrid(BuildContext context, COCAccount player) {
    return GridView.count(
      crossAxisCount: 2,
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      mainAxisSpacing: 12,
      crossAxisSpacing: 12,
      children: [
        _buildStatCard('Town Hall', '${player.townHallLevel}', Icons.castle),
        _buildStatCard('Trophies', '${player.trophies}', Icons.emoji_events),
        _buildStatCard('Best Trophies', '${player.bestTrophies}', Icons.star),
        _buildStatCard('Exp Level', '${player.expLevel}', Icons.trending_up),
      ],
    );
  }

  Widget _buildStatCard(String title, String value, IconData icon) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 32, color: Colors.blue),
            const SizedBox(height: 8),
            Text(
              value,
              style: const TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              title,
              style: const TextStyle(fontSize: 12, color: Colors.grey),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSectionCard(
    BuildContext context,
    String title,
    List<Widget> children,
  ) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              title,
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 12),
            ...children,
          ],
        ),
      ),
    );
  }

  Widget _buildStatRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label),
          Text(
            value,
            style: const TextStyle(fontWeight: FontWeight.bold),
          ),
        ],
      ),
    );
  }
}
