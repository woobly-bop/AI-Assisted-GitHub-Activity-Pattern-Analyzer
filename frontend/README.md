# GitHub Developer Analyzer — Frontend

React (Vite) + Tailwind CSS v4 + shadcn-style UI + Recharts + Framer Motion.

## Scripts

```bash
npm install
npm run dev      # http://localhost:5173
npm run build
npm run preview
```

## Backend

Start the Flask API from the repo root (port **5000**):

```bash
cd backend
pip install -r requirements.txt
# Set GITHUB_TOKEN in .env at repo root
python app.py
```

The Vite dev server proxies `/api/*` to `http://127.0.0.1:5000` (see `vite.config.js`).

## Environment

- **`VITE_API_URL`**: Optional. If unset, requests use relative `/api/...` (proxied in dev). For production, set to your API origin (e.g. `https://api.example.com`).

## Features

- Dark/light toggle (persisted)
- Live analysis + **demo fallback** if the API is down or missing token
- Download report (JSON export)
