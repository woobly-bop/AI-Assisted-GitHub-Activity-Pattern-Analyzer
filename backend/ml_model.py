"""
AI/ML Models for Advanced Pattern Recognition
Provides real sklearn-based classifiers with rule-based fallbacks when models
have not been trained yet.
"""
from __future__ import annotations

import logging
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import LabelEncoder, StandardScaler

    _SKLEARN_AVAILABLE = True
except ImportError:
    _SKLEARN_AVAILABLE = False

logger = logging.getLogger(__name__)


# ======================================================================
# Feature extraction
# ======================================================================

def extract_features(patterns: Dict[str, Any]) -> np.ndarray:
    """
    Build a flat feature vector from analyzer patterns.

    Features (in order):
        0  commits_per_day
        1  daily_average_events
        2  active_days
        3  consistency_ratio
        4  language_diversity
        5  collaboration_frequency
        6  collaboration_ratio
        7  total_stars
        8  total_repositories
        9  activity_diversity
    """
    prod = patterns.get("productivity_metrics", {})
    lang = patterns.get("language_patterns", {})
    collab = patterns.get("collaboration_patterns", {})
    repo = patterns.get("repository_patterns", {})
    act = patterns.get("activity_patterns", {})

    return np.array([
        prod.get("commits_per_day", 0),
        prod.get("daily_average_events", 0),
        prod.get("active_days", 0),
        prod.get("consistency_ratio", 0),
        lang.get("language_diversity", 0),
        collab.get("collaboration_frequency", 0),
        collab.get("collaboration_ratio", 0),
        repo.get("total_stars", 0),
        repo.get("total_repositories", 0),
        act.get("activity_diversity", 0),
    ], dtype=np.float64).reshape(1, -1)


