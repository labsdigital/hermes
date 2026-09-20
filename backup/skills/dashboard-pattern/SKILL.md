---
name: dashboard-pattern
description: "Create static and real-time dashboards for Hermes subagents."
version: 1.0.0
author: Hermes Agent + labsdigital
license: MIT
tags: [dashboard, monitoring, github-pages, socket.io, node]
---

# Dashboard Deployment Patterns

Build monitoring dashboards for Hermes subagents with two approaches:

1. **Static Dashboard** (GitHub Pages) - Simple, free, accessible anywhere
2. **Real-time Dashboard** (Node.js + Socket.io) - Live updates, requires server

## When to Use Which

| Scenario | Recommendation |
|----------|---------------|
| Public monitoring, no maintenance | Static (GitHub Pages) |
| Internal use, real-time needed | Real-time (Node.js) |
| Container environment | Static (avoids port issues) |
| Need WebSocket/live updates | Real-time (Node.js) |

## Pattern 1: Static Dashboard (GitHub Pages)

### Why This Pattern
- No server maintenance required
- Free hosting on GitHub Pages
- Accessible from anywhere
- Simple update workflow

### File Structure
```
hermes/
└── hermes-dashboard/
    ├── index.html          # Main dashboard (self-contained)
    ├── agents.json         # Agent statistics
    ├── activity.json       # Recent git activity
    └── README.md           # Documentation
```

### HTML Template
```html
<!DOCTYPE html>
<html>
<head>
  <title>Hermes Dashboard</title>
  <style>
    /* Dark theme, responsive grid */
    body { background: #1a1a2e; color: #fff; font-family: sans-serif; }
    .agent-card { background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; }
  </style>
</head>
<body>
  <h1>🤖 Hermes Agent Dashboard</h1>
  <div id="agents"></div>
  <div id="activity"></div>
  
  <script>
    // Embed data directly in HTML
    const agentsData = AGENTS_DATA;
    const activityData = ACTIVITY_DATA;
    
    function render() {
      document.getElementById('agents').innerHTML = agentsData.map(a => 
        `<div class="agent-card">@${a.name}: ${a.articles} articles</div>`
      ).join('');
    }
    render();
  </script>
</body>
</html>
```

### Update Workflow
```bash
# 1. Get fresh data from running dashboard
curl http://localhost:8080/api/agents > agents.json
curl http://localhost:8080/api/activity > activity.json

# 2. Embed in HTML
python3 << 'EOF'
import json
with open('index.html', 'r') as f:
    html = f.read()
with open('agents.json', 'r') as f:
    html = html.replace('AGENTS_DATA', f.read())
with open('activity.json', 'r') as f:
    html = html.replace('ACTIVITY_DATA', f.read())
with open('index.html', 'w') as f:
    f.write(html)
EOF

# 3. Commit and push
git add hermes-dashboard/
git commit -m "Dashboard: Update stats"
git push origin main

# 4. Enable GitHub Pages (one-time)
# Settings → Pages → Source: main branch, folder: /hermes-dashboard
```

### Pitfalls
- ❌ Don't commit `node_modules/` - add to `.gitignore`
- ❌ Don't expect auto-refresh - users click refresh button
- ✅ GitHub Pages takes 2-5 minutes to deploy after push

## Pattern 2: Real-time Dashboard (Node.js)

### Why This Pattern
- Live updates via WebSocket
- No manual refresh needed
- Good for internal monitoring

### Stack
- Node.js + Express (HTTP server)
- Socket.io (WebSocket)
- Vanilla JS (no framework needed)

### Server Code (server.js)
```javascript
const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const { exec } = require('child_process');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

const PORT = process.env.PORT || 8080;

// Serve static files
app.use(express.static('public'));

// API endpoints
app.get('/api/agents', (req, res) => {
  res.json(getAgentsData());
});

app.get('/api/activity', (req, res) => {
  res.json(getActivity());
});

// WebSocket for real-time
io.on('connection', (socket) => {
  socket.emit('init', {
    agents: getAgentsData(),
    activity: getActivity(),
    stats: getSystemStats()
  });
  
  // Update every 5 seconds
  setInterval(() => {
    socket.emit('update', {
      agents: getAgentsData(),
      activity: getActivity()
    });
  }, 5000);
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`Dashboard running on http://0.0.0.0:${PORT}`);
});
```

### Frontend (public/index.html)
```html
<!DOCTYPE html>
<html>
<head>
  <title>Hermes Dashboard</title>
  <script src="/socket.io/socket.io.js"></script>
</head>
<body>
  <h1>🤖 Hermes Dashboard</h1>
  <div id="agents"></div>
  <div id="activity"></div>
  
  <script>
    const socket = io();
    
    socket.on('init', (data) => {
      renderAgents(data.agents);
      renderActivity(data.activity);
    });
    
    socket.on('update', (data) => {
      renderAgents(data.agents);
      renderActivity(data.activity);
    });
    
    function renderAgents(agents) {
      document.getElementById('agents').innerHTML = agents.map(a => 
        `<div class="card">@${a.name}: ${a.articles} articles</div>`
      ).join('');
    }
  </script>
</body>
</html>
```

### Running the Server
```bash
cd /opt/data/hermes-dashboard
npm install express socket.io
node server.js
```

## Critical: Container Network Isolation

### The Problem
Hermes runs inside Docker container:
- Container IP: 172.20.3.2 (internal only)
- Public IP: 103.153.189.177 (on HOST)
- Port forwarding NOT configured by default

### Test Results
```bash
# Inside container - works
curl http://localhost:8080/          # ✅ 200 OK
curl http://172.20.3.2:8080/        # ✅ 200 OK

# From outside - fails
curl http://103.153.189.177:8080/   # ❌ Connection refused
```

### Solutions

#### Option 1: SSH Tunnel (Recommended for local testing)
```bash
# From your computer (not server)
ssh -L 8080:localhost:8080 hermes@103.153.189.177

# Then open in browser
http://localhost:8080
```

#### Option 2: GitHub Pages (Recommended for public access)
- Deploy static HTML to `/hermes-dashboard/` folder
- Enable GitHub Pages in repo settings
- Access: `https://labsdigital.github.io/hermes/hermes-dashboard/`

#### Option 3: Cloudflare Tunnel (For public URL)
```bash
# Install cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.tgz
tar xzf cloudflared-linux-amd64.tgz

# Create tunnel
./cloudflared tunnel --url http://localhost:8080
# Result: https://xxx.trycloudflare.com
```

#### Option 4: Port Forwarding (Requires admin)
Contact VPS admin to forward port 8080 from host to container.

## Quick Reference

| Task | Command |
|------|---------|
| Generate static data | `curl http://localhost:8080/api/agents > agents.json` |
| Embed in HTML | Python script (see above) |
| Deploy to GitHub | `git add hermes-dashboard/ && git push` |
| Enable Pages | Settings → Pages → Source: main, folder: /hermes-dashboard |
| Start real-time server | `node server.js` |
| Test locally | `curl http://localhost:8080/api/agents` |

## Related Skills
- `multi-subagent-orchestration` - Subagent management patterns
- `github-repo-management` - Git and GitHub operations
- `dashboard-network` - Network troubleshooting guide
