"""
Insights Generation
Converts analyzed patterns into dynamic, human-readable insights with
comparative analysis and a placement-readiness score.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from ml_model import ActivityPredictor, DeveloperProfiler


# Benchmark values representing a "typical active" GitHub user.
# Used for comparative insights.
_BENCHMARKS = {
    "daily_average_events": 5.0,
    "commits_per_day": 3.0,
    "active_days": 30,
    "collaboration_frequency": 15,
    "language_diversity": 4,
    "total_stars": 50,
    "total_repositories": 20,
    "consistency_ratio": 0.4,
}


class InsightGenerator:
    """Generates human-readable insights from analyzed patterns."""

    def __init__(self) -> None:
        self.predictor = ActivityPredictor()
        self.profiler = DeveloperProfiler()

    def generate_insights(
        self,
        patterns: Dict[str, Any],
        user_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Generate comprehensive insights from patterns.

        Args:
            patterns: Analyzed patterns from PatternAnalyzer.
            user_data: Optional raw user data for enhanced insights.

        Returns:
            Dictionary of human-readable insights plus placement score.
        """
        insights: Dict[str, Any] = {
            "summary": self._generate_summary(patterns),
            "time_insights": self._generate_time_insights(patterns),
            "activity_insights": self._generate_activity_insights(patterns),
            "language_insights": self._generate_language_insights(patterns),
            "productivity_insights": self._generate_productivity_insights(patterns),
            "comparative_insights": self._generate_comparative_insights(patterns),
            "recommendations": self._generate_recommendations(patterns),
            "placement_score": self._calculate_placement_score(patterns),
        }

        if user_data:
            insights["predictions"] = self.predictor.predict_next_activity(patterns)
            insights["developer_profile"] = self.profiler.create_profile(patterns, user_data)

        return insights

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def _generate_summary(self, patterns: Dict[str, Any]) -> str:
        metrics = patterns.get("productivity_metrics", {})
        repo_patterns = patterns.get("repository_patterns", {})
        lang_patterns = patterns.get("language_patterns", {})
        collab = patterns.get("collaboration_patterns", {})

        active_days = metrics.get("active_days", 0)
        total_events = metrics.get("total_events", 0)
        primary_lang = lang_patterns.get("primary_language", "Unknown")
        total_repos = repo_patterns.get("total_repositories", 0)

        parts = [
            f"Developer has been active for {active_days} days with {total_events} total events.",
        ]

        if primary_lang != "Unknown":
            parts.append(f"Primary language is {primary_lang} across {total_repos} repositories.")

        collab_freq = collab.get("collaboration_frequency", 0)
        if collab_freq > 20:
            parts.append("Highly collaborative with significant PR and issue activity.")
        elif collab_freq > 5:
            parts.append("Participates in collaborative workflows through PRs and issues.")

        return " ".join(parts)

    # ------------------------------------------------------------------
    # Time insights
    # ------------------------------------------------------------------

    def _generate_time_insights(self, patterns: Dict[str, Any]) -> List[str]:
        time_patterns = patterns.get("time_patterns", {})
        peak_hours = time_patterns.get("peak_hours", [])
        most_active_day = time_patterns.get("most_active_day")
        weekend_ratio = time_patterns.get("weekend_ratio", 0)

        insights: List[str] = []

        if peak_hours:
            top_hour = peak_hours[0]["hour"]
            period = self._get_time_period(top_hour)
            insights.append(f"Most active during {period} hours (around {top_hour}:00)")

        if most_active_day:
            insights.append(f"Most productive on {most_active_day}s")

        if weekend_ratio > 0.3:
            insights.append(
                f"Significant weekend activity ({weekend_ratio:.0%} of events)"
            )
        elif weekend_ratio < 0.05 and peak_hours:
            insights.append("Primarily a weekday contributor")

        return insights

    # ------------------------------------------------------------------
    # Activity insights
    # ------------------------------------------------------------------

    def _generate_activity_insights(self, patterns: Dict[str, Any]) -> List[str]:
        activity = patterns.get("activity_patterns", {})
        event_dist = activity.get("event_type_distribution", {})
        pcts = activity.get("event_type_percentages", {})

        insights: List[str] = []
        total = sum(event_dist.values()) or 1

        if "PushEvent" in event_dist:
            pct = pcts.get("PushEvent", 0)
            insights.append(f"Pushes code frequently ({pct:.1f}% of activity)")

        if "PullRequestEvent" in event_dist:
            pct = pcts.get("PullRequestEvent", 0)
            insights.append(f"Actively participates in code reviews via pull requests ({pct:.1f}%)")

        if "IssuesEvent" in event_dist:
            insights.append("Engages in issue tracking and project management")

        if "CreateEvent" in event_dist:
            count = event_dist["CreateEvent"]
            insights.append(f"Frequently creates new branches or repositories ({count} events)")

        diversity = activity.get("activity_diversity", 0)
        if diversity > 5:
            insights.append(
                f"Diverse contribution profile spanning {diversity} event types"
            )

        return insights

    # ------------------------------------------------------------------
    # Language insights
    # ------------------------------------------------------------------

    def _generate_language_insights(self, patterns: Dict[str, Any]) -> List[str]:
        lang = patterns.get("language_patterns", {})
        distribution = lang.get("language_distribution", {})
        primary = lang.get("primary_language")
        diversity = lang.get("language_diversity", 0)
        top_langs = lang.get("top_languages", [])

        insights: List[str] = []

        if primary:
            pct = distribution.get(primary, 0)
            insights.append(f"Primary expertise in {primary} ({pct:.1f}% of repos)")

        if diversity > 5:
            insights.append(f"Polyglot developer with experience in {diversity} languages")
        elif diversity > 3:
            insights.append(f"Works with multiple languages ({diversity} total)")

        trending = {"Rust", "Go", "TypeScript", "Kotlin", "Zig", "Elixir"}
        used_trending = set(top_langs) & trending
        if used_trending:
            insights.append(f"Adopts modern languages: {', '.join(sorted(used_trending))}")

        return insights

    # ------------------------------------------------------------------
    # Productivity insights
    # ------------------------------------------------------------------

    def _generate_productivity_insights(self, patterns: Dict[str, Any]) -> List[str]:
        metrics = patterns.get("productivity_metrics", {})
        repo_patterns = patterns.get("repository_patterns", {})

        insights: List[str] = []

        daily_avg = metrics.get("daily_average_events", 0)
        if daily_avg > 10:
            insights.append("Extremely active developer with high daily engagement")
        elif daily_avg > 5:
            insights.append("Maintains consistent daily activity")
        elif daily_avg > 2:
            insights.append("Regular contributor with steady activity")
        else:
            insights.append("Light activity — consider contributing more regularly")

        cpd = metrics.get("commits_per_day", 0)
        if cpd > 5:
            insights.append(f"High commit frequency ({cpd:.1f} commits/day)")
        elif cpd > 2:
            insights.append(f"Healthy commit cadence ({cpd:.1f} commits/day)")

        consistency = metrics.get("consistency_ratio", 0)
        if consistency > 0.6:
            insights.append("Excellent consistency — active on most days in the analysis window")
        elif consistency > 0.3:
            insights.append("Moderate consistency — room to improve daily streak")

        total_stars = repo_patterns.get("total_stars", 0)
        if total_stars > 100:
            insights.append(f"Creates popular projects ({total_stars} total stars)")
        elif total_stars > 20:
            insights.append(f"Growing project recognition ({total_stars} total stars)")

        return insights

    # ------------------------------------------------------------------
    # Comparative insights (NEW)
    # ------------------------------------------------------------------

    @staticmethod
    def _generate_comparative_insights(patterns: Dict[str, Any]) -> List[str]:
        """Compare user metrics against community benchmarks."""
        metrics = patterns.get("productivity_metrics", {})
        lang = patterns.get("language_patterns", {})
        collab = patterns.get("collaboration_patterns", {})
        repo = patterns.get("repository_patterns", {})

        insights: List[str] = []

        daily_avg = metrics.get("daily_average_events", 0)
        bench = _BENCHMARKS["daily_average_events"]
        if daily_avg >= bench * 2:
            insights.append(f"Activity is {daily_avg / bench:.1f}x the community average — top-tier contributor")
        elif daily_avg >= bench:
            insights.append("Above-average activity compared to typical GitHub users")
        elif daily_avg >= bench * 0.5:
            insights.append("Activity is slightly below the community average")
        else:
            insights.append("Activity is well below the community average")

        collab_freq = collab.get("collaboration_frequency", 0)
        if collab_freq >= _BENCHMARKS["collaboration_frequency"] * 2:
            insights.append("Highly collaborative developer — significantly exceeds collaboration benchmarks")
        elif collab_freq >= _BENCHMARKS["collaboration_frequency"]:
            insights.append("Above-average collaboration through PRs and issues")

        stars = repo.get("total_stars", 0)
        if stars >= _BENCHMARKS["total_stars"] * 2:
            insights.append("Repository quality stands out — well above average star count")
        elif stars >= _BENCHMARKS["total_stars"]:
            insights.append("Repositories are gaining healthy community recognition")

        diversity = lang.get("language_diversity", 0)
        if diversity >= _BENCHMARKS["language_diversity"] * 2:
            insights.append("Exceptional language breadth — a true polyglot")
        elif diversity >= _BENCHMARKS["language_diversity"]:
            insights.append("Good language diversity across projects")

        return insights

    # ------------------------------------------------------------------
    # Placement readiness score (NEW)
    # ------------------------------------------------------------------

    @staticmethod
    def _calculate_placement_score(patterns: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compute a placement-readiness score (0-100) based on:
          - Activity consistency   (25 pts)
          - Collaboration          (25 pts)
          - Repository quality     (25 pts)
          - Language diversity      (25 pts)
        """
        metrics = patterns.get("productivity_metrics", {})
        collab = patterns.get("collaboration_patterns", {})
        repo = patterns.get("repository_patterns", {})
        lang = patterns.get("language_patterns", {})

        # --- Activity consistency (0-25) ---
        consistency_ratio = metrics.get("consistency_ratio", 0)
        active_days = metrics.get("active_days", 0)
        consistency_score = min(consistency_ratio / 0.6, 1.0) * 15 + min(active_days / 60, 1.0) * 10

        # --- Collaboration (0-25) ---
        collab_freq = collab.get("collaboration_frequency", 0)
        collab_ratio = collab.get("collaboration_ratio", 0)
        collab_score = min(collab_freq / 30, 1.0) * 15 + min(collab_ratio / 0.3, 1.0) * 10

        # --- Repo quality (0-25) ---
        total_stars = repo.get("total_stars", 0)
        total_repos = repo.get("total_repositories", 0)
        desc_count = repo.get("repos_with_description", 0)
        desc_ratio = (desc_count / total_repos) if total_repos else 0
        repo_score = min(total_stars / 100, 1.0) * 12 + min(total_repos / 30, 1.0) * 8 + min(desc_ratio, 1.0) * 5

        # --- Language diversity (0-25) ---
        diversity = lang.get("language_diversity", 0)
        lang_score = min(diversity / 6, 1.0) * 25

        raw = consistency_score + collab_score + repo_score + lang_score
        score = round(min(max(raw, 0), 100), 1)

        if score >= 75:
            level = "High"
        elif score >= 40:
            level = "Medium"
        else:
            level = "Low"

        reasons: List[str] = []
        if consistency_score >= 20:
            reasons.append("strong activity consistency")
        if collab_score >= 20:
            reasons.append("excellent collaboration record")
        if repo_score >= 20:
            reasons.append("high-quality repositories")
        if lang_score >= 20:
            reasons.append("broad language expertise")

        if not reasons:
            if score >= 40:
                reasons.append("balanced profile across multiple dimensions")
            else:
                reasons.append("profile is developing — increase activity and collaboration")

        return {
            "score": score,
            "level": level,
            "reason": "; ".join(reasons),
            "breakdown": {
                "activity_consistency": round(consistency_score, 1),
                "collaboration": round(collab_score, 1),
                "repository_quality": round(repo_score, 1),
                "language_diversity": round(lang_score, 1),
            },
        }

    # ------------------------------------------------------------------
    # Recommendations
    # ------------------------------------------------------------------

    def _generate_recommendations(self, patterns: Dict[str, Any]) -> List[str]:
        recommendations: List[str] = []

        metrics = patterns.get("productivity_metrics", {})
        lang = patterns.get("language_patterns", {})
        collab = patterns.get("collaboration_patterns", {})
        repo = patterns.get("repository_patterns", {})

        if metrics.get("active_days", 0) < 30:
            recommendations.append(
                "Maintain more consistent daily activity to build momentum and visibility"
            )

        if metrics.get("consistency_ratio", 0) < 0.3:
            recommendations.append(
                "Aim for regular small contributions rather than infrequent large bursts"
            )

        if lang.get("language_diversity", 0) < 3:
            recommendations.append(
                "Explore additional programming languages to broaden your skill set"
            )

        collab_freq = collab.get("collaboration_frequency", 0)
        if collab_freq < 10:
            recommendations.append(
                "Increase collaboration through code reviews, pull requests, and issue discussions"
            )

        desc_ratio = 0
        total_repos = repo.get("total_repositories", 0)
        if total_repos:
            desc_ratio = repo.get("repos_with_description", 0) / total_repos
        if desc_ratio < 0.5:
            recommendations.append(
                "Add descriptions and README files to your repositories for better discoverability"
            )

        if repo.get("total_stars", 0) < 10:
            recommendations.append(
                "Share your projects on social platforms and contribute to popular open-source projects"
            )

        return recommendations

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _get_time_period(hour: int) -> str:
        if 5 <= hour < 12:
            return "morning"
        if 12 <= hour < 17:
            return "afternoon"
        if 17 <= hour < 21:
            return "evening"
        return "night"
