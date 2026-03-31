"""Unit tests for PatternAnalyzer and utility functions."""
import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from analyzer import PatternAnalyzer
from utils import safe_divide, percentage, validate_github_username


class TestPatternAnalyzer(unittest.TestCase):
    """Tests for the PatternAnalyzer class."""

    def setUp(self):
        self.analyzer = PatternAnalyzer()
        self.sample_data = {
            "username": "testuser",
            "profile": {"login": "testuser", "public_repos": 5},
            "events": [
                {
                    "type": "PushEvent",
                    "created_at": "2026-03-20T14:00:00Z",
                    "repo": {"name": "user/repo1"},
                    "payload": {"size": 3},
                },
                {
                    "type": "PullRequestEvent",
                    "created_at": "2026-03-19T10:00:00Z",
                    "repo": {"name": "user/repo2"},
                    "payload": {},
                },
                {
                    "type": "IssuesEvent",
                    "created_at": "2026-03-18T09:00:00Z",
                    "repo": {"name": "user/repo1"},
                    "payload": {},
                },
            ],
            "repositories": [
                {
                    "name": "repo1",
                    "language": "Python",
                    "stargazers_count": 10,
                    "forks_count": 2,
                    "size": 3000,
                    "fork": False,
                    "description": "A test repo",
                    "topics": ["python"],
                },
                {
                    "name": "repo2",
                    "language": "JavaScript",
                    "stargazers_count": 5,
                    "forks_count": 1,
                    "size": 1500,
                    "fork": False,
                    "description": "JS project",
                    "topics": [],
                },
            ],
        }

    def test_analyze_returns_all_pattern_keys(self):
        result = self.analyzer.analyze(self.sample_data)
        expected_keys = {
            "time_patterns",
            "activity_patterns",
            "language_patterns",
            "repository_patterns",
            "collaboration_patterns",
            "productivity_metrics",
        }
        self.assertEqual(set(result.keys()), expected_keys)

    def test_time_patterns_peak_hours(self):
        result = self.analyzer.analyze(self.sample_data)
        peak_hours = result["time_patterns"]["peak_hours"]
        self.assertIsInstance(peak_hours, list)
        self.assertTrue(len(peak_hours) > 0)
        self.assertIn("hour", peak_hours[0])
        self.assertIn("count", peak_hours[0])

    def test_activity_diversity_matches_event_types(self):
        result = self.analyzer.analyze(self.sample_data)
        activity = result["activity_patterns"]
        self.assertEqual(activity["activity_diversity"], 3)
        self.assertEqual(activity["total_events"], 3)

    def test_language_patterns_primary_language(self):
        result = self.analyzer.analyze(self.sample_data)
        lang = result["language_patterns"]
        self.assertEqual(lang["primary_language"], "Python")
        self.assertEqual(lang["language_diversity"], 2)

    def test_repository_patterns_star_count(self):
        result = self.analyzer.analyze(self.sample_data)
        repo = result["repository_patterns"]
        self.assertEqual(repo["total_stars"], 15)
        self.assertEqual(repo["total_repositories"], 2)
        self.assertEqual(repo["owned_repositories"], 2)
        self.assertEqual(repo["forked_repositories"], 0)

    def test_collaboration_counts(self):
        result = self.analyzer.analyze(self.sample_data)
        collab = result["collaboration_patterns"]
        self.assertEqual(collab["pull_requests"], 1)
        self.assertEqual(collab["issues"], 1)
        self.assertEqual(collab["collaboration_frequency"], 2)

    def test_productivity_commits_from_push_events(self):
        result = self.analyzer.analyze(self.sample_data)
        prod = result["productivity_metrics"]
        self.assertEqual(prod["push_commits"], 3)
        self.assertEqual(prod["active_days"], 3)

    def test_empty_events(self):
        data = {**self.sample_data, "events": []}
        result = self.analyzer.analyze(data)
        self.assertEqual(result["activity_patterns"]["total_events"], 0)
        self.assertEqual(result["productivity_metrics"]["active_days"], 0)

    def test_empty_repos(self):
        data = {**self.sample_data, "repositories": []}
        result = self.analyzer.analyze(data)
        self.assertIsNone(result["language_patterns"]["primary_language"])
        self.assertEqual(result["repository_patterns"]["total_repositories"], 0)


class TestUtilityFunctions(unittest.TestCase):
    """Tests for utility helper functions."""

    def test_safe_divide_normal(self):
        self.assertEqual(safe_divide(10, 2), 5.0)

    def test_safe_divide_by_zero(self):
        self.assertEqual(safe_divide(10, 0), 0)

    def test_safe_divide_custom_default(self):
        self.assertEqual(safe_divide(10, 0, default=-1), -1)

    def test_percentage_normal(self):
        self.assertEqual(percentage(25, 100), 25.0)

    def test_percentage_zero_whole(self):
        self.assertEqual(percentage(10, 0), 0.0)

    def test_validate_username_valid(self):
        self.assertTrue(validate_github_username("octocat"))
        self.assertTrue(validate_github_username("my-user"))

    def test_validate_username_invalid(self):
        self.assertFalse(validate_github_username(""))
        self.assertFalse(validate_github_username(None))
        self.assertFalse(validate_github_username("-leading"))
        self.assertFalse(validate_github_username("trailing-"))
        self.assertFalse(validate_github_username("double--hyphen"))

    def test_validate_username_too_long(self):
        self.assertFalse(validate_github_username("a" * 40))


if __name__ == "__main__":
    unittest.main()
