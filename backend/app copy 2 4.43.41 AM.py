from flask import Flask, jsonify, request, send_from_directory, render_template_string
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import socket
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cricket_analytics.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-secret-key'

# Initialize database
db = SQLAlchemy(app)

# Cricket API Configuration
CRICAPI_KEY = "b474660e-4eed-4355-a381-6d24bc1a0ca5"
CRICAPI_BASE_URL = "https://api.cricapi.com/v1"

@app.route('/api/execute-sql', methods=['POST'])
def execute_sql():
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'status': 'error', 'message': 'No query provided'})
        
        if not query.upper().startswith('SELECT'):
            return jsonify({'status': 'error', 'message': 'Only SELECT queries allowed'})
        
        result = db.session.execute(query).fetchall()
        
        if result:
            columns = list(result[0].keys()) if result else []
            rows = [dict(row) for row in result]
        else:
            columns = []
            rows = []
        
        return jsonify({
            'status': 'success',
            'columns': columns,
            'rows': rows,
            'count': len(rows)
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

# Database Models
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    short_name = db.Column(db.String(10))
    country = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'short_name': self.short_name,
            'country': self.country,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    role = db.Column(db.String(20))
    country = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    team = db.relationship('Team', backref='players')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'team': self.team.name if self.team else None,
            'role': self.role,
            'country': self.country,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.String(50), unique=True)
    team1_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    team2_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    venue = db.Column(db.String(100))
    match_date = db.Column(db.DateTime)
    match_type = db.Column(db.String(20))
    status = db.Column(db.String(50))
    series = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    team1 = db.relationship('Team', foreign_keys=[team1_id])
    team2 = db.relationship('Team', foreign_keys=[team2_id])
    
    def to_dict(self):
        return {
            'id': self.id,
            'match_id': self.match_id,
            'team1': self.team1.name if self.team1 else None,
            'team2': self.team2.name if self.team2 else None,
            'venue': self.venue,
            'match_date': self.match_date.isoformat() if self.match_date else None,
            'match_type': self.match_type,
            'status': self.status,
            'series': self.series,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Cricket API Service
class CricketAPI:
    def __init__(self):
        self.base_url = CRICAPI_BASE_URL
        self.api_key = CRICAPI_KEY
    
    def get_current_matches(self):
        """Get current/live matches"""
        url = f"{self.base_url}/currentMatches"
        params = {"apikey": self.api_key, "offset": 0}
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 'success':
                return data.get('data', [])
            else:
                print(f"API Error: {data.get('reason', 'Unknown error')}")
                return []
        except requests.RequestException as e:
            print(f"Request Error: {e}")
            return []
    
    def get_recent_matches(self):
        """Get recent completed matches"""
        url = f"{self.base_url}/matches"
        params = {"apikey": self.api_key, "offset": 0}
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 'success':
                return data.get('data', [])
            return []
        except requests.RequestException as e:
            print(f"Request Error: {e}")
            return []

# Initialize Cricket API
cricket_api = CricketAPI()

def find_free_port(start_port=8080):
    """Find a free port starting from start_port"""
    for port in range(start_port, start_port + 20):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

# Frontend Route
@app.route('/')
def serve_dashboard():
    try:
        with open('../frontend/dashboard.html', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return '''
        <h1>🏏 Cricket Analytics Backend</h1>
        <p>Frontend dashboard.html not found.</p>
        <p>API is running at <a href="/api">/api</a></p>
        '''

# API Routes
@app.route('/api')
def api_home():
    return jsonify({
        'message': '🏏 Cricket Analytics Dashboard API',
        'version': '2.0.0',
        'status': 'running',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'database': 'connected',
        'cricket_api': 'configured'
    })

@app.route('/api/database/status')
def database_status():
    try:
        # Test database connection
        result = db.session.execute('SELECT 1').fetchone()
        
        # Count records
        teams_count = Team.query.count()
        players_count = Player.query.count()
        matches_count = Match.query.count()
        
        return jsonify({
            'status': 'connected',
            'database_type': 'SQLite',
            'database_file': 'cricket_analytics.db',
            'tables': {
                'teams': teams_count,
                'players': players_count,
                'matches': matches_count
            },
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/api/teams')
def get_teams():
    try:
        teams = Team.query.all()
        return jsonify({
            'teams': [team.to_dict() for team in teams],
            'count': len(teams)
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'teams': [],
            'count': 0
        })

@app.route('/api/players')
def get_players():
    try:
        players = Player.query.all()
        return jsonify({
            'players': [player.to_dict() for player in players],
            'count': len(players)
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'players': [],
            'count': 0
        })

@app.route('/api/matches')
def get_matches():
    try:
        matches = Match.query.order_by(Match.created_at.desc()).limit(20).all()
        return jsonify({
            'matches': [match.to_dict() for match in matches],
            'count': len(matches)
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'matches': [],
            'count': 0
        })

@app.route('/api/live-matches')
def get_live_matches():
    try:
        matches = cricket_api.get_current_matches()
        return jsonify({
            'status': 'success',
            'live_matches': matches,
            'count': len(matches),
            'last_updated': datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'live_matches': [],
            'count': 0
        })

@app.route('/api/recent-matches')
def get_recent_matches():
    try:
        matches = cricket_api.get_recent_matches()
        return jsonify({
            'status': 'success',
            'recent_matches': matches,
            'count': len(matches),
            'last_updated': datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'recent_matches': [],
            'count': 0
        })

@app.route('/api/create-sample-data')
def create_sample_data():
    try:
        # Create sample teams
        teams_data = [
            {'name': 'India', 'short_name': 'IND', 'country': 'India'},
            {'name': 'Australia', 'short_name': 'AUS', 'country': 'Australia'},
            {'name': 'England', 'short_name': 'ENG', 'country': 'England'},
            {'name': 'Pakistan', 'short_name': 'PAK', 'country': 'Pakistan'},
            {'name': 'South Africa', 'short_name': 'SA', 'country': 'South Africa'},
            {'name': 'New Zealand', 'short_name': 'NZ', 'country': 'New Zealand'}
        ]
        
        teams_created = 0
        for team_data in teams_data:
            existing_team = Team.query.filter_by(name=team_data['name']).first()
            if not existing_team:
                team = Team(**team_data)
                db.session.add(team)
                teams_created += 1
        
        # Create sample players
        players_created = 0
        if teams_created > 0:
            db.session.flush()
            
            india = Team.query.filter_by(name='India').first()
            australia = Team.query.filter_by(name='Australia').first()
            england = Team.query.filter_by(name='England').first()
            
            if india and australia and england:
                players_data = [
                    {'name': 'Virat Kohli', 'team_id': india.id, 'role': 'batsman', 'country': 'India'},
                    {'name': 'Rohit Sharma', 'team_id': india.id, 'role': 'batsman', 'country': 'India'},
                    {'name': 'Jasprit Bumrah', 'team_id': india.id, 'role': 'bowler', 'country': 'India'},
                    {'name': 'Steve Smith', 'team_id': australia.id, 'role': 'batsman', 'country': 'Australia'},
                    {'name': 'David Warner', 'team_id': australia.id, 'role': 'batsman', 'country': 'Australia'},
                    {'name': 'Pat Cummins', 'team_id': australia.id, 'role': 'bowler', 'country': 'Australia'},
                    {'name': 'Joe Root', 'team_id': england.id, 'role': 'batsman', 'country': 'England'},
                    {'name': 'Ben Stokes', 'team_id': england.id, 'role': 'all-rounder', 'country': 'England'}
                ]
                
                for player_data in players_data:
                    existing_player = Player.query.filter_by(name=player_data['name']).first()
                    if not existing_player:
                        player = Player(**player_data)
                        db.session.add(player)
                        players_created += 1
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Sample data created successfully',
            'teams_created': teams_created,
            'players_created': players_created
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/test-cricket-api')
def test_cricket_api():
    try:
        url = f"{CRICAPI_BASE_URL}/currentMatches"
        params = {"apikey": CRICAPI_KEY, "offset": 0}
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        return jsonify({
            'status': 'success' if data.get('status') == 'success' else 'error',
            'api_response': data.get('status'),
            'message': data.get('reason', 'API test successful'),
            'data_count': len(data.get('data', [])),
            'api_key_status': 'valid' if data.get('status') == 'success' else 'invalid'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'api_key_status': 'error'
        })

# SQL Query endpoint
@app.route('/api/execute-sql', methods=['POST'])
def execute_sql():
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({
                'status': 'error',
                'message': 'No query provided'
            }), 400
        
        # Security: Only allow SELECT statements
        if not query.upper().startswith('SELECT'):
            return jsonify({
                'status': 'error',
                'message': 'Only SELECT queries are allowed for security reasons'
            }), 400
        
        # Execute the query
        result = db.session.execute(query).fetchall()
        
        # Convert result to list of dictionaries
        if result:
            columns = list(result[0].keys()) if hasattr(result[0], 'keys') else []
            rows = []
            for row in result:
                if hasattr(row, '_asdict'):
                    rows.append(row._asdict())
                elif hasattr(row, 'keys'):
                    rows.append(dict(row))
                else:
                    rows.append(dict(zip(columns, row)))
        else:
            columns = []
            rows = []
        
        return jsonify({
            'status': 'success',
            'columns': columns,
            'rows': rows,
            'count': len(rows),
            'query': query
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'query': query if 'query' in locals() else ''
        }), 500

@app.route('/api/sample-queries')
def get_sample_queries():
    sample_queries = [
        {
            'name': 'All Teams',
            'description': 'List all teams in the database',
            'query': 'SELECT * FROM team ORDER BY name;'
        },
        {
            'name': 'All Players with Teams',
            'description': 'List all players with their team names',
            'query': '''SELECT p.name as player_name, t.name as team_name, p.role, p.country 
                       FROM player p 
                       LEFT JOIN team t ON p.team_id = t.id 
                       ORDER BY p.name;'''
        },
        {
            'name': 'Team Player Count',
            'description': 'Count players per team',
            'query': '''SELECT t.name as team_name, COUNT(p.id) as player_count 
                       FROM team t 
                       LEFT JOIN player p ON t.id = p.team_id 
                       GROUP BY t.id, t.name 
                       ORDER BY player_count DESC;'''
        },
        {
            'name': 'Players by Role',
            'description': 'Count players by their roles',
            'query': '''SELECT role, COUNT(*) as count 
                       FROM player 
                       WHERE role IS NOT NULL 
                       GROUP BY role 
                       ORDER BY count DESC;'''
        },
        {
            'name': 'Recent Matches',
            'description': 'List recent matches with team names',
            'query': '''SELECT m.match_id, t1.name as team1, t2.name as team2, 
                              m.venue, m.status, m.match_type 
                       FROM match m 
                       LEFT JOIN team t1 ON m.team1_id = t1.id 
                       LEFT JOIN team t2 ON m.team2_id = t2.id 
                       ORDER BY m.created_at DESC 
                       LIMIT 10;'''
        },
        {
            'name': 'Database Schema',
            'description': 'Show all tables in the database',
            'query': "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
        }
    ]
    
    return jsonify({
        'status': 'success',
        'sample_queries': sample_queries
    })

if __name__ == '__main__':
    # Find a free port
    port = find_free_port(8080)
    
    if port is None:
        print("❌ Could not find a free port")
        exit(1)
    
    print("🏏 Cricket Analytics Backend Server")
    print("=" * 50)
    print(f"🚀 Server: http://localhost:{port}")
    print(f"🌐 Dashboard: http://localhost:{port}")
    print(f"📊 API: http://localhost:{port}/api")
    print(f"❤️  Health: http://localhost:{port}/api/health")
    print("=" * 50)
    print("📝 Press Ctrl+C to stop")
    
    # Create database tables
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables created successfully!")
        except Exception as e:
            print(f"❌ Database error: {e}")
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=port,
        threaded=True
    )
