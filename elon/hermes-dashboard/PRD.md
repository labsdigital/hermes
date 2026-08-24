# PRD: Hermes Agent Dashboard

**Document Version:** 1.0.0  
**Status:** ✅ Approved  
**Last Updated:** 2026-08-24  
**Author:** @elon (Web Development Specialist)  
**Project:** Hermes Multi-Agent System — Web Dashboard

---

## 1. Executive Summary

### 1.1 Product Overview
Hermes Agent Dashboard adalah aplikasi web berbasis PHP + HTML yang berfungsi sebagai pusat kontrol untuk mengelola dan berinteraksi dengan Hermes multi-agent system yang di-hosting di VPS. Aplikasi ini dirancang untuk diakses melalui shared hosting dengan autentikasi sederhana berbasis file (tanpa database).

### 1.2 Objectives
- ✅ Menyediakan dashboard monitoring untuk semua agent Hermes
- ✅ Memudahkan interaksi chat dengan agent via web interface
- ✅ Mengelola task/agent (spawn, monitor, kill)
- ✅ Menampilkan statistik sistem (uptime, memory, request)
- ✅ Autentikasi multi-user tanpa role management
- ✅ Tampilan modern profesional (MyStyle1 design system)

### 1.3 Target Users
| User Type | Description | Use Case |
|-----------|-------------|----------|
| **Admin** | Master Tamim (owner) | Full access ke semua fitur |
| **User** | Tim/staf | Akses monitoring dan chat agent |

---

## 2. Design System — MyStyle1

### 2.1 Color Palette
```css
/* Primary Colors */
--color-primary-dark: #0f172a;  /* Slate 900 — Text utama, judul */
--color-primary-white: #ffffff;  /* White — Background cards */
--color-accent-orange: #f97316;  /* Orange 500 — Highlights, buttons */
--color-background-light: #f8fafc;  /* Slate 50 — Page background */

/* Secondary Colors */
--color-text-muted: #64748b;  /* Slate 500 — Subtitle, caption */
--color-border-soft: #e2e8f0;  /* Slate 200 — Borders, dividers */
--color-success: #10b981;     /* Green — Online status */
--color-warning: #f59e0b;     /* Yellow — Warning */
--color-danger: #ef4444;      /* Red — Error/offline */
```

### 2.2 Typography Scale (Inter Font)
| Element | Size Range | Weight | Usage |
|---------|------------|--------|-------|
| **App Title** | 32-40px | 800 (ExtraBold) | Dashboard header |
| **Section Heading** | 24-32px | 700 (Bold) | Card titles |
| **Subheading** | 18-24px | 600 (SemiBold) | Labels |
| **Body Text** | 14-16px | 400 (Regular) | Content |
| **Caption** | 12-14px | 500 (Medium) | Metadata |

### 2.3 Design Principles
- **Clean & Professional:** Apple/Google design language
- **Card-Based Layout:** White cards dengan subtle shadow
- **Responsive:** Mobile-first approach
- **Minimalist:** Kurangi elemen dekoratif
- **Accessible:** Kontras tinggi, font mudah dibaca

---

## 3. Technical Specifications

### 3.1 Tech Stack
```
Backend:
├── PHP 7.4+ (shared hosting compatible)
├── File-based authentication (JSON/text)
└── No database dependency

Frontend:
├── HTML5 (Semantic)
├── CSS3 (Modern, CSS Variables)
├── Vanilla JavaScript (ES6+)
├── Google Fonts: Inter
└── Inline SVG icons

Deployment:
├── Shared hosting (cPanel/LiteSpeed)
├── No server requirements (PHP native)
└── Static file deployment
```

### 3.2 File Structure
```
/hermes-dashboard/
├── index.php                 # Main entry (redirect to login/dashboard)
├── login.php                 # Authentication page
├── logout.php                # Session termination
├── dashboard.php             # Main dashboard
├── chat.php                  # Chat interface
├── agents.php                # Agent management
├── assets/
│   ├── css/
│   │   └── styles.css        # Main stylesheet
│   └── js/
│       └── app.js            # Main JavaScript
├── data/
│   ├── users.json            # User credentials (encrypted passwords)
│   ├── agents.json           # Agent configurations
│   ├── sessions.json         # Active sessions
│   └── logs/                 # Activity logs
├── api/
│   ├── auth.php              # Authentication API
│   ├── agents.php            # Agent management API
│   ├── chat.php              # Chat API
│   └── stats.php             # Statistics API
└── README.md                 # Installation guide
```

