from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Team(db.Model):
    __tablename__ = 'teams'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    short_name = db.Column(db.String(10))
    country = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Team {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'short_name': self.short_name,
            'country': self.country
        }

class Player(db.Model):
    __tablename__ = 'players'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    role = db.Column(db.String(20))
    country = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    team = db.relationship('Team', backref='players')

    def __repr__(self):
        return f'<Player {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'team': self.team.name if self.team else None,
            'role': self.role,
            'country': self.country
        }

class Match(db.Model):
    __tablename__ = 'matches'
    
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.String(50), unique=True)
    team1_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team2_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    venue = db.Column(db.String(100))
    status = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    team1 = db.relationship('Team', foreign_keys=[team1_id])
    team2 = db.relationship('Team', foreign_keys=[team2_id])

    def __repr__(self):
        return f'<Match {self.match_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'match_id': self.match_id,
            'team1': self.team1.name if self.team1 else None,
            'team2': self.team2.name if self.team2 else None,
            'venue': self.venue,
            'status': self.status
        }

class PlayerStats(db.Model):
    __tablename__ = 'player_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'))
    runs_scored = db.Column(db.Integer, default=0)
    wickets_taken = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    player = db.relationship('Player')
    match = db.relationship('Match')

    def to_dict(self):
        return {
            'id': self.id,
            'player': self.player.name if self.player else None,
            'runs_scored': self.runs_scored,
            'wickets_taken': self.wickets_taken
        }

# Simplified for now - we can add more models later
class Innings(db.Model):
    __tablename__ = 'innings'
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'))

class LiveScore(db.Model):
    __tablename__ = 'live_scores'
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'))