def _generate_synthetic_training_data(
    n_samples: int = 200,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Generate synthetic training data that mirrors realistic GitHub user
    feature distributions.  Returns (X, y_event_type, y_trend).

    Event-type labels: 0=PushEvent, 1=PullRequestEvent, 2=IssuesEvent, 3=Other
    Trend labels:      0=low, 1=occasional, 2=moderate, 3=high
    """
    rng = np.random.RandomState(42)

    commits_per_day = rng.exponential(2.0, n_samples)
    daily_avg = rng.exponential(4.0, n_samples)
    active_days = rng.randint(1, 90, n_samples).astype(float)
    consistency = rng.beta(2, 5, n_samples)
    lang_div = rng.randint(1, 12, n_samples).astype(float)
    collab_freq = rng.poisson(8, n_samples).astype(float)
    collab_ratio = rng.beta(2, 5, n_samples)
    stars = rng.exponential(50, n_samples)
    repos = rng.randint(1, 80, n_samples).astype(float)
    act_div = rng.randint(1, 10, n_samples).astype(float)

    X = np.column_stack([
        commits_per_day, daily_avg, active_days, consistency,
        lang_div, collab_freq, collab_ratio, stars, repos, act_div,
    ])

    y_event = np.where(
        commits_per_day > 3, 0,
        np.where(collab_freq > 10, 1, np.where(collab_freq > 5, 2, 3))
    )

    y_trend = np.where(
        daily_avg > 10, 3,
        np.where(daily_avg > 5, 2, np.where(daily_avg > 2, 1, 0))
    )

    return X, y_event, y_trend


# ======================================================================
# Activity Predictor
# ======================================================================

EVENT_TYPE_LABELS = ["PushEvent", "PullRequestEvent", "IssuesEvent", "Other"]
TREND_LABELS = ["low_activity", "occasionally_active", "moderately_active", "highly_active"]


class ActivityPredictor:
    """Predicts future activity patterns using an ML model with rule-based fallback."""

    def __init__(self) -> None:
        self._event_model: Optional[RandomForestClassifier] = None
        self._trend_model: Optional[LogisticRegression] = None
        self._scaler: Optional[StandardScaler] = None
        self._trained = False

        if _SKLEARN_AVAILABLE:
            self._train_on_synthetic_data()

    # ------------------------------------------------------------------
    # Training
    # ------------------------------------------------------------------

    def _train_on_synthetic_data(self) -> None:
        """Train both classifiers on synthetic data so predictions work out of the box."""
        try:
            X, y_event, y_trend = _generate_synthetic_training_data()

            self._scaler = StandardScaler()
            X_scaled = self._scaler.fit_transform(X)

            self._event_model = RandomForestClassifier(
                n_estimators=80, max_depth=6, random_state=42
            )
            self._event_model.fit(X_scaled, y_event)

            self._trend_model = LogisticRegression(
                max_iter=500, random_state=42
            )
            self._trend_model.fit(X_scaled, y_trend)

            self._trained = True
            logger.info("ML models trained successfully on synthetic data")
        except Exception:
            logger.exception("Failed to train ML models; falling back to rules")
            self._trained = False

    # ------------------------------------------------------------------
    # Public prediction API
    # ------------------------------------------------------------------

    def predict_next_activity(self, patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Return predictions about next event type, active time, and productivity trend."""
        return {
            "likely_next_event_type": self._predict_event_type(patterns),
            "likely_active_time": self._predict_active_time(patterns),
            "productivity_trend": self._analyze_productivity_trend(patterns),
        }

    # ------------------------------------------------------------------
    # Event-type prediction
    # ------------------------------------------------------------------

    def _predict_event_type(self, patterns: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if self._trained:
            return self._ml_predict_event(patterns)
        return self._rule_predict_event(patterns)

    def _ml_predict_event(self, patterns: Dict[str, Any]) -> Dict[str, Any]:
        X = extract_features(patterns)
        X_scaled = self._scaler.transform(X)  # type: ignore[union-attr]
        proba = self._event_model.predict_proba(X_scaled)[0]  # type: ignore[union-attr]
        idx = int(np.argmax(proba))
        return {
            "event_type": EVENT_TYPE_LABELS[idx],
            "confidence": round(float(proba[idx]), 3),
            "method": "ml",
        }

    @staticmethod
    def _rule_predict_event(patterns: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        event_dist = patterns.get("activity_patterns", {}).get("event_type_distribution", {})
        if not event_dist:
            return None
        most_common = max(event_dist.items(), key=lambda x: x[1])
        total = sum(event_dist.values())
        return {
            "event_type": most_common[0],
            "confidence": round(most_common[1] / total, 3) if total else 0,
            "method": "rule",
        }

    # ------------------------------------------------------------------
    # Productivity trend
    # ------------------------------------------------------------------

    def _analyze_productivity_trend(self, patterns: Dict[str, Any]) -> Dict[str, Any]:
        if self._trained:
            return self._ml_predict_trend(patterns)
        return self._rule_predict_trend(patterns)

    def _ml_predict_trend(self, patterns: Dict[str, Any]) -> Dict[str, Any]:
        X = extract_features(patterns)
        X_scaled = self._scaler.transform(X)  # type: ignore[union-attr]
        proba = self._trend_model.predict_proba(X_scaled)[0]  # type: ignore[union-attr]
        idx = int(np.argmax(proba))
        trend = TREND_LABELS[idx]
        return {
            "trend": trend,
            "confidence": round(float(proba[idx]), 3),
            "daily_average": patterns.get("productivity_metrics", {}).get("daily_average_events", 0),
            "description": self._get_trend_description(trend),
            "method": "ml",
        }

    @staticmethod
    def _rule_predict_trend(patterns: Dict[str, Any]) -> Dict[str, Any]:
        daily_avg = patterns.get("productivity_metrics", {}).get("daily_average_events", 0)
        if daily_avg > 10:
            trend = "highly_active"
        elif daily_avg > 5:
            trend = "moderately_active"
        elif daily_avg > 2:
            trend = "occasionally_active"
        else:
            trend = "low_activity"
        return {
            "trend": trend,
            "daily_average": daily_avg,
            "description": ActivityPredictor._get_trend_description(trend),
            "method": "rule",
        }

    # ------------------------------------------------------------------
    # Active-time prediction (stays rule-based)
    # ------------------------------------------------------------------

    @staticmethod
    def _predict_active_time(patterns: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        peak_hours = patterns.get("time_patterns", {}).get("peak_hours", [])
        if not peak_hours:
            return None
        return {
            "most_likely_hour": peak_hours[0]["hour"],
            "peak_hours": [h["hour"] for h in peak_hours],
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _get_trend_description(trend: str) -> str:
        descriptions = {
            "highly_active": "User shows very high engagement with consistent daily activity",
            "moderately_active": "User maintains regular activity with good consistency",
            "occasionally_active": "User contributes periodically with moderate engagement",
            "low_activity": "User shows minimal activity, possibly inactive or new account",
        }
        return descriptions.get(trend, "Unknown activity pattern")


# ======================================================================
# Developer Profiler
# ======================================================================

class DeveloperProfiler:
    """Creates a developer profile based on activity patterns."""

    def create_profile(
        self, patterns: Dict[str, Any], user_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Build a comprehensive developer profile."""
        lang_patterns = patterns.get("language_patterns", {})
        repo_patterns = patterns.get("repository_patterns", {})
        collab_patterns = patterns.get("collaboration_patterns", {})

        return {
            "expertise_level": self._determine_expertise_level(patterns, user_data),
            "primary_language": lang_patterns.get("primary_language"),
            "specialization": self._determine_specialization(lang_patterns),
            "collaboration_style": self._determine_collaboration_style(collab_patterns),
            "project_focus": self._determine_project_focus(repo_patterns),
            "activity_consistency": self._measure_consistency(patterns),
        }

    # ------------------------------------------------------------------

    @staticmethod
    def _determine_expertise_level(
        patterns: Dict[str, Any], user_data: Dict[str, Any]
    ) -> str:
        repo_count = patterns.get("repository_patterns", {}).get("total_repositories", 0)
        total_stars = patterns.get("repository_patterns", {}).get("total_stars", 0)
        diversity = patterns.get("language_patterns", {}).get("language_diversity", 0)

        score = 0.0
        score += min(repo_count / 10, 3)
        score += min(total_stars / 100, 3)
        score += min(diversity / 3, 2)

        if score >= 6:
            return "expert"
        if score >= 4:
            return "intermediate"
        if score >= 2:
            return "beginner"
        return "novice"

    @staticmethod
    def _determine_specialization(lang_patterns: Dict[str, Any]) -> str:
        primary_lang = lang_patterns.get("primary_language")

        specializations = {
            "Python": "Data Science/Backend Development",
            "JavaScript": "Web Development",
            "TypeScript": "Modern Web Development",
            "Java": "Enterprise/Android Development",
            "Go": "Systems/Backend Development",
            "Rust": "Systems Programming",
            "C++": "Systems/Game Development",
            "C#": "Enterprise/.NET Development",
            "Ruby": "Web Development",
            "PHP": "Web Development",
            "Swift": "iOS/macOS Development",
            "Kotlin": "Android/Backend Development",
        }
        return specializations.get(primary_lang, "General Development")

    @staticmethod
    def _determine_collaboration_style(collab_patterns: Dict[str, Any]) -> str:
        freq = collab_patterns.get("collaboration_frequency", 0)
        if freq > 50:
            return "highly_collaborative"
        if freq > 20:
            return "team_player"
        if freq > 5:
            return "occasional_collaborator"
        return "solo_developer"

    @staticmethod
    def _determine_project_focus(repo_patterns: Dict[str, Any]) -> str:
        total_repos = repo_patterns.get("total_repositories", 0)
        avg_stars = repo_patterns.get("average_stars", 0)

        if avg_stars > 50:
            return "quality_focused"
        if total_repos > 50:
            return "quantity_focused"
        return "balanced"

    @staticmethod
    def _measure_consistency(patterns: Dict[str, Any]) -> str:
        metrics = patterns.get("productivity_metrics", {})
        active_days = metrics.get("active_days", 0)
        daily_avg = metrics.get("daily_average_events", 0)

        if active_days > 60 and daily_avg > 3:
            return "very_consistent"
        if active_days > 30 and daily_avg > 2:
            return "consistent"
        if active_days > 15:
            return "moderately_consistent"
        return "sporadic"
