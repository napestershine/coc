from flask import Flask, jsonify, request
from models import create_account, get_account, get_all_accounts, update_account, delete_account, update_account_stats
from coc_service import COCService
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
        'message': 'Welcome to CoC Account Manager API',
        'version': '1.0.0',
        'endpoints': {
            'accounts': '/api/accounts',
            'health': '/api/health'
        }
    })


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'coc-api',
        'version': '1.0.0'
    })


# ============================================================================
# CoC ACCOUNT MANAGEMENT ENDPOINTS
# ============================================================================

@app.route('/api/accounts', methods=['GET'])
def list_accounts():
    """Get all managed CoC accounts"""
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
    """Add a new CoC account to track"""
    try:
        data = request.get_json()
        
        if not data or 'username' not in data:
            return jsonify({'success': False, 'error': 'Username is required'}), 400
        
        username = data.get('username', '').strip()
        
        if not username:
            return jsonify({'success': False, 'error': 'Username cannot be empty'}), 400
        
        # Fetch player data from CoC
        player_data = COCService.get_player_data(username)
        
        if not player_data:
            return jsonify({'success': False, 'error': 'Could not fetch player data'}), 404
        
        # Create account entry
        account = create_account(username)
        
        # Update with fetched stats
        stats = {
            'level': player_data.get('level'),
            'rank': player_data.get('rank'),
            'global_rank': player_data.get('global_rank'),
            'clashes_count': player_data.get('clashes_count'),
            'wins': player_data.get('wins'),
            'win_rate': player_data.get('win_rate', 'N/A'),
            'country': player_data.get('country', ''),
            'bio': player_data.get('bio', '')
        }
        
        updated_account = update_account_stats(account['id'], stats)
        
        return jsonify({
            'success': True,
            'message': f'Account {username} added successfully',
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
        
        # Fetch fresh data from CoC
        player_data = COCService.get_player_data(account['username'])
        
        if player_data:
            stats = {
                'level': player_data.get('level'),
                'rank': player_data.get('rank'),
                'global_rank': player_data.get('global_rank'),
                'clashes_count': player_data.get('clashes_count'),
                'wins': player_data.get('wins'),
                'is_online': player_data.get('is_online', False),
                'win_rate': player_data.get('win_rate', 'N/A')
            }
            account = update_account_stats(account_id, stats)
        
        return jsonify({
            'success': True,
            'data': account
        })
        
    except Exception as e:
        logger.error(f"Error getting account details: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/accounts/<int:account_id>/stats', methods=['GET'])
def get_account_stats(account_id):
    """Get statistics for a specific account"""
    try:
        account = get_account(account_id)
        
        if not account:
            return jsonify({'success': False, 'error': 'Account not found'}), 404
        
        username = account['username']
        
        # Fetch fresh stats
        player_data = COCService.get_player_data(username)
        clash_history = COCService.get_clash_history(username)
        current_clash = COCService.get_current_clash(username)
        
        return jsonify({
            'success': True,
            'data': {
                'account_id': account_id,
                'username': username,
                'stats': account.get('stats', {}),
                'current_clash': current_clash,
                'recent_clashes': clash_history
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
        
        username = account['username']
        delete_account(account_id)
        
        return jsonify({
            'success': True,
            'message': f'Account {username} removed successfully'
        })
        
    except Exception as e:
        logger.error(f"Error deleting account: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/accounts/<int:account_id>/refresh', methods=['POST'])
def refresh_account(account_id):
    """Refresh account data from CoC"""
    try:
        account = get_account(account_id)
        
        if not account:
            return jsonify({'success': False, 'error': 'Account not found'}), 404
        
        username = account['username']
        player_data = COCService.get_player_data(username)
        
        if not player_data:
            return jsonify({'success': False, 'error': 'Could not fetch player data'}), 404
        
        stats = {
            'level': player_data.get('level'),
            'rank': player_data.get('rank'),
            'global_rank': player_data.get('global_rank'),
            'clashes_count': player_data.get('clashes_count'),
            'wins': player_data.get('wins'),
            'is_online': player_data.get('is_online', False),
            'win_rate': player_data.get('win_rate', 'N/A')
        }
        
        updated_account = update_account_stats(account_id, stats)
        
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
