from models.match import db
from sqlalchemy import text
from typing import List, Dict

class CricketAnalytics:
    
    def get_top_scorers(self, limit: int = 10) -> List[Dict]:
        """Get top scoring players across all matches"""
        query = text("""
            SELECT 
                p.name,
                p.nationality,
                t.name as team_name,
                SUM(ps.runs_scored) as total_runs,
                COUNT(ps.match_id) as matches_played,
                AVG(ps.runs_scored) as average_runs,
                MAX(ps.runs_scored) as highest_score,
                SUM(ps.fours) as total_fours,
                SUM(ps.sixes) as total_sixes
            FROM players p
            JOIN player_stats ps ON p.player_id = ps.player_id
            LEFT JOIN teams t ON p.team_id = t.team_id
            GROUP BY p.player_id, p.name, p.nationality, t.name
            ORDER BY total_runs DESC
            LIMIT :limit
        """)
        
        result = db.session.execute(query, {'limit': limit})
        return [dict(row._mapping) for row in result]
    
    def get_top_bowlers(self, limit: int = 10) -> List[Dict]:
        """Get top bowling performers"""
        query = text("""
            SELECT 
                p.name,
                p.nationality,
                t.name as team_name,
                SUM(ps.wickets_taken) as total_wickets,
                COUNT(ps.match_id) as matches_played,
                SUM(ps.overs_bowled) as total_overs,
                SUM(ps.runs_conceded) as total_runs_conceded,
                AVG(ps.economy_rate) as average_economy
            FROM players p
            JOIN player_stats ps ON p.player_id = ps.player_id
            LEFT JOIN teams t ON p.team_id = t.team_id
            WHERE ps.wickets_taken > 0
            GROUP BY p.player_id, p.name, p.nationality, t.name
            ORDER BY total_wickets DESC, average_economy ASC
            LIMIT :limit
        """)
        
        result = db.session.execute(query, {'limit': limit})
        return [dict(row._mapping) for row in result]
    
    def get_team_performance(self) -> List[Dict]:
        """Get team performance statistics"""
        query = text("""
            SELECT 
                t.name as team_name,
                t.country,
                COUNT(DISTINCT m.match_id) as total_matches,
                COUNT(DISTINCT CASE WHEN m.winner_team_id = t.team_id THEN m.match_id END) as wins,
                COUNT(DISTINCT CASE WHEN m.winner_team_id != t.team_id AND m.winner_team_id IS NOT NULL THEN m.match_id END) as losses,
                ROUND(
                    COUNT(DISTINCT CASE WHEN m.winner_team_id = t.team_id THEN m.match_id END) * 100.0 / 
                    NULLIF(COUNT(DISTINCT CASE WHEN m.status = 'completed' THEN m.match_id END), 0), 2
                ) as win_percentage
            FROM teams t
            LEFT JOIN matches m ON (t.team_id = m.team1_id OR t.team_id = m.team2_id)
            GROUP BY t.team_id, t.name, t.country
            ORDER BY win_percentage DESC, total_matches DESC
        """)
        
        result = db.session.execute(query)
        return [dict(row._mapping) for row in result]
    
    def get_match_statistics(self, match_type: str = None) -> Dict:
        """Get overall match statistics"""
        where_clause = "WHERE m.match_type = :match_type" if match_type else ""
        
        query = text(f"""
            SELECT 
                COUNT(*) as total_matches,
                COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_matches,
                COUNT(CASE WHEN status = 'live' THEN 1 END) as live_matches,
                COUNT(CASE WHEN status = 'upcoming' THEN 1 END) as upcoming_matches,
                AVG(ms.total_runs) as average_runs_per_innings,
                MAX(ms.total_runs) as highest_team_score
            FROM matches m
            LEFT JOIN match_scores ms ON m.match_id = ms.match_id
            {where_clause}
        """)
        
        params = {'match_type': match_type} if match_type else {}
        result = db.session.execute(query, params).first()
        return dict(result._mapping) if result else {}
    
    def get_venue_statistics(self) -> List[Dict]:
        """Get statistics by venue"""
        query = text("""
            SELECT 
                venue,
                COUNT(*) as matches_played,
                AVG(ms.total_runs) as average_runs,
                COUNT(CASE WHEN m.status = 'completed' THEN 1 END) as completed_matches
            FROM matches m
            LEFT JOIN match_scores ms ON m.match_id = ms.match_id
            WHERE venue IS NOT NULL
            GROUP BY venue
            ORDER BY matches_played DESC
        """)
        
        result = db.session.execute(query)
        return [dict(row._mapping) for row in result]