### 3.3 Browser Compatibility
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Mobile Safari/Chrome

---

## 4. Authentication System

### 4.1 User Storage (users.json)
```json
{
  "users": [
    {
      "id": "user_001",
      "username": "tamim",
      "name": "Master Tamim",
      "password_hash": "$2y$10$...",
      "created_at": "2026-08-24",
      "last_login": "2026-08-24T10:30:00Z"
    },
    {
      "id": "user_002",
      "username": "admin",
      "name": "Admin",
      "password_hash": "$2y$10$...",
      "created_at": "2026-08-24",
      "last_login": "2026-08-24T09:15:00Z"
    }
  ]
}
```

### 4.2 Authentication Flow
1. User enters username + password
2. System validates against users.json
3. Password verified with `password_verify()`
4. Session created (PHP session)
5. Redirect to dashboard

### 4.3 Security Features
- ✅ Password hashing (bcrypt)
- ✅ Session management
- ✅ CSRF protection
- ✅ Rate limiting (5 attempts per login)
- ✅ Auto logout after 30 minutes inactivity
- ✅ Input sanitization

---

## 5. Dashboard Features

### 5.1 Agent List & Status
**Display:**
- Agent name (zetta, max, elon, chalbi, taraka)
- Status indicator (Online/Offline/Idle)
- Last activity timestamp
- Quick action buttons (Chat, Log)

**Visual:**
```
┌─────────────────────────────────────────┐
│  🤖 AGENT STATUS                        │
├─────────────────────────────────────────┤
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐│
│  │ ZETTA│  │ MAX  │  │ ELON │  │CHALBI││
│  │ ●ON  │  │ ●ON  │  │ ○OFF │  │ ●IDLE││
│  └──────┘  └──────┘  └──────┘  └──────┘│
│  ┌──────┐                                │
│  │ TARAKA│                               │
│  │ ●ON  │                                │
│  └──────┘                                │
└─────────────────────────────────────────┘
```

### 5.2 Task/Agent Management
**Features:**
- Spawn new agent task
- View active tasks
- Kill/cancel running task
- View task logs
- Task history (last 24h)

**Actions:**
| Action | Button | Function |
|--------|--------|----------|
| Spawn | `+ New Task` | Create new agent task |
| View Log | `📄 Log` | Open task log file |
| Kill | `⏹ Stop` | Terminate running task |
| Refresh | `🔄` | Reload task list |

### 5.3 Statistics Panel
**Metrics Displayed:**
| Metric | Source | Update |
|--------|--------|--------|
| **Uptime** | System uptime command | Every 5 min |
| **Memory Usage** | /proc/meminfo | Every 5 min |
| **CPU Load** | /proc/loadavg | Every 5 min |
| **Active Agents** | agents.json | Real-time |
| **Total Requests** | Counter file | Real-time |
| **Disk Usage** | df command | Hourly |

**Visualization:**
- Progress bars for resource usage
- Trend indicators (↑↓→)
- Color-coded status (green <70%, yellow 70-90%, red >90%)

### 5.4 Recent Activity Feed
**Shows:**
- Last 10 agent interactions
- Login/logout events
- Task spawn/complete events
- Error/warning notifications

---

## 6. Chat Feature

### 6.1 Chat Interface
**Layout:**
```
┌─────────────────────────────────────────┐
│  💬 CHAT WITH [AGENT NAME]       [🔌]   │
├─────────────────────────────────────────┤
│                                         │
│  User: Halo, apa kabar?                 │
│                                         │
│  Agent: Baik! Ada yang bisa dibantu?    │
│                                         │
│  User: Tolong cek status max           │
│                                         │
├─────────────────────────────────────────┤
│  [Type message...]              [Send ➤]│
└─────────────────────────────────────────┘
```

### 6.2 Chat Features
- ✅ Select agent from dropdown
- ✅ Message history (last 50 messages)
- ✅ Auto-scroll to latest message
- ✅ Timestamp display
- ✅ Typing indicator
- ✅ Send with Enter key
- ✅ Clear conversation button

### 6.3 Chat API
**Endpoint:** `POST /api/chat.php`

**Request:**
```json
{
  "agent": "max",
  "message": "Cek status article terbaru",
  "session_id": "abc123"
}
```

