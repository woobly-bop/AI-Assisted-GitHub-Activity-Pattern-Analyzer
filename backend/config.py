"""
Configuration settings for the application
Loads environment variables and API keys
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# GitHub API Configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')
GITHUB_API_URL = 'https://api.github.com'

# Flask Configuration
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
HOST = os.getenv('HOST', '127.0.0.1')
PORT = int(os.getenv('PORT', 5000))
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Analysis Configuration
MAX_EVENTS = int(os.getenv('MAX_EVENTS', 300))
ANALYSIS_LOOKBACK_DAYS = int(os.getenv('ANALYSIS_LOOKBACK_DAYS', 90))

# ML Model Configuration
MODEL_PATH = os.getenv('MODEL_PATH', 'models/')
CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', 0.7))
