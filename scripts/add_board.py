#!/usr/bin/env python3
"""
Tambah Board Kanban untuk Workflow Artikel
"""
import sqlite3
from datetime import datetime

KANBAN_DB = "/opt/data/home/.hermes/kanban.db"

conn = sqlite3.connect(KANBAN_DB)
c = conn.cursor()

# Create new board
c.execute(
    "INSERT INTO boards (name, description) VALUES (?, ?)",
    ("Artikel-Workflow", "Workflow pembuatan artikel non-fiksi dengan ilustrasi")
)
board_id = c.lastrowid

# Add tasks
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

print(f"✅ Board 'Artikel-Workflow' created with ID: {board_id}")
print(f"✅ 4 tasks added")
