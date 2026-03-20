"""
Request Validation
Sanitizes and validates incoming API request data before processing.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from utils import validate_github_username


class ValidationError(Exception):
    """Raised when request data fails validation."""

    def __init__(self, message: str, field: Optional[str] = None) -> None:
        self.field = field
        super().__init__(message)


def validate_analyze_request(data: Optional[Dict[str, Any]]) -> Tuple[str, Dict[str, Any]]:
    """
    Validate the /api/analyze request payload.

    Args:
        data: Raw JSON body from the request.

    Returns:
        Tuple of (username, options) after sanitization.

    Raises:
        ValidationError: If the payload is invalid.
    """
    if not data or not isinstance(data, dict):
        raise ValidationError("Request body must be a JSON object")

    username = data.get("username", "").strip()
    if not username:
        raise ValidationError("Username is required", field="username")

    if not validate_github_username(username):
        raise ValidationError(
            "Invalid GitHub username format. Usernames may only contain "
            "alphanumeric characters or single hyphens, and cannot begin "
            "or end with a hyphen (max 39 characters).",
            field="username",
        )

    options: Dict[str, Any] = {}
    if "max_events" in data:
        try:
            max_events = int(data["max_events"])
            if max_events < 1 or max_events > 1000:
                raise ValueError
            options["max_events"] = max_events
        except (ValueError, TypeError):
            raise ValidationError(
                "max_events must be an integer between 1 and 1000",
                field="max_events",
            )

    return username, options


def sanitize_string(value: str, max_length: int = 200) -> str:
    """Strip whitespace and truncate to a safe maximum length."""
    return value.strip()[:max_length]


def format_validation_error(error: ValidationError) -> Dict[str, Any]:
    """Convert a ValidationError into a JSON-friendly response dict."""
    response: Dict[str, Any] = {
        "error": True,
        "message": str(error),
    }
    if error.field:
        response["field"] = error.field
    return response
