#!/usr/bin/env python3
"""
Setup Tasks untuk Board Artikel-Workflow
"""
import sqlite3

KANBAN_DB = "/opt/data/home/.hermes/kanban.db"

conn = sqlite3.connect(KANBAN_DB)
c = conn.cursor()

# Get board ID
c.execute("SELECT id FROM boards WHERE name = ?", ("Artikel-Workflow",))
board = c.fetchone()
if not board:
    print("Board 'Artikel-Workflow' not found")
    conn.close()
    exit(1)

board_id = board[0]

# Clear existing tasks
c.execute("DELETE FROM tasks WHERE board_id = ?", (board_id,))

# Add tasks with descriptions
tasks = [
    (board_id, "@max: Cari list topik dan tren terkini tentang AI dan kehidupan sehari-hari", 
     "Riset topik untuk artikel berikutnya", "todo", "high", "max", None),
    (board_id, "@atlas: Pilih satu topik paling menarik dari list", 
     "Seleksi topik berdasarkan relevansi", "todo", "high", "atlas", None),
    (board_id, "@atlas: Tulis artikel non-fiksi + ilustrasi (SVG + PNG)", 
     "Penulisan dan pembuatan ilustrasi", "todo", "high", "atlas", None),
    (board_id, "@atlas: Publish ke GitHub, Email Blogger, dan FTP", 
     "Deployment ke semua platform", "todo", "medium", "atlas", None),
]

c.executemany(
    """INSERT INTO tasks 
       (board_id, title, description, status, priority, assignee, blocked_reason)
       VALUES (?, ?, ?, ?, ?, ?, ?)""",
    tasks
)

conn.commit()
conn.close()

print(f"✅ Board 'Artikel-Workflow' (ID: {board_id}) ready")
print(f"✅ 4 tasks added")
print(f"\n📋 Tasks:")
for i, (bid, title, desc, status, priority, assignee, blocked) in enumerate(tasks, 1):
    print(f"  {i}. [{priority.upper()}] {title[:50]}... -> @{assignee}")
