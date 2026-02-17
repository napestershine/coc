import 'package:flutter/material.dart';
import 'models/coc_account.dart';
import 'services/api_service.dart';
import 'screens/player_search_screen.dart';
import 'screens/account_details_screen.dart';
import 'screens/upgrades_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Clash of Clans Manager',
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.orange,
          brightness: Brightness.light,
        ),
      ),
      darkTheme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.orange,
          brightness: Brightness.dark,
        ),
      ),
      themeMode: ThemeMode.system,
      home: const MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({Key? key}) : super(key: key);

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  final List<String> _playerTags = [];
  final _apiService = ApiService();

  void _addPlayer(String playerTag) {
    if (!_playerTags.contains(playerTag)) {
      setState(() {
        _playerTags.add(playerTag);
      });
    }
  }

  void _removePlayer(String playerTag) {
    setState(() {
      _playerTags.remove(playerTag);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Clash of Clans Manager'),
        elevation: 0,
      ),
      body: _playerTags.isEmpty
          ? _buildEmptyState(context)
          : _buildPlayerList(context),
      floatingActionButton: FloatingActionButton(
        onPressed: () => Navigator.of(context).push(
          MaterialPageRoute(
            builder: (context) => PlayerSearchScreen(
              onPlayerAdded: _addPlayer,
            ),
          ),
        ),
        tooltip: 'Add Player',
        child: const Icon(Icons.add),
      ),
    );
  }

  Widget _buildEmptyState(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.sports_esports,
            size: 64,
            color: Colors.grey[400],
          ),
          const SizedBox(height: 16),
          const Text(
            'No Accounts Yet',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 8),
          const Text(
            'Tap the + button to add your first account',
            style: TextStyle(color: Colors.grey),
          ),
          const SizedBox(height: 24),
          ElevatedButton.icon(
            onPressed: () => Navigator.of(context).push(
              MaterialPageRoute(
                builder: (context) => PlayerSearchScreen(
                  onPlayerAdded: _addPlayer,
                ),
              ),
            ),
            icon: const Icon(Icons.add),
            label: const Text('Add Your First Account'),
          ),
        ],
      ),
    );
  }

  Widget _buildPlayerList(BuildContext context) {
    return ListView.builder(
      padding: const EdgeInsets.all(12),
      itemCount: _playerTags.length,
      itemBuilder: (context, index) {
        final playerTag = _playerTags[index];
        return _buildPlayerCard(context, playerTag);
      },
    );
  }

  Widget _buildPlayerCard(BuildContext context, String playerTag) {
    return FutureBuilder<COCAccount?>(
      future: _apiService.getPlayer(playerTag),
      builder: (context, snapshot) {
        return Card(
          margin: const EdgeInsets.symmetric(vertical: 8),
          child: InkWell(
            onTap: () => Navigator.of(context).push(
              MaterialPageRoute(
                builder: (context) => AccountDetailsScreen(
                  playerTag: playerTag,
                ),
              ),
            ),
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
                            if (snapshot.hasData)
                              Text(
                                snapshot.data!.name,
                                style: const TextStyle(
                                  fontSize: 18,
                                  fontWeight: FontWeight.bold,
                                ),
                                maxLines: 1,
                                overflow: TextOverflow.ellipsis,
                              )
                            else
                              const Text(
                                'Loading...',
                                style: TextStyle(
                                  fontSize: 18,
                                  fontWeight: FontWeight.bold,
                                  color: Colors.grey,
                                ),
                              ),
                            const SizedBox(height: 4),
                            Text(
                              playerTag,
                              style: const TextStyle(
                                fontSize: 12,
                                color: Colors.grey,
                              ),
                            ),
                          ],
                        ),
                      ),
                      if (snapshot.hasData) ...[
                        PopupMenuButton(
                          itemBuilder: (context) => [
                            PopupMenuItem(
                              child: const Text('View Upgrades'),
                              onTap: () => Navigator.of(context).push(
                                MaterialPageRoute(
                                  builder: (context) => UpgradesScreen(
                                    playerTag: playerTag,
                                  ),
                                ),
                              ),
                            ),
                            PopupMenuItem(
                              child: const Text('Delete'),
                              onTap: () => _showDeleteConfirmation(
                                context,
                                playerTag,
                                snapshot.data!.name,
                              ),
                            ),
                          ],
                        ),
                      ],
                    ],
                  ),
                  if (snapshot.hasData) ...[
                    const SizedBox(height: 12),
                    Row(
                      children: [
                        _buildStatChip(
                          'TH ${snapshot.data!.townHallLevel}',
                          Colors.blue,
                        ),
                        const SizedBox(width: 8),
                        _buildStatChip(
                          '${snapshot.data!.trophies} 🏆',
                          Colors.orange,
                        ),
                        const SizedBox(width: 8),
                        if (snapshot.data!.clanTag != 'N/A')
                          _buildStatChip(
                            snapshot.data!.clanTag,
                            Colors.green,
                          ),
                      ],
                    ),
                  ],
                ],
              ),
            ),
          ),
        );
      },
    );
  }

  Widget _buildStatChip(String label, Color color) {
    return Chip(
      label: Text(label),
      backgroundColor: color.withOpacity(0.2),
      labelStyle: TextStyle(color: color, fontWeight: FontWeight.bold),
      side: BorderSide(color: color),
    );
  }

  void _showDeleteConfirmation(
    BuildContext context,
    String playerTag,
    String playerName,
  ) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Delete Account?'),
        content: Text('Remove $playerName ($playerTag) from your tracker?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () {
              _removePlayer(playerTag);
              Navigator.pop(context);
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('Deleted $playerName')),
              );
            },
            child: const Text('Delete', style: TextStyle(color: Colors.red)),
          ),
        ],
      ),
    );
  }
}
