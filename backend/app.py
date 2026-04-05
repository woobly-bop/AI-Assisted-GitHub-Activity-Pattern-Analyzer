"""
Flask application entry point for the GitHub Developer Analyzer API.
Serves optional legacy HTML UI and JSON API for the React dashboard.
"""
from __future__ import annotations

import logging
import os
from typing import Any, Dict

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

import config
from analyzer import PatternAnalyzer
from github_api import GitHubAPI, GitHubAPIError
from insights import InsightGenerator
from validators import ValidationError, format_validation_error, validate_analyze_request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
_FRONTEND_DIR = os.path.join(_BACKEND_DIR, "..", "frontend")

app = Flask(
    __name__,
    template_folder=os.path.join(_FRONTEND_DIR, "templates"),
    static_folder=os.path.join(_FRONTEND_DIR, "static"),
)
CORS(
    app,
    resources={r"/api/*": {"origins": "*"}},
    supports_credentials=True,
)


@app.route("/")
def index() -> Any:
    """Serve legacy HTML UI if templates exist."""
    try:
        return render_template("index.html")
    except Exception:
        return (
            "<p>API is running. Use <code>npm run dev</code> in <code>frontend/</code> "
            "(port 5173) or POST JSON to <code>/api/analyze</code>.</p>",
            200,
            {"Content-Type": "text/html; charset=utf-8"},
        )


@app.route("/api/health", methods=["GET"])
def health() -> Any:
    return jsonify({"status": "ok", "service": "github-developer-analyzer", "version": "1.0.0"})


@app.route("/api/analyze", methods=["POST"])
def analyze() -> Any:
    """
    Analyze a GitHub user. Body: {"username": "octocat"}

    Response matches React client: username, profile, patterns, insights.
    """
    try:
        payload = request.get_json(silent=True)
        username, _options = validate_analyze_request(payload)

        token = (config.GITHUB_TOKEN or os.getenv("GITHUB_TOKEN", "")).strip()
        if not token:
            return (
                jsonify(
                    {
                        "error": True,
                        "message": (
                            "Server is missing GITHUB_TOKEN. "
                            "Set it in .env at the project root."
                        ),
                    }
                ),
                503,
            )

        api = GitHubAPI(token)
        user_data = api.fetch_user_activity(username)

        analyzer = PatternAnalyzer()
        patterns = analyzer.analyze(user_data)

        generator = InsightGenerator()
        insights = generator.generate_insights(patterns, user_data)

        body: Dict[str, Any] = {
            "username": username,
            "profile": user_data.get("profile", {}),
            "patterns": patterns,
            "insights": insights,
            "contributions": user_data.get("contributions", {}),
        }
        return jsonify(body), 200

    except ValidationError as exc:
        return jsonify(format_validation_error(exc)), 400
    except GitHubAPIError as exc:
        if exc.status_code == 404:
            return jsonify({"error": True, "message": str(exc)}), 404
        if exc.status_code == 403:
            return jsonify({"error": True, "message": str(exc)}), 403
        return jsonify({"error": True, "message": str(exc)}), 502
    except Exception as exc:  # noqa: BLE001
        logger.exception("Unexpected error during analysis")
        return jsonify({"error": True, "message": str(exc)}), 500


if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
