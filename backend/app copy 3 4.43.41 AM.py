from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Database setup
DATABASE = 'cricket_analytics.db'

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Players table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            team TEXT NOT NULL,
            runs INTEGER DEFAULT 0,
            balls INTEGER DEFAULT 0,
            fours INTEGER DEFAULT 0,
            sixes INTEGER DEFAULT 0,
            strike_rate REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Matches table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team1 TEXT NOT NULL,
            team2 TEXT NOT NULL,
            score1 TEXT DEFAULT '0-0',
            score2 TEXT DEFAULT '0-0',
            status TEXT DEFAULT 'Upcoming',
            overs TEXT DEFAULT '0.0',
            venue TEXT,
            match_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert sample data if tables are empty
    cursor.execute('SELECT COUNT(*) FROM players')
    if cursor.fetchone()[0] == 0:
        sample_players = [
            ('V. KOHLI', 'IND', 45, 56, 4, 0, 80.36),
            ('S. IYER', 'IND', 23, 28, 3, 0, 82.14),
            ('D. WARNER', 'AUS', 67, 54, 8, 2, 124.07),
            ('S. SMITH', 'AUS', 34, 41, 4, 0, 82.93),
            ('R. SHARMA', 'IND', 89, 72, 11, 3, 123.61),
            ('M. LABUSCHAGNE', 'AUS', 56, 78, 6, 1, 71.79)
        ]
        
        cursor.executemany('''
            INSERT INTO players (name, team, runs, balls, fours, sixes, strike_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', sample_players)
    
    cursor.execute('SELECT COUNT(*) FROM matches')
    if cursor.fetchone()[0] == 0:
        sample_matches = [
            ('IND', 'AUS', '210-3', '207&250', 'Live', '45.2', 'Melbourne Cricket Ground', '2025-01-15'),
            ('ENG', 'NZ', '284-7', '156-4', 'Completed', '50.0', 'Lords', '2025-01-10'),
            ('SA', 'WI', '0-0', '0-0', 'Upcoming', '0.0', 'Cape Town', '2025-01-20')
        ]
        
        cursor.executemany('''
            INSERT INTO matches (team1, team2, score1, score2, status, overs, venue, match_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_matches)
    
    conn.commit()
    conn.close()

def calculate_strike_rate(runs, balls):
    """Calculate strike rate"""
    return round((runs / balls) * 100, 2) if balls > 0 else 0.0

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# ============ PLAYER CRUD ENDPOINTS ============

@app.route('/api/players', methods=['GET'])
def get_all_players():
    """Get all players"""
    try:
        conn = get_db_connection()
        players = conn.execute('SELECT * FROM players ORDER BY id DESC').fetchall()
        conn.close()
        
        players_list = []
        for player in players:
            players_list.append({
                'id': player['id'],
                'name': player['name'],
                'team': player['team'],
                'runs': player['runs'],
                'balls': player['balls'],
                'fours': player['fours'],
                'sixes': player['sixes'],
                'strike_rate': player['strike_rate'],
                'created_at': player['created_at'],
                'updated_at': player['updated_at']
            })
        
        return jsonify({
            'success': True,
            'data': players_list,
            'count': len(players_list)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/players/<int:player_id>', methods=['GET'])
def get_player_by_id(player_id):
    """Get player by ID"""
    try:
        conn = get_db_connection()
        player = conn.execute('SELECT * FROM players WHERE id = ?', (player_id,)).fetchone()
        conn.close()
        
        if not player:
            return jsonify({
                'success': False,
                'message': 'Player not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'id': player['id'],
                'name': player['name'],
                'team': player['team'],
                'runs': player['runs'],
                'balls': player['balls'],
                'fours': player['fours'],
                'sixes': player['sixes'],
                'strike_rate': player['strike_rate'],
                'created_at': player['created_at'],
                'updated_at': player['updated_at']
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/players', methods=['POST'])
def add_player():
    """Add new player"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('name') or not data.get('team'):
            return jsonify({
                'success': False,
                'message': 'Name and team are required'
            }), 400
        
        name = data['name'].upper()
        team = data['team'].upper()
        runs = int(data.get('runs', 0))
        balls = int(data.get('balls', 0))
        fours = int(data.get('fours', 0))
        sixes = int(data.get('sixes', 0))
        strike_rate = calculate_strike_rate(runs, balls)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO players (name, team, runs, balls, fours, sixes, strike_rate, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, team, runs, balls, fours, sixes, strike_rate, datetime.now()))
        
        player_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Player added successfully',
            'data': {
                'id': player_id,
                'name': name,
                'team': team,
                'runs': runs,
                'balls': balls,
                'fours': fours,
                'sixes': sixes,
                'strike_rate': strike_rate
            }
        }), 201
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/players/<int:player_id>', methods=['PUT'])
def update_player(player_id):
    """Update player"""
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        player = conn.execute('SELECT * FROM players WHERE id = ?', (player_id,)).fetchone()
        
        if not player:
            conn.close()
            return jsonify({
                'success': False,
                'message': 'Player not found'
            }), 404
        
        # Update fields
        name = data.get('name', player['name']).upper()
        team = data.get('team', player['team']).upper()
        runs = int(data.get('runs', player['runs']))
        balls = int(data.get('balls', player['balls']))
        fours = int(data.get('fours', player['fours']))
        sixes = int(data.get('sixes', player['sixes']))
        strike_rate = calculate_strike_rate(runs, balls)
        
        conn.execute('''
            UPDATE players 
            SET name = ?, team = ?, runs = ?, balls = ?, fours = ?, sixes = ?, 
                strike_rate = ?, updated_at = ?
            WHERE id = ?
        ''', (name, team, runs, balls, fours, sixes, strike_rate, datetime.now(), player_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Player updated successfully',
            'data': {
                'id': player_id,
                'name': name,
                'team': team,
                'runs': runs,
                'balls': balls,
                'fours': fours,
                'sixes': sixes,
                'strike_rate': strike_rate
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/players/<int:player_id>', methods=['DELETE'])
def delete_player(player_id):
    """Delete player"""
    try:
        conn = get_db_connection()
        player = conn.execute('SELECT * FROM players WHERE id = ?', (player_id,)).fetchone()
        
        if not player:
            conn.close()
            return jsonify({
                'success': False,
                'message': 'Player not found'
            }), 404
        
        conn.execute('DELETE FROM players WHERE id = ?', (player_id,))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': f'Player {player["name"]} deleted successfully'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

# ============ MATCH CRUD ENDPOINTS ============

@app.route('/api/matches', methods=['GET'])
def get_all_matches():
    """Get all matches"""
    try:
        conn = get_db_connection()
        matches = conn.execute('SELECT * FROM matches ORDER BY id DESC').fetchall()
        conn.close()
        
        matches_list = []
        for match in matches:
            matches_list.append({
                'id': match['id'],
                'team1': match['team1'],
                'team2': match['team2'],
                'score1': match['score1'],
                'score2': match['score2'],
                'status': match['status'],
                'overs': match['overs'],
                'venue': match['venue'],
                'match_date': match['match_date'],
                'created_at': match['created_at'],
                'updated_at': match['updated_at']
            })
        
        return jsonify({
            'success': True,
            'data': matches_list,
            'count': len(matches_list)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/matches/<int:match_id>', methods=['GET'])
def get_match_by_id(match_id):
    """Get match by ID"""
    try:
        conn = get_db_connection()
        match = conn.execute('SELECT * FROM matches WHERE id = ?', (match_id,)).fetchone()
        conn.close()
        
        if not match:
            return jsonify({
                'success': False,
                'message': 'Match not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'id': match['id'],
                'team1': match['team1'],
                'team2': match['team2'],
                'score1': match['score1'],
                'score2': match['score2'],
                'status': match['status'],
                'overs': match['overs'],
                'venue': match['venue'],
                'match_date': match['match_date'],
                'created_at': match['created_at'],
                'updated_at': match['updated_at']
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/matches', methods=['POST'])
def add_match():
    """Add new match"""
    try:
        data = request.get_json()
        
        if not data.get('team1') or not data.get('team2'):
            return jsonify({
                'success': False,
                'message': 'Both team names are required'
            }), 400
        
        team1 = data['team1'].upper()
        team2 = data['team2'].upper()
        score1 = data.get('score1', '0-0')
        score2 = data.get('score2', '0-0')
        status = data.get('status', 'Upcoming')
        overs = data.get('overs', '0.0')
        venue = data.get('venue', '')
        match_date = data.get('match_date', datetime.now().date())
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO matches (team1, team2, score1, score2, status, overs, venue, match_date, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (team1, team2, score1, score2, status, overs, venue, match_date, datetime.now()))
        
        match_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Match added successfully',
            'data': {
                'id': match_id,
                'team1': team1,
                'team2': team2,
                'score1': score1,
                'score2': score2,
                'status': status,
                'overs': overs,
                'venue': venue,
                'match_date': str(match_date)
            }
        }), 201
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/matches/<int:match_id>', methods=['PUT'])
def update_match(match_id):
    """Update match"""
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        match = conn.execute('SELECT * FROM matches WHERE id = ?', (match_id,)).fetchone()
        
        if not match:
            conn.close()
            return jsonify({
                'success': False,
                'message': 'Match not found'
            }), 404
        
        team1 = data.get('team1', match['team1']).upper()
        team2 = data.get('team2', match['team2']).upper()
        score1 = data.get('score1', match['score1'])
        score2 = data.get('score2', match['score2'])
        status = data.get('status', match['status'])
        overs = data.get('overs', match['overs'])
        venue = data.get('venue', match['venue'])
        match_date = data.get('match_date', match['match_date'])
        
        conn.execute('''
            UPDATE matches 
            SET team1 = ?, team2 = ?, score1 = ?, score2 = ?, status = ?, 
                overs = ?, venue = ?, match_date = ?, updated_at = ?
            WHERE id = ?
        ''', (team1, team2, score1, score2, status, overs, venue, match_date, datetime.now(), match_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Match updated successfully',
            'data': {
                'id': match_id,
                'team1': team1,
                'team2': team2,
                'score1': score1,
                'score2': score2,
                'status': status,
                'overs': overs,
                'venue': venue,
                'match_date': str(match_date)
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/matches/<int:match_id>', methods=['DELETE'])
def delete_match(match_id):
    """Delete match"""
    try:
        conn = get_db_connection()
        match = conn.execute('SELECT * FROM matches WHERE id = ?', (match_id,)).fetchone()
        
        if not match:
            conn.close()
            return jsonify({
                'success': False,
                'message': 'Match not found'
            }), 404
        
        conn.execute('DELETE FROM matches WHERE id = ?', (match_id,))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': f'Match {match["team1"]} vs {match["team2"]} deleted successfully'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

# ============ DASHBOARD ENDPOINTS ============

@app.route('/api/dashboard/live', methods=['GET'])
def get_live_scorecard():
    """Get live match data for scorecard"""
    try:
        conn = get_db_connection()
        
        # Get live match
        live_match = conn.execute(
            "SELECT * FROM matches WHERE status = 'Live' ORDER BY id DESC LIMIT 1"
        ).fetchone()
        
        if not live_match:
            # Get the most recent match if no live match
            live_match = conn.execute(
                "SELECT * FROM matches ORDER BY id DESC LIMIT 1"
            ).fetchone()
        
        # Get current batters for team1
        current_batters = []
        if live_match:
            batters = conn.execute(
                "SELECT * FROM players WHERE team = ? ORDER BY runs DESC LIMIT 2",
                (live_match['team1'],)
            ).fetchall()
            
            for batter in batters:
                current_batters.append({
                    'id': batter['id'],
                    'name': batter['name'],
                    'runs': batter['runs'],
                    'balls': batter['balls'],
                    'fours': batter['fours'],
                    'sixes': batter['sixes'],
                    'strike_rate': batter['strike_rate']
                })
        
        conn.close()
        
        live_data = {}
        if live_match:
            live_data = {
                'id': live_match['id'],
                'team1': live_match['team1'],
                'team2': live_match['team2'],
                'score1': live_match['score1'],
                'score2': live_match['score2'],
                'status': live_match['status'],
                'overs': live_match['overs'],
                'venue': live_match['venue'],
                'current_batters': current_batters
            }
        
        return jsonify({
            'success': True,
            'data': live_data
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/dashboard/analytics', methods=['GET'])
def get_player_analytics():
    """Get player analytics for dashboard"""
    try:
        conn = get_db_connection()
        
        # Top performers
        top_run_scorers = conn.execute(
            "SELECT * FROM players ORDER BY runs DESC LIMIT 5"
        ).fetchall()
        
        top_strike_rates = conn.execute(
            "SELECT * FROM players WHERE balls >= 10 ORDER BY strike_rate DESC LIMIT 5"
        ).fetchall()
        
        # Team statistics
        team_stats = conn.execute('''
            SELECT team, 
                   COUNT(*) as players_count,
                   SUM(runs) as total_runs,
                   AVG(strike_rate) as avg_strike_rate
            FROM players 
            GROUP BY team
        ''').fetchall()
        
        conn.close()
        
        analytics_data = {
            'top_run_scorers': [dict(player) for player in top_run_scorers],
            'top_strike_rates': [dict(player) for player in top_strike_rates],
            'team_statistics': [dict(stat) for stat in team_stats]
        }
        
        return jsonify({
            'success': True,
            'data': analytics_data
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

# ============ UTILITY ENDPOINTS ============

@app.route('/', methods=['GET'])
def home():
    """Home page with API documentation"""
    api_docs = '''
    <html>
    <head>
        <title>Cricket Analytics API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            .container { background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; backdrop-filter: blur(10px); }
            h1 { color: #fff; text-align: center; margin-bottom: 30px; }
            .endpoint { background: rgba(255,255,255,0.1); padding: 15px; margin: 10px 0; border-radius: 8px; }
            .method { color: #4CAF50; font-weight: bold; }
            .method.post { color: #2196F3; }
            .method.put { color: #FF9800; }
            .method.delete { color: #f44336; }
            code { background: rgba(0,0,0,0.3); padding: 2px 6px; border-radius: 4px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏏 Cricket Analytics API</h1>
            
            <h2>Player Endpoints</h2>
            <div class="endpoint">
                <span class="method">GET</span> <code>/api/players</code> - Get all players
            </div>
            <div class="endpoint">
                <span class="method">GET</span> <code>/api/players/{id}</code> - Get player by ID
            </div>
            <div class="endpoint">
                <span class="method post">POST</span> <code>/api/players</code> - Add new player
            </div>
            <div class="endpoint">
                <span class="method put">PUT</span> <code>/api/players/{id}</code> - Update player
            </div>
            <div class="endpoint">
                <span class="method delete">DELETE</span> <code>/api/players/{id}</code> - Delete player
            </div>
            
            <h2>Match Endpoints</h2>
            <div class="endpoint">
                <span class="method">GET</span> <code>/api/matches</code> - Get all matches
            </div>
            <div class="endpoint">
                <span class="method">GET</span> <code>/api/matches/{id}</code> - Get match by ID
            </div>
            <div class="endpoint">
                <span class="method post">POST</span> <code>/api/matches</code> - Add new match
            </div>
            <div class="endpoint">
                <span class="method put">PUT</span> <code>/api/matches/{id}</code> - Update match
            </div>
            <div class="endpoint">
                <span class="method delete">DELETE</span> <code>/api/matches/{id}</code> - Delete match
            </div>
            
            <h2>Dashboard Endpoints</h2>
            <div class="endpoint">
                <span class="method">GET</span> <code>/api/dashboard/live</code> - Get live scorecard data
            </div>
            <div class="endpoint">
                <span class="method">GET</span> <code>/api/dashboard/analytics</code> - Get player analytics
            </div>
            
            <h2>Usage</h2>
            <p>All endpoints return JSON responses with the following structure:</p>
            <pre><code>{
    "success": true/false,
    "data": {...},
    "message": "...",
    "count": number
}</code></pre>
        </div>
    </body>
    </html>
    '''
    return api_docs

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'message': 'Cricket Analytics API is running',
        'timestamp': datetime.now().isoformat()
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'message': 'Internal server error'
    }), 500

if __name__ == '__main__':
    # Initialize database
    init_db()
    print("🏏 Cricket Analytics API Starting...")
    print("📊 Database initialized with sample data")
    print("🚀 Server running at http://localhost:5000")
    print("📖 API Documentation available at http://localhost:5000")
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)
