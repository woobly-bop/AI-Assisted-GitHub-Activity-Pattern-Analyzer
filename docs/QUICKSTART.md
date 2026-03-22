# Quick Start Guide

## Initial Setup (First Time Only)

### 1. Install Python Dependencies
```bash
pip install -r backend/requirements.txt
```

### 2. Configure GitHub Token
Edit the `.env` file and add your GitHub Personal Access Token:
```env
GITHUB_TOKEN=your_github_personal_access_token_here
```

To create a GitHub token:
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo`, `user`
4. Copy the generated token and paste it in `.env`

### 3. Run the Application
```bash
python run.py
```

### 4. Access the Application
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

## Usage

1. Enter a GitHub username (e.g., `octocat`, `torvalds`, `gvanrossum`)
2. Click "Analyze Activity"
3. View the comprehensive analysis

## Troubleshooting

### "Module not found" error
```bash
pip install -r backend/requirements.txt
```

### "API rate limit exceeded" error
- Make sure your `GITHUB_TOKEN` is set in `.env`
- Wait a few minutes for rate limit to reset
- Use an authenticated token for higher rate limits (5000/hour vs 60/hour)

### Flask app won't start
- Check if port 5000 is already in use
- Change PORT in `.env` file to use a different port

## Next Steps

- Customize the analysis parameters in `backend/config.py`
- Modify the UI styling in `frontend/static/css/style.css`
- Extend the ML models in `backend/ml_model.py`
- Add more insights in `backend/insights.py`

## Features Overview

✅ **User Profile Analysis** - Name, bio, repos, followers
✅ **Productivity Metrics** - Commits, events, active days
✅ **Language Distribution** - Primary languages and expertise
✅ **Time Patterns** - Peak hours and most active days
✅ **Activity Types** - Push, PR, Issues, etc.
✅ **AI Insights** - Developer profiling and recommendations

## API Testing

You can also test the API directly:

```bash
curl -X POST http://127.0.0.1:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"username": "octocat"}'
```

## Development Mode

The app runs in DEBUG mode by default. For production:
1. Set `DEBUG=False` in `.env`
2. Use a production WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 127.0.0.1:5000 backend.app:app
```
