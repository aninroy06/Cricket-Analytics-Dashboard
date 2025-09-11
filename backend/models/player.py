from models.match import db
from datetime import datetime

class Player(db.Model):
    __tablename__ = 'players'
    
    player_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'))
    position = db.Column(db.String(50))
    batting_style = db.Column(db.String(20))
    bowling_style = db.Column(db.String(30))
    nationality = db.Column(db.String(50))
    birth_date = db.Column(db.Date)
    debut_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    team = db.relationship('Team', backref='players')
    
    def to_dict(self):
        return {
            'player_id': self.player_id,
            'name': self.name,
            'team': self.team.to_dict() if self.team else None,
            'position': self.position,
            'batting_style': self.batting_style,
            'bowling_style': self.bowling_style,
            'nationality': self.nationality,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'debut_date': self.debut_date.isoformat() if self.debut_date else None
        }

class PlayerStats(db.Model):
    __tablename__ = 'player_stats'
    
    stat_id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.player_id'))
    match_id = db.Column(db.Integer, db.ForeignKey('matches.match_id'))
    runs_scored = db.Column(db.Integer, default=0)
    balls_faced = db.Column(db.Integer, default=0)
    fours = db.Column(db.Integer, default=0)
    sixes = db.Column(db.Integer, default=0)
    strike_rate = db.Column(db.Numeric(5,2))
    wickets_taken = db.Column(db.Integer, default=0)
    overs_bowled = db.Column(db.Numeric(4,1), default=0)
    runs_conceded = db.Column(db.Integer, default=0)
    economy_rate = db.Column(db.Numeric(4,2))
    catches = db.Column(db.Integer, default=0)
    stumpings = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    player = db.relationship('Player', backref='stats')
    match = db.relationship('Match', backref='player_stats')