import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://username:password@localhost/cricket_analytics'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CRICKET_API_KEY = os.environ.get('CRICKET_API_KEY') or 'your-api-key'
    CRICKET_API_BASE_URL = 'https://cricketdata.org/api'