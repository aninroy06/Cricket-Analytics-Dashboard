from flask import Blueprint, jsonify, request
from models.match import db, Match, Team
from models.player import Player, PlayerStats
from api.cricket_client import CricketAPIClient
from database.queries import CricketAnalytics
import json

api_bp = Blueprint('api', __name__, url_prefix='/api')
cricket_client = CricketAPIClient()
analytics = CricketAnalytics()

@api_bp.route('/live-matches', methods=['GET'])
def get_live_matches():
    """Get live matches from external API and database"""
    try:
        # Get from external API
        live_matches = cricket_client.get_live_matches()
        
        # Also get from database
        db_matches = Match.query.filter_by(status='live').all()
        db_matches_data = [match.to_dict() for match in db_matches]
        
        return jsonify({
            'success': True,
            'live_matches': live_matches,
            'db_matches': db_matches_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/matches', methods=['GET'])
def get_all_matches():
    """Get all matches from database"""
    try:
        matches = Match.query.order_by(Match.match_date.desc()).all()
        return jsonify({
            'success': True,
            'matches': [match.to_dict() for match in matches]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/matches', methods=['POST'])
def create_match():
    """Create a new match"""
    try:
        data = request.get_json()
        
        match = Match(
            external_match_id=data.get('external_match_id'),
            team1_id=data.get('team1_id'),
            team2_id=data.get('team2_id'),
            match_date=data.get('match_date'),
            venue=data.get('venue'),
            match_type=data.get('match_type'),
            status=data.get('status', 'upcoming')
        )
        
        db.session.add(match)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'match': match.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/players', methods=['GET'])
def get_all_players():
    """Get all players"""
    try:
        players = Player.query.all()
        return jsonify({
            'success': True,
            'players': [player.to_dict() for player in players]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/players', methods=['POST'])
def create_player():
    """Create a new player"""
    try:
        data = request.get_json()
        
        player = Player(
            name=data.get('name'),
            team_id=data.get('team_id'),
            position=data.get('position'),
            batting_style=data.get('batting_style'),
            bowling_style=data.get('bowling_style'),
            nationality=data.get('nationality'),
            birth_date=data.get('birth_date'),
            debut_date=data.get('debut_date')
        )
        
        db.session.add(player)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'player': player.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/teams', methods=['GET'])
def get_all_teams():
    """Get all teams"""
    try:
        teams = Team.query.all()
        return jsonify({
            'success': True,
            'teams': [team.to_dict() for team in teams]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/teams', methods=['POST'])
def create_team():
    """Create a new team"""
    try:
        data = request.get_json()
        
        team = Team(
            name=data.get('name'),
            country=data.get('country'),
            founded_year=data.get('founded_year'),
            captain=data.get('captain'),
            coach=data.get('coach')
        )
        
        db.session.add(team)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'team': team.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/analytics/top-scorers', methods=['GET'])
def get_top_scorers():
    """Get top scoring players"""
    try:
        limit = request.args.get('limit', 10, type=int)
        top_scorers = analytics.get_top_scorers(limit)
        
        return jsonify({
            'success': True,
            'top_scorers': top_scorers
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/analytics/team-performance', methods=['GET'])
def get_team_performance():
    """Get team performance statistics"""
    try:
        team_performance = analytics.get_team_performance()
        
        return jsonify({
            'success': True,
            'team_performance': team_performance
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500