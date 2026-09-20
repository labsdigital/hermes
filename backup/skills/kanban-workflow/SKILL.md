---
name: kanban-workflow
description: "Kanban boards with SQLite, CLI, and GitHub Pages dashboard."
version: 1.0.0
author: Hermes Agent + labsdigital
license: MIT
tags: [kanban, workflow, sqlite, dashboard]
---

# Kanban Workflow Management

Sistem Kanban untuk mengelola workflow multi-agen Hermes.

## Quick Start

```bash
# Setup database
python3 /opt/data/hermes/scripts/kanban_setup.py

# Add board
python3 /opt/data/hermes/scripts/setup_board.py

# View
python3 /opt/data/hermes/scripts/kanban_cli.py list
python3 /opt/data/hermes/scripts/kanban_cli.py show <id>

# Update dashboard
python3 /opt/data/hermes/scripts/update_dashboard.py
```

## Dashboard URL
https://labsdigital.github.io/hermes/kanban-dashboard/

## CLI Commands
- `list` - List boards
- `show <id>` - Show board tasks
- `create --title "..." --board <id>` - Create task
- `complete <id>` - Mark done
- `block <id> --reason "..."` - Block task
- `stats` - Show statistics

## Files Created
- `/opt/data/hermes/scripts/kanban_setup.py`
- `/opt/data/hermes/scripts/kanban_cli.py`
- `/opt/data/hermes/scripts/setup_board.py`
- `/opt/data/hermes/scripts/update_dashboard.py`
- `/opt/data/hermes/kanban-dashboard/`

## Pitfalls
- **SQLite path:** Kanban DB is at `/opt/data/home/.hermes/kanban.db` — must set `HERMES_HOME=/opt/data/home` or use absolute paths
- **Task creation:** `kanban_cli.py create` uses `--desc` not `--description` for task descriptions
- **Board setup:** Use `setup_board.py` to add initial tasks with proper structure

## References
- `references/pitfalls.md` - Common pitfalls and fixes