**Response:**
```json
{
  "success": true,
  "reply": "Article terbaru: membesarkan-ai-2026-08-23.md",
  "timestamp": "2026-08-24T10:30:00Z"
}
```

### 6.4 Message Handling
1. User types message + selects agent
2. Click Send or press Enter
3. AJAX POST to chat API
4. Server processes via Hermes CLI
5. Response displayed in chat bubble
6. History saved to chat_logs.json

---

## 7. Agent Management

### 7.1 Agent Configuration (agents.json)
```json
{
  "agents": [
    {
      "id": "zetta",
      "name": "Zetta",
      "role": "Main Agent",
      "model": "agnes-2.5-flash",
      "status": "online",
      "last_seen": "2026-08-24T10:30:00Z",
      "tasks": 12,
      "articles": 14
    },
    {
      "id": "max",
      "name": "Max",
      "role": "Research Writer",
      "model": "stealth/ox-alpha",
      "status": "online",
      "last_seen": "2026-08-24T10:28:00Z",
      "tasks": 8,
      "articles": 14
    },
    {
      "id": "elon",
      "name": "Elon",
      "role": "Web Developer",
      "model": "stealth/ox-alpha",
      "status": "idle",
      "last_seen": "2026-08-24T10:25:00Z",
      "tasks": 6,
      "presentations": 5
    },
    {
      "id": "chalbi",
      "name": "Chalbi",
      "role": "Rumi Researcher",
      "model": "stealth/ox-alpha",
      "status": "online",
      "last_seen": "2026-08-24T10:20:00Z",
      "tasks": 4,
      "articles": 7
    },
    {
      "id": "taraka",
      "name": "Taraka",
      "role": "Foundation Writer",
      "model": "stealth/ox-alpha",
      "status": "offline",
      "last_seen": "2026-08-24T08:00:00Z",
      "tasks": 2,
      "proposals": 2
    }
  ]
}
```

### 7.2 Agent Actions
| Action | Description | API Endpoint |
|--------|-------------|--------------|
| **View Status** | Check online/offline | GET /api/agents.php |
| **Send Message** | Chat with agent | POST /api/chat.php |
| **View Logs** | Task execution logs | GET /api/logs.php |
| **Spawn Task** | Start new task | POST /api/agents.php |
| **Kill Task** | Stop running task | DELETE /api/agents.php |

---

## 8. UI/UX Components

### 8.1 Layout Structure
```
┌─────────────────────────────────────────────────────┐
│  🏠 Hermes Dashboard                    👤 User ▼   │
├──────────┬──────────────────────────────────────────┤
│          │                                          │
│ 📊 Dashboard│  Welcome back, Master Tamim!          │
│ 💬 Chat   │  ┌─────────┐ ┌─────────┐ ┌─────────┐  │
│ 🤖 Agents │  │ Agents  │ │ Tasks   │ │ Stats   │  │
│ ⚙️ Settings│  │ 5 Online│ │ 3 Active│ │ CPU 45% │  │
│          │  └─────────┘ └─────────┘ └─────────┘  │
│          │                                          │
│          │  ┌─────────────────────────────────┐   │
│          │  │  Recent Activity                 │   │
│          │  │  • Max: Article committed        │   │
│          │  │  • Elon: Presentation v5 done    │   │
│          │  │  • Chalbi: New article synced    │   │
│          │  └─────────────────────────────────┘   │
├──────────┴──────────────────────────────────────────┤
│  © 2026 Hermes Agent System | v1.0.0               │
└─────────────────────────────────────────────────────┘
```

### 8.2 Navigation
- **Sidebar:** Collapsible on mobile
- **Active state:** Orange left border
- **Icons:** Inline SVG
- **Labels:** Text below icon

### 8.3 Cards
- **Style:** White background, rounded corners (12px)
- **Shadow:** `0 4px 6px -1px rgba(0,0,0,0.1)`
- **Padding:** 24px
- **Hover:** Slight lift effect

### 8.4 Buttons
| Type | Style | Use Case |
|------|-------|----------|
| **Primary** | Orange fill, white text | Main actions |
| **Secondary** | Border only, orange text | Secondary actions |
| **Danger** | Red fill, white text | Delete/kill actions |
| **Success** | Green fill, white text | Confirm/spawn actions |

---

## 9. API Endpoints

