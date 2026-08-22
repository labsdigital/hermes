# Hermes Dashboard

Static dashboard for monitoring Hermes Agent subagents.

## Features

- 🤖 Agent statistics (@max, @elon, @chalbi, @taraka)
- 📊 Activity timeline
- 📈 System metrics
- 🔄 Refreshable static data

## Access

- **GitHub Pages**: https://labsdigital.github.io/hermes-dashboard/
- **Source**: https://github.com/labsdigital/hermes/tree/main/hermes-dashboard

## How it works

1. Dashboard runs on Node.js (port 8080) inside container
2. Static data is exported to JSON files
3. GitHub Pages serves the static HTML+JSON
4. User clicks "Refresh" to get latest data

## API Endpoints

- `/api/agents` - Agent statistics
- `/api/activity` - Recent git activity
- `/api/stats` - System metrics

---
Powered by Hermes Agent
