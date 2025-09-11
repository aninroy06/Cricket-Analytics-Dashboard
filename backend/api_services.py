import requests
import os
from datetime import datetime
from backend.models import Match, Player, PlayerStats, LiveScore, Team, db

class CricketAPIService:
    def __init__(self):
        self.api_key = os.getenv('CRICAPI_KEY')  # Get from cricapi.com
        self.base_url = "https://api.cricapi.com/v1"
    
    def get_live_matches(self):
        """Fetch live matches from API"""
        try:
            url = f"{self.base_url}/currentMatches"
            params = {"apikey": self.api_key, "offset": 0}
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error fetching live matches: {e}")
            return None
    
    def get_match_details(self, match_id):
        """Fetch detailed match information"""
        try:
            url = f"{self.base_url}/match_info"
            params = {"apikey": self.api_key, "id": match_id}
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error fetching match details: {e}")
            return None
    
    def get_player_stats(self, player_id):
        """Fetch player statistics"""
        try:
            url = f"{self.base_url}/players_info"
            params = {"apikey": self.api_key, "id": player_id}
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error fetching player stats: {e}")
            return None
    
    def update_database_with_live_data(self):
        """Update database with latest match data"""
        live_matches = self.get_live_matches()
        
        if live_matches and 'data' in live_matches:
            for match_data in live_matches['data']:
                # Update or create match record
                match = Match.query.filter_by(match_id=match_data.get('id')).first()
                
                if not match:
                    match = Match(
                        match_id=match_data.get('id'),
                        team1=match_data.get('teams', ['', ''])[0],
                        team2=match_data.get('teams', ['', ''])[1] if len(match_data.get('teams', [])) > 1 else '',
                        match_type=match_data.get('matchType', ''),
                        venue=match_data.get('venue', ''),
                        match_date=datetime.fromisoformat(match_data.get('dateTimeGMT', '').replace('Z', '+00:00')) if match_data.get('dateTimeGMT') else datetime.now(),
                        status=match_data.get('status', '')
                    )
                    db.session.add(match)
                
                # Update live score
                live_score = LiveScore.query.filter_by(match_id=match_data.get('id')).first()
                
                if not live_score:
                    live_score = LiveScore(match_id=match_data.get('id'))
                    db.session.add(live_score)
                
                live_score.team1_score = match_data.get('score', [{}])[0].get('r', '') if match_data.get('score') else ''
                live_score.team2_score = match_data.get('score', [{}])[1].get('r', '') if len(match_data.get('score', [])) > 1 else ''
                live_score.last_updated = datetime.utcnow()
            
            db.session.commit()
            return True
        
        return False