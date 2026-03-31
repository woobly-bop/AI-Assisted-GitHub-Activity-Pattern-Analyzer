"""
GitHub API Integration
Handles all GitHub data fetching with in-memory caching and robust error handling.
"""
from __future__ import annotations

import logging
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import requests

import config

logger = logging.getLogger(__name__)


class CacheEntry:
    """Represents a single cache value with an expiry timestamp."""

    __slots__ = ("data", "expires_at")

    def __init__(self, data: Any, ttl: int) -> None:
        self.data = data
        self.expires_at = time.monotonic() + ttl

    @property
    def is_expired(self) -> bool:
        return time.monotonic() >= self.expires_at


class APICache:
    """Simple in-memory TTL cache to avoid repeated GitHub API calls."""

    def __init__(self, ttl: int = config.CACHE_TTL_SECONDS) -> None:
        self._store: Dict[str, CacheEntry] = {}
        self._ttl = ttl

    def get(self, key: str) -> Optional[Any]:
        entry = self._store.get(key)
        if entry is None or entry.is_expired:
            self._store.pop(key, None)
            return None
        return entry.data

    def set(self, key: str, value: Any) -> None:
        self._store[key] = CacheEntry(value, self._ttl)

    def invalidate(self, key: str) -> None:
        self._store.pop(key, None)

    def clear(self) -> None:
        self._store.clear()


class GitHubAPIError(Exception):
    """Raised when a GitHub API call fails in a non-recoverable way."""

    def __init__(self, message: str, status_code: Optional[int] = None) -> None:
        self.status_code = status_code
        super().__init__(message)


class GitHubAPI:
    """Fetches user data from the GitHub REST API."""

    def __init__(self, token: str) -> None:
        self.token = token
        self.base_url: str = config.GITHUB_API_URL
        self.headers: Dict[str, str] = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
        }
        self._cache = APICache()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def fetch_user_activity(self, username: str) -> Dict[str, Any]:
        """
        Fetch comprehensive activity data for a GitHub user.

        Events are fetched **once** and reused for contribution stats,
        eliminating the duplicate-call issue.

        Returns:
            dict with keys: username, profile, events, repositories, contributions
        """
        cache_key = f"user_activity:{username}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            logger.info("Cache hit for %s", username)
            return cached

        profile = self._get_user_profile(username)
        events = self._get_user_events(username)
        repos = self._get_user_repos(username)
        contributions = self._build_contribution_stats(events)

        user_data: Dict[str, Any] = {
            "username": username,
            "profile": profile,
            "events": events,
            "repositories": repos,
            "contributions": contributions,
        }

        self._cache.set(cache_key, user_data)
        return user_data

    # ------------------------------------------------------------------
    # Private fetchers
    # ------------------------------------------------------------------

    def _get_user_profile(self, username: str) -> Dict[str, Any]:
        """Fetch user profile information."""
        url = f"{self.base_url}/users/{username}"
        return self._request(url)

    def _get_user_events(self, username: str) -> List[Dict[str, Any]]:
        """Fetch recent user events with pagination."""
        url = f"{self.base_url}/users/{username}/events"
        per_page = min(config.MAX_EVENTS, 100)

        events: List[Dict[str, Any]] = []
        page = 1

        while len(events) < config.MAX_EVENTS:
            data = self._request(url, params={"per_page": per_page, "page": page})
            if not data:
                break
            events.extend(data)
            page += 1

        return events[: config.MAX_EVENTS]

    def _get_user_repos(self, username: str) -> List[Dict[str, Any]]:
        """Fetch user repositories sorted by last update."""
        url = f"{self.base_url}/users/{username}/repos"
        return self._request(url, params={"sort": "updated", "per_page": 100})

    # ------------------------------------------------------------------
    # Contribution stats (computed from already-fetched events)
    # ------------------------------------------------------------------

    @staticmethod
    def _build_contribution_stats(events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Derive contribution statistics from the events list.

        This is a pure computation -- no API call is made.
        """
        stats: Dict[str, Any] = {
            "total_events": len(events),
            "event_types": {},
            "active_days": set(),
            "repositories_contributed": set(),
        }

        for event in events:
            event_type = event.get("type", "Unknown")
            stats["event_types"][event_type] = stats["event_types"].get(event_type, 0) + 1

            raw_ts = event.get("created_at", "")
            try:
                created_at = datetime.strptime(raw_ts, "%Y-%m-%dT%H:%M:%SZ")
                stats["active_days"].add(created_at.date().isoformat())
            except (ValueError, TypeError):
                pass

            repo = event.get("repo")
            if repo:
                stats["repositories_contributed"].add(repo.get("name", ""))

        stats["active_days"] = sorted(stats["active_days"], reverse=True)
        stats["repositories_contributed"] = list(stats["repositories_contributed"])

        return stats

    # ------------------------------------------------------------------
    # HTTP helper
    # ------------------------------------------------------------------

    def _request(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Execute a GET request with unified error handling.

        Raises:
            GitHubAPIError on HTTP errors or network failures.
        """
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=15)
        except requests.ConnectionError as exc:
            raise GitHubAPIError(f"Network error reaching GitHub: {exc}") from exc
        except requests.Timeout as exc:
            raise GitHubAPIError("GitHub API request timed out") from exc

        if response.status_code == 404:
            raise GitHubAPIError(
                f"GitHub user or resource not found: {url}", status_code=404
            )
        if response.status_code == 403:
            remaining = response.headers.get("X-RateLimit-Remaining", "?")
            raise GitHubAPIError(
                f"GitHub API rate limit exceeded (remaining: {remaining})",
                status_code=403,
            )
        if response.status_code >= 400:
            raise GitHubAPIError(
                f"GitHub API error {response.status_code}: {response.text[:200]}",
                status_code=response.status_code,
            )

        return response.json()
