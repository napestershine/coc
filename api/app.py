from flask import Flask, jsonify, request
from models import (
    create_account, get_account, get_all_accounts, delete_account,
    update_player_info, update_clan_info, update_troop_stats
)
from coc_service import ClashOfClansService
import logging

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# GENERAL ENDPOINTS
# ============================================================================

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Welcome to Clash of Clans Account Manager API',
        'version': '2.0.0',
        'endpoints': {
            'accounts': '/api/accounts',
            'health': '/api/health'
        }
    })


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'clash-of-clans-api',
        'version': '2.0.0'
    })


# ============================================================================
# CLASH OF CLANS ACCOUNT MANAGEMENT ENDPOINTS
# ============================================================================

@app.route('/api/accounts', methods=['GET'])
def list_accounts():
    """Get all managed Clash of Clans accounts"""
    try:
        accounts = get_all_accounts()
        return jsonify({
            'success': True,
            'count': len(accounts),
            'data': accounts
        })
    except Exception as e:
        logger.error(f"Error listing accounts: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/accounts', methods=['POST'])
def add_account():
    """Add a new Clash of Clans account to track"""
    try:
        data = request.get_json()
        
        if not data or 'player_tag' not in data:
            return jsonify({'success': False, 'error': 'player_tag is required'}), 400
        
        player_tag = data.get('player_tag', '').strip()
        
        if not player_tag:
            return jsonify({'success': False, 'error': 'player_tag cannot be empty'}), 400
        
        # Ensure player_tag starts with #
        if not player_tag.startswith('#'):
            player_tag = '#' + player_tag
        
        # Fetch player data from Clash of Clans
        player_data = ClashOfClansService.get_player_data(player_tag)
        
        if not player_data:
            return jsonify({'success': False, 'error': 'Could not fetch player data'}), 404
        
        # Create account entry
        account = create_account(player_tag)
        
        # Update with fetched player info
        player_info = {
            'name': player_data.get('name', 'Unknown'),
            'town_hall_level': player_data.get('town_hall_level', 0),
            'exp_level': player_data.get('exp_level', 0),
            'trophies': player_data.get('trophies', 0),
            'best_trophies': player_data.get('best_trophies', 0),
            'war_stars': player_data.get('war_stars', 0),
            'attack_wins': player_data.get('attack_wins', 0),
            'defense_wins': player_data.get('defense_wins', 0),
            'clan_name': player_data.get('clan_name', 'No Clan'),
            'clan_rank': player_data.get('clan_rank', 'N/A'),
            'role': player_data.get('role', 'N/A'),
            'troops_trained': player_data.get('troops_trained', 0),
            'spells_trained': player_data.get('spells_trained', 0),
            'heroes_upgraded': player_data.get('heroes_upgraded', 0),
            'threat_level': player_data.get('threat_level', 'N/A')
        }
        
        updated_account = update_player_info(account['id'], player_info)
        
        # Store clan info if available
        if player_data.get('clan_info'):
            update_clan_info(account['id'], player_data['clan_info'])
            updated_account = get_account(account['id'])
        
        return jsonify({
            'success': True,
            'message': f'Account {player_tag} added successfully',
            'data': updated_account
        }), 201
        
    except Exception as e:
        logger.error(f"Error adding account: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/accounts/<int:account_id>', methods=['GET'])
def get_account_details(account_id):
    """Get details of a specific account"""
    try:
        account = get_account(account_id)
        
        if not account:
            return jsonify({'success': False, 'error': 'Account not found'}), 404
        
        # Fetch fresh data from Clash of Clans
        player_data = ClashOfClansService.get_player_data(account['player_tag'])
        
        if player_data:
            player_info = {
                'name': player_data.get('name', 'Unknown'),
                'town_hall_level': player_data.get('town_hall_level', 0),
                'exp_level': player_data.get('exp_level', 0),
                'trophies': player_data.get('trophies', 0),
                'best_trophies': player_data.get('best_trophies', 0),
                'war_stars': player_data.get('war_stars', 0),
                'attack_wins': player_data.get('attack_wins', 0),
                'defense_wins': player_data.get('defense_wins', 0),
                'clan_name': player_data.get('clan_name', 'No Clan'),
                'clan_rank': player_data.get('clan_rank', 'N/A'),
                'role': player_data.get('role', 'N/A'),
                'troops_trained': player_data.get('troops_trained', 0),
                'spells_trained': player_data.get('spells_trained', 0),
                'heroes_upgraded': player_data.get('heroes_upgraded', 0),
                'threat_level': player_data.get('threat_level', 'N/A')
            }
            account = update_player_info(account_id, player_info)
            
            if player_data.get('clan_info'):
                update_clan_info(account_id, player_data['clan_info'])
                account = get_account(account_id)
        
        return jsonify({
            'success': True,
            'data': account
        })
        
    except Exception as e:
        logger.error(f"Error getting account details: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/accounts/<int:account_id>/stats', methods=['GET'])
def get_account_stats(account_id):
    """Get detailed statistics for a specific account"""
    try:
        account = get_account(account_id)
        
        if not account:
            return jsonify({'success': False, 'error': 'Account not found'}), 404
        
        player_tag = account['player_tag']
        
        # Fetch fresh stats
        player_data = ClashOfClansService.get_player_data(player_tag)
        clan_info = ClashOfClansService.get_clan_info(
            player_data.get('clan_info', {}).get('tag', '') if player_data else ''
        )
        troop_data = ClashOfClansService.get_troop_data(player_tag)
        
        return jsonify({
            'success': True,
            'data': {
                'account_id': account_id,
                'player_tag': player_tag,
                'player_info': account.get('player_info', {}),
                'clan_info': clan_info,
                'troops': troop_data.get('troops', []) if troop_data else []
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting account stats: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/accounts/<int:account_id>', methods=['DELETE'])
def delete_account_endpoint(account_id):
    """Remove an account from tracking"""
    try:
        account = get_account(account_id)
        
        if not account:
            return jsonify({'success': False, 'error': 'Account not found'}), 404
        
        player_tag = account['player_tag']
        delete_account(account_id)
        
        return jsonify({
            'success': True,
            'message': f'Account {player_tag} removed successfully'
        })
        
    except Exception as e:
        logger.error(f"Error deleting account: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/accounts/<int:account_id>/refresh', methods=['POST'])
def refresh_account(account_id):
    """Refresh account data from Clash of Clans"""
    try:
        account = get_account(account_id)
        
        if not account:
            return jsonify({'success': False, 'error': 'Account not found'}), 404
        
        player_tag = account['player_tag']
        player_data = ClashOfClansService.get_player_data(player_tag)
        
        if not player_data:
            return jsonify({'success': False, 'error': 'Could not fetch player data'}), 404
        
        player_info = {
            'name': player_data.get('name', 'Unknown'),
            'town_hall_level': player_data.get('town_hall_level', 0),
            'exp_level': player_data.get('exp_level', 0),
            'trophies': player_data.get('trophies', 0),
            'best_trophies': player_data.get('best_trophies', 0),
            'war_stars': player_data.get('war_stars', 0),
            'attack_wins': player_data.get('attack_wins', 0),
            'defense_wins': player_data.get('defense_wins', 0),
            'clan_name': player_data.get('clan_name', 'No Clan'),
            'clan_rank': player_data.get('clan_rank', 'N/A'),
            'role': player_data.get('role', 'N/A'),
            'troops_trained': player_data.get('troops_trained', 0),
            'spells_trained': player_data.get('spells_trained', 0),
            'heroes_upgraded': player_data.get('heroes_upgraded', 0),
            'threat_level': player_data.get('threat_level', 'N/A')
        }
        
        updated_account = update_player_info(account_id, player_info)
        
        if player_data.get('clan_info'):
            update_clan_info(account_id, player_data['clan_info'])
            updated_account = get_account(account_id)
        
        return jsonify({
            'success': True,
            'message': 'Account refreshed successfully',
            'data': updated_account
        })
        
    except Exception as e:
        logger.error(f"Error refreshing account: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
