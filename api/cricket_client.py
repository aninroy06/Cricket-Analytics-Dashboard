import requests
import json
from typing import Dict, List, Optional
from config import Config

class CricketAPIClient:
    def __init__(self):
        self.base_url = Config.CRICKET_API_BASE_URL
        self.api_key = Config.CRICKET_API_KEY
        
    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Make API request with error handling"""
        try:
            url = f"{self.base_url}/{endpoint}"
            headers = {
                'Accept': 'application/json',
            }
            
            # Add API key if required by the service
            if self.api_key and self.api_key != 'your-api-key':
                params = params or {}
                params['apikey'] = self.api_key
                
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None
    
    def get_live_matches(self) -> List[Dict]:
        """Fetch current live matches"""
        data = self._make_request('matches')
        if data and 'data' in data:
            return [match for match in data['data'] if match.get('status') == 'live']
        return []
    
    def get_match_details(self, match_id: str) -> Optional[Dict]:
        """Get detailed information about a specific match"""
        return self._make_request(f'matches/{match_id}')
    
    def get_match_scorecard(self, match_id: str) -> Optional[Dict]:
        """Get scorecard for a match"""
        return self._make_request(f'matches/{match_id}/scorecard')
    
    def get_player_info(self, player_id: str) -> Optional[Dict]:
        """Get player information"""
        return self._make_request(f'players/{player_id}')
    
    def get_upcoming_matches(self) -> List[Dict]:
        """Get upcoming matches"""
        data = self._make_request('matches')
        if data and 'data' in data:
            return [match for match in data['data'] if match.get('status') == 'upcoming']
        return []
    
    def get_recent_matches(self) -> List[Dict]:
        """Get recently completed matches"""
        data = self._make_request('matches')
        if data and 'data' in data:
            return [match for match in data['data'] if match.get('status') == 'completed']
        return []
