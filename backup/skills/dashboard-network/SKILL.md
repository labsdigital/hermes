---
name: dashboard-network
description: "Fix dashboard network issues in containerized Hermes."
version: 1.0.0
author: Hermes Agent + labsdigital
license: MIT
tags: [dashboard, networking, docker, container, troubleshooting]
---

# Dashboard Network Troubleshooting

Quick reference for diagnosing and fixing dashboard accessibility issues in containerized environments.

## Common Problem: "It works locally but not externally"

### Symptom
```bash
# Inside container - WORKS
curl http://localhost:8080/          # ✅ 200 OK
curl http://172.20.3.2:8080/        # ✅ 200 OK

# From outside - FAILS
curl http://103.153.189.177:8080/   # ❌ Connection refused
```

### Root Cause
Docker container network isolation:
- Container has internal IP (e.g., 172.20.3.2)
- Host has public IP (e.g., 103.153.189.177)
- No port forwarding configured by default
- Same issue affects all ports (80, 443, 3000, 8080, 9119)

## Diagnostic Checklist

Run these commands to diagnose:

```bash
# 1. Check if server is running
ps aux | grep "node server.js" | grep -v grep

# 2. Check what's listening
python3 -c "
import socket
ports = [80, 443, 3000, 8080, 8000, 9119]
for port in ports:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex(('127.0.0.1', port))
    print(f'Port {port}: {\"OPEN\" if result == 0 else \"closed\"}')
    sock.close()
"

# 3. Test local access
curl -s http://localhost:8080/ -o /dev/null -w "Local: %{http_code}\n"

# 4. Test external access (from inside container)
curl -s --max-time 3 http://103.153.189.177:8080/ -o /dev/null -w "External: %{http_code}\n"

# 5. Check container IPs
hostname -I

# 6. Check public IP
curl -s ifconfig.me
```

## Access Methods

### Method 1: SSH Tunnel (Easiest)
From your computer (not the server):
```bash
ssh -L 8080:localhost:8080 hermes@103.153.189.177
```
Then open: http://localhost:8080

**Pros:** Simple, secure, no config changes
**Cons:** Requires SSH access, tunnel must stay open

### Method 2: GitHub Pages (Best for public)
Deploy static HTML to GitHub and enable Pages:
1. Create folder: `/hermes-dashboard/`
2. Add `index.html` with embedded data
3. Push to GitHub
4. Enable Pages: Settings → Pages → Source: main branch, folder: /hermes-dashboard

**Pros:** Free, public URL, no server needed
**Cons:** Static data (needs re-push to update)

### Method 3: Cloudflare Tunnel (Public URL, real-time)
```bash
# Install cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.tgz
tar xzf cloudflared-linux-amd64.tgz
chmod +x cloudflared-linux-amd64

# Create tunnel
./cloudflared-linux-amd64 tunnel --url http://localhost:8080
```
Result: https://xxx.trycloudflare.com

**Pros:** Public URL, real-time, free tier
**Cons:** Requires download (wget may not be available)

### Method 4: Port Forwarding (Needs admin)
Contact VPS provider to forward port:
```
Host: 103.153.189.177:8080 → Container: 172.20.3.2:8080
```

**Pros:** Direct access, real-time
**Cons:** Requires admin access, may not be available

## GitHub Pages Troubleshooting

### Issue: 404 Not Found
```
https://username.github.io/repo/dashboard/ → 404
```

**Checklist:**
- [ ] Repository is PUBLIC (not private)
- [ ] GitHub Pages enabled in Settings → Pages
- [ ] Source set to correct branch (main)
- [ ] Folder path correct (/hermes-dashboard/)
- [ ] File named `index.html` (not `Index.html`)
- [ ] Waited 2-5 minutes after push for deployment

### Issue: CORS Errors in Browser Console
```
Access to script at '.../agents.json' blocked by CORS
```

**Cause:** Fetching JSON from different origin
**Solution:** Embed JSON directly in HTML (no separate fetch)

### Issue: Old Data Showing
**Cause:** Browser caching
**Solution:** Hard refresh (Ctrl+Shift+R) or add cache-busting query param

## Network Testing Commands

### Test from Inside Container
```bash
# All common ports
for port in 22 80 443 3000 8080 8000 9119; do
  curl -s --max-time 2 http://103.153.189.177:$port/ -o /dev/null -w "Port $port: %{http_code}\n"
done
```

### Test from Your Computer (if you have SSH access)
```bash
# SSH into server and test
ssh hermes@103.153.189.177 "curl -s http://localhost:8080/api/agents"
```

## Quick Fixes

### Restart Dashboard Server
```bash
# Kill existing
pkill -f "node server.js" || true

# Start fresh
cd /opt/data/hermes-dashboard
node server.js &

# Verify
sleep 2
curl http://localhost:8080/api/agents
```

### Generate Static Dashboard
```bash
cd /opt/data/hermes

# Get fresh data
curl http://localhost:8080/api/agents > hermes-dashboard/agents.json
curl http://localhost:8080/api/activity > hermes-dashboard/activity.json

# Embed in HTML (using Python)
python3 << 'PYEOF'
import json
with open('hermes-dashboard/index.html', 'r') as f:
    html = f.read()
with open('hermes-dashboard/agents.json', 'r') as f:
    html = html.replace('AGENTS_DATA', f.read())
with open('hermes-dashboard/activity.json', 'r') as f:
    html = html.replace('ACTIVITY_DATA', f.read())
with open('hermes-dashboard/index.html', 'w') as f:
    f.write(html)
PYEOF

# Commit and push
git add hermes-dashboard/
git commit -m "Dashboard: Update stats"
git push origin main
```

## Security Notes

- Dashboard has NO authentication by default
- Only expose via tunnel or private network
- Consider adding basic auth for production use
- Never commit API keys or tokens to Git

## GitHub Pages Limitation

**Critical:** GitHub Pages is STATIC hosting only. PHP scripts will be served as plain text, not executed.

For real-time dashboards needing server-side processing:
1. **Deploy to PHP hosting** (taraka.id, shared hosting)
2. **Use auto-export pattern** - SQLite → JSON → GitHub Pages
3. **Cron job automation** - Export every 5 minutes to approximate real-time

See `dashboard-pattern` skill for kanban export workflow and `references/kanban-export-pattern.md` for details.

## Related Skills
- `dashboard-pattern` - Dashboard deployment patterns
- `multi-subagent-orchestration` - Subagent management
- `github-repo-management` - GitHub operations

## GitHub Pages Limitation

**Critical:** GitHub Pages is STATIC hosting only. PHP scripts will be served as plain text, not executed.

For real-time dashboards needing server-side processing:
1. **Deploy to PHP hosting** (taraka.id, shared hosting)
2. **Use auto-export pattern** - SQLite → JSON → GitHub Pages
3. **Cron job automation** - Export every 5 minutes to approximate real-time

See `dashboard-pattern` skill for kanban export workflow.

## Related Skills
- `dashboard-pattern` - Dashboard deployment patterns
- `multi-subagent-orchestration` - Subagent management
- `github-repo-management` - GitHub operations
