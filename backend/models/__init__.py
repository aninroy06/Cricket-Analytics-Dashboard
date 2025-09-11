from backend.database import db
from datetime import datetime

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.String(50), unique=True, nullable=False)
    team1 = db.Column(db.String(100), nullable=False)
    team2 = db.Column(db.String(100), nullable=False)
    match_type = db.Column(db.String(20), nullable=False)
    venue = db.Column(db.String(200))
    match_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50))
    winner = db.Column(db.String(100))
    toss_winner = db.Column(db.String(100))
    toss_decision = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    team = db.Column(db.String(100))
    role = db.Column(db.String(50))
    batting_style = db.Column(db.String(50))
    bowling_style = db.Column(db.String(50))
    country = db.Column(db.String(50))

class PlayerStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.String(50), db.ForeignKey('player.player_id'), nullable=False)
    match_id = db.Column(db.String(50), db.ForeignKey('match.match_id'), nullable=False)
    runs = db.Column(db.Integer, default=0)
    balls_faced = db.Column(db.Integer, default=0)
    fours = db.Column(db.Integer, default=0)
    sixes = db.Column(db.Integer, default=0)
    wickets = db.Column(db.Integer, default=0)
    overs_bowled = db.Column(db.Float, default=0.0)
    runs_conceded = db.Column(db.Integer, default=0)
    strike_rate = db.Column(db.Float, default=0.0)
    economy_rate = db.Column(db.Float, default=0.0)

class LiveScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.String(50), nullable=False)
    team1_score = db.Column(db.String(50))
    team2_score = db.Column(db.String(50))
    current_over = db.Column(db.Float)
    current_rr = db.Column(db.Float)
    required_rr = db.Column(db.Float)
    commentary = db.Column(db.Text)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    short_name = db.Column(db.String(10))
    country = db.Column(db.String(50))
    logo_url = db.Column(db.String(500))