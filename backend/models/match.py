from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Team(db.Model):
    __tablename__ = 'teams'
    
    team_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    country = db.Column(db.String(50))
    founded_year = db.Column(db.Integer)
    captain = db.Column(db.String(100))
    coach = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'team_id': self.team_id,
            'name': self.name,
            'country': self.country,
            'founded_year': self.founded_year,
            'captain': self.captain,
            'coach': self.coach
        }

class Match(db.Model):
    __tablename__ = 'matches'
    
    match_id = db.Column(db.Integer, primary_key=True)
    external_match_id = db.Column(db.String(50), unique=True)
    team1_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'))
    team2_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'))
    match_date = db.Column(db.DateTime)
    venue = db.Column(db.String(200))
    match_type = db.Column(db.String(20))
    status = db.Column(db.String(20), default='upcoming')
    winner_team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'))
    toss_winner_team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'))
    toss_decision = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    team1 = db.relationship('Team', foreign_keys=[team1_id])
    team2 = db.relationship('Team', foreign_keys=[team2_id])
    winner = db.relationship('Team', foreign_keys=[winner_team_id])
    
    def to_dict(self):
        return {
            'match_id': self.match_id,
            'external_match_id': self.external_match_id,
            'team1': self.team1.to_dict() if self.team1 else None,
            'team2': self.team2.to_dict() if self.team2 else None,
            'match_date': self.match_date.isoformat() if self.match_date else None,
            'venue': self.venue,
            'match_type': self.match_type,
            'status': self.status,
            'winner': self.winner.to_dict() if self.winner else None,
            'toss_winner_team_id': self.toss_winner_team_id,
            'toss_decision': self.toss_decision
        }