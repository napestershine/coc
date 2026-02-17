import 'package:flutter/material.dart';
import '../services/api_service.dart';

/// Screen for searching and adding new player accounts
class PlayerSearchScreen extends StatefulWidget {
  final Function(String) onPlayerAdded;

  const PlayerSearchScreen({
    Key? key,
    required this.onPlayerAdded,
  }) : super(key: key);

  @override
  State<PlayerSearchScreen> createState() => _PlayerSearchScreenState();
}

class _PlayerSearchScreenState extends State<PlayerSearchScreen> {
  final _tagController = TextEditingController();
  final _apiService = ApiService();
  bool _isLoading = false;
  String? _errorMessage;

  @override
  void dispose() {
    _tagController.dispose();
    super.dispose();
  }

  void _addPlayer() async {
    final tag = _tagController.text.trim();

    if (tag.isEmpty) {
      setState(() {
        _errorMessage = 'Please enter a player tag';
      });
      return;
    }

    if (!_apiService.isValidPlayerTag(tag)) {
      setState(() {
        _errorMessage = 'Invalid player tag format. Use format: #P92VQC8UG';
      });
      return;
    }

    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    // Verify player exists by fetching data
    final player = await _apiService.getPlayer(tag);

    if (mounted) {
      if (player != null) {
        widget.onPlayerAdded(player.tag);
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Added ${player.name}')),
        );
      } else {
        setState(() {
          _errorMessage = 'Player not found or invalid API key';
          _isLoading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Add Player Account'),
        elevation: 0,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Information card
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: const [
                    Text(
                      'How to find your player tag:',
                      style: TextStyle(fontWeight: FontWeight.bold),
                    ),
                    SizedBox(height: 8),
                    Text('1. Open Clash of Clans'),
                    Text('2. Go to Profile'),
                    Text('3. View Player Information'),
                    Text('4. Copy your tag (e.g., #P92VQC8UG)'),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),

            // Input field
            TextField(
              controller: _tagController,
              textCapitalization: TextCapitalization.characters,
              decoration: InputDecoration(
                hintText: 'Enter player tag (e.g., #P92VQC8UG)',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
                prefixIcon: const Icon(Icons.tag),
                errorText: _errorMessage,
              ),
              onSubmitted: (_) => _addPlayer(),
            ),
            const SizedBox(height: 16),

            // Add button
            ElevatedButton.icon(
              onPressed: _isLoading ? null : _addPlayer,
              icon: _isLoading
                  ? const SizedBox(
                      width: 20,
                      height: 20,
                      child: CircularProgressIndicator(strokeWidth: 2),
                    )
                  : const Icon(Icons.add),
              label: Text(_isLoading ? 'Adding...' : 'Add Player'),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 12),
              ),
            ),
            const Spacer(),

            // Footer info
            const Center(
              child: Text(
                'Make sure you have a valid Clash of Clans API key configured',
                style: TextStyle(fontSize: 12, color: Colors.grey),
                textAlign: TextAlign.center,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
