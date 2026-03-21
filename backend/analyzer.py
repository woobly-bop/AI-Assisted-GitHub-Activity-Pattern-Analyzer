"""
Pattern Analysis Engine
Processes raw GitHub data into structured patterns consumed by ML models and insights.

Data flow:  github_api -> analyzer -> ml_model -> insights
"""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional

from utils import safe_divide, percentage


class PatternAnalyzer:
    """Transforms raw GitHub user data into actionable pattern dictionaries."""

    DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    def analyze(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the full analysis pipeline on raw user data.

        Args:
            user_data: Output of GitHubAPI.fetch_user_activity().

        Returns:
            A dict with keys: time_patterns, activity_patterns, language_patterns,
            repository_patterns, collaboration_patterns, productivity_metrics.
        """
        events: List[Dict] = user_data.get("events", [])
        repos: List[Dict] = user_data.get("repositories", [])
        profile: Dict = user_data.get("profile", {})

        return {
            "time_patterns": self._analyze_time_patterns(events),
            "activity_patterns": self._analyze_activity_patterns(events),
            "language_patterns": self._analyze_language_patterns(repos),
            "repository_patterns": self._analyze_repository_patterns(repos, profile),
            "collaboration_patterns": self._analyze_collaboration_patterns(events),
            "productivity_metrics": self._analyze_productivity_metrics(events, repos),
        }

    # ------------------------------------------------------------------
    # Time patterns
    # ------------------------------------------------------------------

    def _analyze_time_patterns(self, events: List[Dict]) -> Dict[str, Any]:
        hourly: Counter = Counter()
        daily: Counter = Counter()

        for event in events:
            dt = self._parse_event_time(event)
            if dt is None:
                continue
            hourly[dt.hour] += 1
            daily[dt.strftime("%A")] += 1

        peak_hours = [
            {"hour": hour, "count": count}
            for hour, count in hourly.most_common(5)
        ]

        most_active_day: Optional[str] = daily.most_common(1)[0][0] if daily else None

        hourly_distribution = dict(sorted(hourly.items()))
        daily_distribution = {
            day: daily.get(day, 0) for day in self.DAY_NAMES
        }

        weekend_count = daily.get("Saturday", 0) + daily.get("Sunday", 0)
        total_count = sum(daily.values())
        weekend_ratio = round(weekend_count / total_count, 3) if total_count > 0 else 0.0
        weekday_count = total_count - weekend_count

        return {
            "peak_hours": peak_hours,
            "most_active_day": most_active_day,
            "hourly_distribution": hourly_distribution,
            "daily_distribution": daily_distribution,
            "weekend_ratio": weekend_ratio,
            "weekday_events": weekday_count,
            "weekend_events": weekend_count,
        }

    # ------------------------------------------------------------------
    # Activity patterns
    # ------------------------------------------------------------------

    def _analyze_activity_patterns(self, events: List[Dict]) -> Dict[str, Any]:
        type_counter: Counter = Counter()
        for event in events:
            type_counter[event.get("type", "Unknown")] += 1

        total = sum(type_counter.values())

        return {
            "event_type_distribution": dict(type_counter),
            "event_type_percentages": {
                etype: percentage(count, total) for etype, count in type_counter.items()
            },
            "activity_diversity": len(type_counter),
            "total_events": total,
            "most_common_event": type_counter.most_common(1)[0][0] if type_counter else None,
        }

    # ------------------------------------------------------------------
    # Language patterns
    # ------------------------------------------------------------------

    def _analyze_language_patterns(self, repos: List[Dict]) -> Dict[str, Any]:
        lang_counter: Counter = Counter()
        lang_bytes: Counter = Counter()

        for repo in repos:
            lang = repo.get("language")
            if lang:
                lang_counter[lang] += 1
                lang_bytes[lang] += repo.get("size", 0)

        total_repos_with_lang = sum(lang_counter.values()) or 1
        distribution = {
            lang: percentage(count, total_repos_with_lang)
            for lang, count in lang_counter.most_common()
        }

        primary_language = lang_counter.most_common(1)[0][0] if lang_counter else None

        return {
            "primary_language": primary_language,
            "language_distribution": distribution,
            "language_repo_counts": dict(lang_counter),
            "language_diversity": len(lang_counter),
            "top_languages": [lang for lang, _ in lang_counter.most_common(5)],
        }

    # ------------------------------------------------------------------
    # Repository patterns
    # ------------------------------------------------------------------

    def _analyze_repository_patterns(
        self, repos: List[Dict], profile: Dict
    ) -> Dict[str, Any]:
        total_stars = sum(r.get("stargazers_count", 0) for r in repos)
        total_forks = sum(r.get("forks_count", 0) for r in repos)
        total_repos = len(repos)
        avg_stars = safe_divide(total_stars, total_repos)
        avg_forks = safe_divide(total_forks, total_repos)

        owned = [r for r in repos if not r.get("fork", False)]
        forked = [r for r in repos if r.get("fork", False)]

        has_description = sum(1 for r in repos if r.get("description"))
        has_topics = sum(1 for r in repos if r.get("topics"))

        return {
            "total_repositories": total_repos,
            "owned_repositories": len(owned),
            "forked_repositories": len(forked),
            "total_stars": total_stars,
            "total_forks": total_forks,
            "average_stars": round(avg_stars, 2),
            "average_forks": round(avg_forks, 2),
            "repos_with_description": has_description,
            "repos_with_topics": has_topics,
            "public_repos_profile": profile.get("public_repos", total_repos),
        }

    # ------------------------------------------------------------------
    # Collaboration patterns
    # ------------------------------------------------------------------

    def _analyze_collaboration_patterns(self, events: List[Dict]) -> Dict[str, Any]:
        pr_events = 0
        pr_review_events = 0
        issue_events = 0
        issue_comment_events = 0
        fork_events = 0
        watch_events = 0

        for event in events:
            etype = event.get("type", "")
            if etype == "PullRequestEvent":
                pr_events += 1
            elif etype == "PullRequestReviewEvent":
                pr_review_events += 1
            elif etype == "IssuesEvent":
                issue_events += 1
            elif etype == "IssueCommentEvent":
                issue_comment_events += 1
            elif etype == "ForkEvent":
                fork_events += 1
            elif etype == "WatchEvent":
                watch_events += 1

        collaboration_frequency = (
            pr_events + pr_review_events + issue_events + issue_comment_events
        )

        total = len(events) or 1
        collaboration_ratio = round(collaboration_frequency / total, 3)

        return {
            "pull_requests": pr_events,
            "pr_reviews": pr_review_events,
            "issues": issue_events,
            "issue_comments": issue_comment_events,
            "forks": fork_events,
            "watches": watch_events,
            "collaboration_frequency": collaboration_frequency,
            "collaboration_ratio": collaboration_ratio,
        }

    # ------------------------------------------------------------------
    # Productivity metrics
    # ------------------------------------------------------------------

    def _analyze_productivity_metrics(
        self, events: List[Dict], repos: List[Dict]
    ) -> Dict[str, Any]:
        active_dates: set = set()
        push_commits = 0

        for event in events:
            dt = self._parse_event_time(event)
            if dt is None:
                continue
            active_dates.add(dt.date())

            if event.get("type") == "PushEvent":
                payload = event.get("payload", {})
                push_commits += payload.get("size", 0)

        active_days = len(active_dates)
        total_events = len(events)

        if active_dates:
            date_range = (max(active_dates) - min(active_dates)).days + 1
        else:
            date_range = 1

        commits_per_day = safe_divide(push_commits, date_range)
        daily_average_events = safe_divide(total_events, date_range)
        consistency_ratio = safe_divide(active_days, date_range)

        repos_contributed: set = set()
        for event in events:
            repo = event.get("repo", {})
            if repo:
                repos_contributed.add(repo.get("name", ""))

        return {
            "total_events": total_events,
            "active_days": active_days,
            "date_range_days": date_range,
            "push_commits": push_commits,
            "commits_per_day": round(commits_per_day, 2),
            "daily_average_events": round(daily_average_events, 2),
            "consistency_ratio": round(consistency_ratio, 3),
            "repositories_contributed": len(repos_contributed),
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_event_time(event: Dict) -> Optional[datetime]:
        raw = event.get("created_at")
        if not raw:
            return None
        try:
            return datetime.strptime(raw, "%Y-%m-%dT%H:%M:%SZ")
        except (ValueError, TypeError):
            return None
