"""
Centralized Configuration
Loads settings from environment variables with sensible defaults.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from repo root (parent of /backend) and cwd
_REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_REPO_ROOT / ".env")
load_dotenv()

GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
GITHUB_API_URL: str = "https://api.github.com"

MAX_EVENTS: int = int(os.getenv("MAX_EVENTS", "300"))
ANALYSIS_LOOKBACK_DAYS: int = int(os.getenv("ANALYSIS_LOOKBACK_DAYS", "90"))
CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.7"))

CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "600"))  # 10 minutes

# Flask server
DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
HOST: str = os.getenv("HOST", "0.0.0.0")
PORT: int = int(os.getenv("PORT", "5000"))
