# Hermes Dashboard

Web-based dashboard untuk mengelola Hermes Multi-Agent System.

## 🚀 Fitur

- **Multi-user Authentication** - File-based (tanpa database)
- **Agent Monitoring** - Real-time status semua agent
- **Chat Interface** - Interaksi dengan agent via web
- **Task Management** - Spawn, monitor, kill tasks
- **System Statistics** - Uptime, memory, CPU, disk usage
- **Activity Feed** - Recent git commits
- **Modern UI** - MyStyle1 design system (Inter font, orange accent)

## 📁 Struktur File

```
hermes-dashboard/
├── index.php              # Main dashboard
├── login.php              # Authentication page
├── logout.php             # Logout handler
├── chat.php               # Chat interface
├── api/
│   ├── agents.php         # Agent status API
│   ├── activity.php       # Git activity API
│   ├── chat.php           # Chat API
│   ├── stats.php          # System stats API
│   └── tasks.php          # Task management API
├── assets/
│   ├── css/
│   │   └── styles.css     # Main stylesheet
│   └── js/
│       └── app.js         # Main JavaScript
├── includes/
│   ├── header.php         # Page header
│   └── footer.php         # Page footer
├── data/
│   ├── users.json         # User credentials
│   ├── agents.json        # Agent configurations
│   ├── tasks.json         # Active tasks
│   └── logs/              # Activity logs
└── scripts/
    └── init.sh            # Initialization script
```

## 🔧 Installation

### 1. Upload Files

Upload semua file ke shared hosting Anda (public_html/hermes-dashboard/).

### 2. Set Permissions

```bash
chmod 755 /hermes-dashboard/
chmod 755 /hermes-dashboard/api/
chmod 755 /hermes-dashboard/data/
chmod 600 /hermes-dashboard/data/users.json
chmod 755 /hermes-dashboard/data/logs/
```

### 3. Initialize Data

```bash
php -r '
$hash = password_hash("hermes2024", PASSWORD_BCRYPT);
echo "Default password hash: " . $hash . "\n";
'
```

Edit `data/users.json` dengan hash password yang dihasilkan.

### 4. Access Dashboard

Buka browser dan akses:
```
https://yourdomain.com/hermes-dashboard/
```

**Default Login:**
- Username: `tamim`
- Password: `hermes2024`

## 🔌 Hermes API Integration

Dashboard ini dirancang untuk berintegrasi dengan Hermes Gateway yang berjalan di port 9119.

### Current Setup

```
Hermes Gateway: http://localhost:9119
Dashboard:      http://yourdomain.com/hermes-dashboard/
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/agents` | GET | Get agent list |
| `/api/v1/chat` | POST | Send message to agent |
| `/api/v1/tasks` | GET/POST | Manage tasks |

## 🛡️ Security

- ✅ Password hashing dengan bcrypt
- ✅ Session management
- ✅ CSRF protection (coming soon)
- ✅ Input sanitization
- ✅ Rate limiting on login (coming soon)

## 🎨 Design System

Menggunakan **MyStyle1**:
- Font: Inter (Google Fonts)
- Colors: #0f172a (dark), #ffffff (white), #f97316 (orange)
- Modern, clean, professional UI

## 📝 TODO

- [ ] Implement CSRF protection
- [ ] Add rate limiting
- [ ] Real-time WebSocket updates
- [ ] File manager
- [ ] Export reports (PDF/CSV)
- [ ] Dark mode toggle
- [ ] Mobile app integration

## 📄 License

MIT License - See LICENSE file for details.

## 🔗 Links

- GitHub: https://github.com/labsdigital/hermes
- PRD: /elon/hermes-dashboard/PRD.md
