"""
Utility Helper Functions
Common utilities used across the application.
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Tuple, Union


def format_date(date_string: str, format_str: str = "%Y-%m-%d") -> str:
    """Format an ISO-8601 date string to a human-readable format."""
    try:
        date_obj = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
        return date_obj.strftime(format_str)
    except (ValueError, TypeError):
        return date_string


def calculate_date_range(days_back: int = 90) -> Tuple[datetime, datetime]:
    """Return (start_date, end_date) looking *days_back* days into the past."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    return start_date, end_date


def safe_divide(
    numerator: Union[int, float],
    denominator: Union[int, float],
    default: Union[int, float] = 0,
) -> float:
    """Safely divide two numbers, returning *default* on division-by-zero."""
    try:
        return numerator / denominator if denominator != 0 else default
    except (TypeError, ZeroDivisionError):
        return float(default)


def truncate_text(
    text: Optional[str], max_length: int = 100, suffix: str = "..."
) -> Optional[str]:
    """Truncate *text* to *max_length* characters, appending *suffix* if needed."""
    if not text or len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def save_json(data: Any, filename: str) -> None:
    """Serialize *data* to a JSON file."""
    with open(filename, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)


def load_json(filename: str) -> Dict[str, Any]:
    """Deserialize a JSON file, returning an empty dict on missing file."""
    try:
        with open(filename, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return {}


def validate_github_username(username: Optional[str]) -> bool:
    """
    Validate a GitHub username against GitHub's format rules:
    alphanumeric + single hyphens, no leading/trailing hyphen, max 39 chars.
    """
    if not username:
        return False
    if len(username) > 39:
        return False
    if username.startswith("-") or username.endswith("-"):
        return False
    if "--" in username:
        return False
    return all(c.isalnum() or c == "-" for c in username)


def percentage(
    part: Union[int, float],
    whole: Union[int, float],
    decimal_places: int = 2,
) -> float:
    """Calculate ``(part / whole) * 100``, rounded to *decimal_places*."""
    if whole == 0:
        return 0.0
    return round((part / whole) * 100, decimal_places)