### 9.1 Authentication
```
POST /api/auth.php
  Body: { username, password }
  Response: { token, user }

GET /api/auth.php/session
  Header: Authorization: Bearer <token>
  Response: { valid, user }

POST /api/auth.php/logout
  Response: { success }
```

### 9.2 Agents
```
GET /api/agents.php
  Response: { agents[] }

POST /api/agents.php
  Body: { agent_id, task }
  Response: { task_id, status }

DELETE /api/agents.php/:task_id
  Response: { success }
```

### 9.3 Chat
```
POST /api/chat.php
  Body: { agent, message, session_id }
  Response: { reply, timestamp }

GET /api/chat.php/history
  Query: ?agent=max&limit=50
  Response: { messages[] }
```

### 9.4 Statistics
```
GET /api/stats.php
  Response: {
    uptime: "14d 5h 32m",
    memory: { used: "2.1GB", total: "4GB", percent: 52 },
    cpu: { load: 0.45, percent: 45 },
    disk: { used: "12GB", total: "50GB", percent: 24 },
    requests: 1234,
    agents_online: 4
  }
```

---

## 10. Security Considerations

### 10.1 File Permissions
```bash
chmod 600 data/users.json
chmod 644 data/agents.json
chmod 755 api/
chmod 755 assets/
```

### 10.2 Protection Measures
- ✅ Password hashing (bcrypt)
- ✅ Session validation on every request
- ✅ CSRF token protection
- ✅ Input sanitization (htmlspecialchars)
- ✅ SQL injection prevention (not applicable, file-based)
- ✅ Rate limiting on login attempts
- ✅ Auto-logout on inactivity
- ✅ Secure file permissions

### 10.3 .htaccess Rules
```apache
# Deny access to data directory
<Directory "data">
    Require all denied
</Directory>

# Deny access to config files
<Files "*.json">
    Require all denied
</Files>

# Enable compression
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/css application/javascript
</IfModule>
```

---

## 11. Installation Guide

### 11.1 Prerequisites
- PHP 7.4+
- Shared hosting with PHP support
- cPanel or similar control panel
- SSH access (optional, for setup)

### 11.2 Upload Files
```bash
# Via FTP/cPanel File Manager
Upload all files to public_html/hermes-dashboard/
```

### 11.3 Set Permissions
```bash
chmod 755 /hermes-dashboard/
chmod 755 /hermes-dashboard/api/
chmod 600 /hermes-dashboard/data/users.json
chmod 755 /hermes-dashboard/data/logs/
```

### 11.4 Configure Users
Edit `data/users.json` and add users with hashed passwords:
```bash
# Generate password hash
php -r 'echo password_hash("yourpassword", PASSWORD_BCRYPT);'
```

### 11.5 Access Dashboard
```
https://yourdomain.com/hermes-dashboard/
```

---

## 12. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-08-24 | Initial release |
| | | - Authentication system |
| | | - Dashboard with agent status |
| | | - Chat interface |
| | | - Task management |
| | | - System statistics |

---

## 13. File Locations

### 13.1 Primary Files
```
Source: /opt/data/hermes/elon/hermes-dashboard/
Web Path: /public_html/hermes-dashboard/
GitHub: https://github.com/labsdigital/hermes/tree/main/elon/hermes-dashboard
```

### 13.2 Data Files
```
Users: data/users.json
Agents: data/agents.json
Sessions: data/sessions.json
Logs: data/logs/
Chat History: data/chat_logs.json
```

---

## 14. Future Enhancements

### 14.1 Planned Features
- [ ] Real-time WebSocket updates
- [ ] Agent-specific dashboards
- [ ] File manager for article viewing
- [ ] Email notifications
- [ ] Mobile app integration
- [ ] Dark mode toggle
- [ ] Export reports (PDF/CSV)
- [ ] Multi-language support

### 14.2 Potential Improvements
- [ ] Add agent task scheduling
- [ ] Implement WebSocket for live chat
- [ ] Add resource usage graphs (Chart.js)
- [ ] Create agent-specific endpoints
- [ ] Add audit log viewer
- [ ] Implement backup/restore functionality

---

## 15. Approval & Sign-off

| Role | Name | Date | Status |
|------|------|------|--------|
| **Product Owner** | Master Tamim | 2026-08-24 | ✅ Approved |
| **Tech Lead** | @zetta | 2026-08-24 | ✅ Approved |
| **Design Lead** | @elon | 2026-08-24 | ✅ Approved |

---

**Document End**
