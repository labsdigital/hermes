#!/usr/bin/env python3
"""
Export Kanban data to JSON for web dashboard
"""
import json
import sqlite3
from datetime import datetime

KANBAN_DB = "/opt/data/home/.hermes/kanban.db"
OUTPUT_FILE = "/opt/data/hermes/kanban-dashboard/kanban-data.json"

conn = sqlite3.connect(KANBAN_DB)
c = conn.cursor()

# Get all data
c.execute('SELECT id, name, description FROM boards ORDER BY id')
boards = c.fetchall()

result = {
    'last_updated': datetime.now().isoformat(),
    'boards': []
}

for bid, bname, bdesc in boards:
    c.execute('''
        SELECT id, title, description, status, priority, assignee, blocked_reason, created_at
        FROM tasks WHERE board_id = ?
        ORDER BY 
            CASE status WHEN 'todo' THEN 1 WHEN 'in-progress' THEN 2 WHEN 'blocked' THEN 3 WHEN 'done' THEN 4 END,
            CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 WHEN 'low' THEN 3 END
    ''', (bid,))
    tasks = []
    for tid, title, desc, status, priority, assignee, blocked, created in c.fetchall():
        tasks.append({
            'id': tid,
            'title': title,
            'description': desc or '',
            'status': status,
            'priority': priority,
            'assignee': assignee or 'unassigned',
            'blocked_reason': blocked or '',
            'created_at': created
        })
    
    result['boards'].append({
        'id': bid,
        'name': bname,
        'description': bdesc or '',
        'tasks': tasks
    })

conn.close()

# Save to file
import os
os.makedirs('/opt/data/hermes/kanban-dashboard', exist_ok=True)
with open(OUTPUT_FILE, 'w') as f:
    json.dump(result, f, indent=2)

print(f"✓ Exported to {OUTPUT_FILE}")
print(f"  Boards: {len(result['boards'])}")
print(f"  Total tasks: {sum(len(b['tasks']) for b in result['boards'])}")
