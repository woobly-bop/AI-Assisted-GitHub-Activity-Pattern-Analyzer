"""
Centralized Configuration
Loads settings from environment variables with sensible defaults.
"""
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
GITHUB_API_URL: str = "https://api.github.com"

MAX_EVENTS: int = int(os.getenv("MAX_EVENTS", "300"))
ANALYSIS_LOOKBACK_DAYS: int = int(os.getenv("ANALYSIS_LOOKBACK_DAYS", "90"))
CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.7"))

CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "600"))  # 10 minutes
