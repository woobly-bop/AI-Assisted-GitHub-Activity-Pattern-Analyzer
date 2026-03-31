# AI-Assisted GitHub Activity Pattern Analyzer

An intelligent web application that analyzes GitHub user activity using data analytics and machine learning to identify productivity patterns, behavioral trends, and contribution insights.

## Features

- Fetches real-time GitHub activity using the GitHub REST API
- Analyzes commit behavior, collaboration patterns, and coding habits over time
- Detects most active days, peak hours, and weekend activity ratios
- Generates AI-based productivity insights using trained sklearn classifiers
- Computes a **Placement Readiness Score** (0–100) based on consistency, collaboration, repo quality, and language diversity
- Provides comparative insights against community benchmarks
- In-memory caching layer to avoid redundant API calls
- User-friendly web interface with trend visualizations

---

## System Architecture

```
Frontend (HTML / CSS / JS)
        ⬇
  Flask Backend API
        ⬇
   GitHub REST API
        ⬇
 PatternAnalyzer (analyzer.py)
        ⬇
 ML Models (scikit-learn)
        ⬇
  Insight Generator
```

---

## Tech Stack

**Frontend:**
- HTML, CSS, JavaScript

**Backend:**
- Python 3.10+
- Flask

**AI / ML:**
- NumPy
- Scikit-learn (RandomForest, LogisticRegression)

**API:**
- GitHub REST API v3
