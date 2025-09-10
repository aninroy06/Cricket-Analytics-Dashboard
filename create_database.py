#!/usr/bin/env python3
"""
Database Creation Script for Cricket Analytics Dashboard
Run this script to create the SQLite database and populate with sample data
"""

import sys
import os
from pathlib import Path
from datetime import datetime, date

# Add backend directory to Python path
backend_dir = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_dir))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import Flask and database models
from flask import Flask
from models.database import db, Team, Player, Match, Innings, PlayerStats, LiveScore

def create_app():
    """Create Flask app for database operations"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///cricket_analytics.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    return app

def create_database():
    """Create database tables"""
    app = create_app()
    
    with app.app_context():
        print("🏏 Creating Cricket Analytics Database...")
        
        # Drop all tables (if they exist) and create new ones
        db.drop_all()
        db.create_all()
        
        print("✅ Database tables created successfully!")
        
        # Verify tables were created
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"📊 Created tables: {', '.join(tables)}")
        
        return app

def populate_sample_data():
    """Populate database with sample cricket data"""
    app = create_app()
    
    with app.app_context():
        print("\n🎯 Adding sample data...")
        
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
            
            teams = {}
            for team_data in teams_data:
                team = Team(**team_data)
                db.session.add(team)
                db.session.flush()  # Get the ID
                teams[team_data['short_name']] = team
                print(f"  ✓ Added team: {team.name}")
            
            # Create sample players
            players_data = [
                {'name': 'Virat Kohli', 'team': 'IND', 'role': 'batsman', 'batting_style': 'Right-hand bat', 'country': 'India'},
                {'name': 'Rohit Sharma', 'team': 'IND', 'role': 'batsman', 'batting_style': 'Right-hand bat', 'country': 'India'},
                {'name': 'Jasprit Bumrah', 'team': 'IND', 'role': 'bowler', 'bowling_style': 'Right-arm fast', 'country': 'India'},
                {'name': 'Steve Smith', 'team': 'AUS', 'role': 'batsman', 'batting_style': 'Right-hand bat', 'country': 'Australia'},
                {'name': 'David Warner', 'team': 'AUS', 'role': 'batsman', 'batting_style': 'Left-hand bat', 'country': 'Australia'},
                {'name': 'Pat Cummins', 'team': 'AUS', 'role': 'bowler', 'bowling_style': 'Right-arm fast', 'country': 'Australia'},
                {'name': 'Joe Root', 'team': 'ENG', 'role': 'batsman', 'batting_style': 'Right-hand bat', 'country': 'England'},
                {'name': 'Ben Stokes', 'team': 'ENG', 'role': 'all-rounder', 'batting_style': 'Left-hand bat', 'country': 'England'},
                {'name': 'Babar Azam', 'team': 'PAK', 'role': 'batsman', 'batting_style': 'Right-hand bat', 'country': 'Pakistan'},
                {'name': 'Shaheen Afridi', 'team': 'PAK', 'role': 'bowler', 'bowling_style': 'Left-arm fast', 'country': 'Pakistan'}
            ]
            
            players = {}
            for player_data in players_data:
                team_key = player_data.pop('team')
                player = Player(team_id=teams[team_key].id, **player_data)
                db.session.add(player)
                db.session.flush()
                players[player.name] = player
                print(f"  ✓ Added player: {player.name} ({teams[team_key].name})")
            
            # Create sample matches
            matches_data = [
                {
                    'match_id': 'IND_vs_AUS_2024_001',
                    'team1': 'IND', 'team2': 'AUS',
                    'venue': 'Melbourne Cricket Ground',
                    'match_date': datetime(2024, 1, 15, 14, 0),
                    'match_type': 'ODI',
                    'status': 'completed',
                    'winner': 'IND'
                },
                {
                    'match_id': 'ENG_vs_PAK_2024_001',
                    'team1': 'ENG', 'team2': 'PAK',
                    'venue': 'Lords Cricket Ground',
                    'match_date': datetime(2024, 1, 20, 11, 0),
                    'match_type': 'T20',
                    'status': 'completed',
                    'winner': 'ENG'
                },
                {
                    'match_id': 'IND_vs_ENG_2024_001',
                    'team1': 'IND', 'team2': 'ENG',
                    'venue': 'Wankhede Stadium',
                    'match_date': datetime(2024, 2, 1, 14, 30),
                    'match_type': 'ODI',
                    'status': 'live',
                    'winner': None
                }
            ]
            
            for match_data in matches_data:
                team1_key = match_data.pop('team1')
                team2_key = match_data.pop('team2')
                winner_key = match_data.pop('winner')
                
                match = Match(
                    team1_id=teams[team1_key].id,
                    team2_id=teams[team2_key].id,
                    winner_team_id=teams[winner_key].id if winner_key else None,
                    **match_data
                )
                db.session.add(match)
                db.session.flush()
                print(f"  ✓ Added match: {teams[team1_key].name} vs {teams[team2_key].name}")
            
            # Create sample player stats
            stats_data = [
                {
                    'player': 'Virat Kohli',
                    'match_id': 1,  # IND vs AUS
                    'runs_scored': 85,
                    'balls_faced': 92,
                    'fours': 8,
                    'sixes': 2,
                    'wickets_taken': 0,
                    'overs_bowled': 0,
                    'runs_conceded': 0
                },
                {
                    'player': 'Steve Smith',
                    'match_id': 1,  # IND vs AUS
                    'runs_scored': 72,
                    'balls_faced': 89,
                    'fours': 6,
                    'sixes': 1,
                    'wickets_taken': 0,
                    'overs_bowled': 0,
                    'runs_conceded': 0
                }
            ]
            
            for stat_data in stats_data:
                player_name = stat_data.pop('player')
                stat = PlayerStats(
                    player_id=players[player_name].id,
                    **stat_data
                )
                db.session.add(stat)
                print(f"  ✓ Added stats for: {player_name}")
            
            # Commit all changes
            db.session.commit()
            print("\n✅ Sample data added successfully!")
            
            # Print summary
            print(f"\n📊 Database Summary:")
            print(f"  Teams: {Team.query.count()}")
            print(f"  Players: {Player.query.count()}")
            print(f"  Matches: {Match.query.count()}")
            print(f"  Player Stats: {PlayerStats.query.count()}")
            
        except Exception as e:
            print(f"❌ Error adding sample data: {e}")
            db.session.rollback()

def verify_database():
    """Verify database was created correctly"""
    app = create_app()
    
    with app.app_context():
        print("\n🔍 Verifying database...")
        
        # Check if tables exist and have data
        tables_info = {
            'Teams': Team.query.count(),
            'Players': Player.query.count(),
            'Matches': Match.query.count(),
            'Player Stats': PlayerStats.query.count(),
            'Innings': Innings.query.count(),
            'Live Scores': LiveScore.query.count()
        }
        
        for table_name, count in tables_info.items():
            status = "✅" if count >= 0 else "❌"
            print(f"  {status} {table_name}: {count} records")
        
        # Test some queries
        print("\n🧪 Testing sample queries...")
        
        # Get top teams
        teams = Team.query.limit(3).all()
        print(f"  Sample teams: {', '.join([t.name for t in teams])}")
        
        # Get top players
        players = Player.query.limit(3).all()
        print(f"  Sample players: {', '.join([p.name for p in players])}")
        
        print("\n🎉 Database verification completed!")

if __name__ == '__main__':
    print("🏏 Cricket Analytics Database Setup")
    print("=" * 50)
    
    try:
        # Create database
        create_database()
        
        # Add sample data
        populate_sample_data()
        
        # Verify everything worked
        verify_database()
        
        print(f"\n🎯 Database created successfully!")
        print(f"📁 Database file: cricket_analytics.db")
        print(f"🚀 You can now run: python backend/app.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
