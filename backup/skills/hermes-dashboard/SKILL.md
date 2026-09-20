---
name: hermes-dashboard
description: Build PHP dashboards for Hermes agents with file auth.
version: 1.0.0
author: Hermes Agent + labsdigital
license: MIT
tags: [php, dashboard, hermes, web-app, agent-management]
---

# Hermes Dashboard

Build web-based dashboards for managing Hermes multi-agent systems. PHP + HTML applications with file-based authentication, real-time agent monitoring, chat interfaces, and system statistics.

## When to Use

- User requests a web dashboard for Hermes agent management
- Need PHP-based control panel for multi-agent systems
- Building monitoring interfaces with agent status, chat, and stats
- Creating web UIs that proxy to Hermes Gateway API (port 9119)

## Core Architecture

### File Structure Pattern
```
dashboard-name/
├── index.php              # Main dashboard
├── login.php              # Authentication page
├── chat.php               # Chat interface
├── api/
│   ├── agents.php         # Agent status API
│   ├── activity.php       # Git activity API
│   ├── chat.php           # Chat proxy API
│   ├── stats.php          # System statistics API
│   └── tasks.php          # Task management API
├── assets/css/styles.css  # Main stylesheet (MyStyle1)
├── includes/
│   ├── header.php         # Page header (session check)
│   └── footer.php         # Page footer
├── data/
│   ├── users.json         # User credentials (bcrypt hashes)
│   ├── agents.json        # Agent configurations
│   └── logs/              # Activity logs
└── scripts/
    └── setup.sh           # Installation script
```

### Key Design Principles

1. **File-Based Auth**: No database dependency — users stored in JSON
2. **Hermes Gateway Proxy**: All agent interactions go through localhost:9119
3. **MyStyle1 Design System**: Inter font, orange accent (#f97316), clean cards
4. **Responsive Layout**: Works on desktop and mobile
5. **Demo Mode Fallback**: Works even when Hermes gateway is offline

## Authentication System

### users.json Structure
```json
{
  "users": [
    {
      "id": "user_001",
      "username": "tamim",
      "name": "Master Tamim",
      "password_hash": "$2y$10$...",
      "created_at": "2026-08-24",
      "last_login": null
    }
  ]
}
```

### Password Hash Generation
```bash
# Generate bcrypt hash
php -r 'echo password_hash("yourpassword", PASSWORD_BCRYPT);'
```

### Session Management
```php
session_start();
if (!isset($_SESSION['authenticated']) || $_SESSION['authenticated'] !== true) {
    header('Location: login.php');
    exit;
}
```

### Security Features
- ✅ Bcrypt password hashing
- ✅ Session regeneration on login
- ✅ Input sanitization (htmlspecialchars)
- ✅ Rate limiting on login (track failures in lockout.json)

## Hermes Gateway Integration

### API Proxy Pattern
```php
function callHermesAPI($endpoint, $method = 'GET', $data = null) {
    $url = 'http://localhost:9119' . $endpoint;
    $ch = curl_init();
    
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 30);
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
    
    if ($method === 'POST' && $data) {
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    }
    
    $response = curl_exec($ch);
    curl_close($ch);
    
    return json_decode($response, true);
}
```

### Chat Forwarding
```php
// api/chat.php
$payload = [
    'agent' => $input['agent'],
    'message' => $input['message'],
    'session_id' => session_id()
];

$result = callHermesAPI('/api/v1/chat', 'POST', $payload);

echo json_encode([
    'success' => true,
    'reply' => $result['message'] ?? 'Response received',
    'timestamp' => date('c')
]);
```

### Demo Mode (Fallback)
When Hermes gateway is unavailable:
```php
if (!$result || $httpCode !== 200) {
    echo json_encode([
        'success' => true,
        'reply' => "Demo mode: Connect to Hermes gateway for real responses.",
        'demo' => true
    ]);
}
```

## Dashboard Components

### Stats Cards
```html
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-icon">🤖</div>
        <div class="stat-value" id="agentCount">5</div>
        <div class="stat-label">Total Agents</div>
    </div>
</div>
```

### Agent Status Cards
```html
<div class="agent-card status-online">
    <div class="agent-header">
        <div class="agent-avatar">M</div>
        <div class="agent-info">
            <h3>Max</h3>
            <span class="agent-role">Research Writer</span>
        </div>
        <span class="status-badge online">Online</span>
    </div>
</div>
```

### Chat Interface
```html
<div class="chat-container">
    <div class="chat-messages" id="chatMessages"></div>
    <div class="chat-input">
        <textarea id="chatInput" placeholder="Type message..."></textarea>
        <button onclick="sendMessage()">Send</button>
    </div>
</div>
```

## MyStyle1 for Web Apps

### CSS Variables
```css
:root {
    --color-dark: #0f172a;
    --color-white: #ffffff;
    --color-orange: #f97316;
    --color-bg: #f8fafc;
    --color-muted: #64748b;
    --font-family: 'Inter', sans-serif;
}
```

### Typography Scale
| Element | Size | Weight |
|---------|------|--------|
| Page Title | 20-24px | 800 (ExtraBold) |
| Section Heading | 18-20px | 700 (Bold) |
| Card Title | 16px | 600 (SemiBold) |
| Body Text | 14-16px | 400 (Regular) |

## System Statistics

### Resource Monitoring
```php
// Memory usage
$mem = parse_ini_file('/proc/meminfo', true);
$total = $mem['MemTotal'][0] / 1024 / 1024; // GB

// CPU load
$load = explode(' ', file_get_contents('/proc/loadavg'));

// Disk usage
$totalDisk = disk_total_space('/');
$freeDisk = disk_free_space('/');
```

### Git Activity
```php
exec("cd /opt/data/hermes && git log --oneline -10", $output);
```

## Deployment

### Shared Hosting (cPanel)
1. Upload folder to `public_html/`
2. Set permissions:
```bash
chmod 755 dashboard/
chmod 600 data/users.json
```
3. Access: `https://yourdomain.com/dashboard/`

### VPS
```bash
bash scripts/setup.sh
```

## Pitfalls

- **Password Hash**: Must use valid bcrypt hash. Test with `password_verify()` before shipping.
- **Session Security**: Always call `session_regenerate_id(true)` on login.
- **Hermes API URL**: Default is `localhost:9119`. Change if deploying remotely.
- **File Permissions**: `data/users.json` must be 600 (owner read/write only).
- **Demo Mode**: Always include fallback when Hermes gateway is offline.

## Related Skills

- `web-slide-decks` - For HTML presentation decks
- `github-push-workflow` - For committing dashboard code
- `prd-generator` - For documenting dashboard features

## Example Project

See `/opt/data/hermes/elon/hermes-dashboard/` for a complete working example.
