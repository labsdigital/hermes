# Hermes Agent Dashboard

Real-time monitoring dashboard for multi-agent system.

## Architecture
- Backend: Flask (Python) + SQLite
- Frontend: Vanilla JS with auto-refresh (3s interval)
- Data source: Git history + Airtable API

## Deploy
```bash
cd /opt/data/hermes/dashboard
python3 server.py
# Access at http://localhost:5000
```

## API Endpoints
- GET /api/agents - Subagent status
- GET /api/activity - Recent commits (last 24h)
- GET /api/articles - Article counts per agent
- GET /api/airtable - Airtable sync status

## Features
- Auto-refresh every 3 seconds
- Commit timeline view
- Agent health status
- Mobile responsive