#!/usr/bin/env python3
"""
Export Kanban database to JSON for dashboard
"""
import json
import sqlite3
import os
from datetime import datetime

DB_PATH = '/opt/data/home/.hermes/kanban.db'
OUTPUT_PATH = '/opt/data/hermes/kanban/kanban-data.json'

def export_kanban():
    """Export all boards and tasks to JSON"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # Get all boards
    c.execute('SELECT * FROM boards WHERE status = "active" ORDER BY id')
    boards = []
    
    for board_row in c.fetchall():
        board = {
            'id': board_row['id'],
            'name': board_row['name'],
            'description': board_row['description'] or '',
            'tasks': []
        }
        
        # Get tasks for this board
        c.execute('SELECT * FROM tasks WHERE board_id = ? ORDER BY priority, id', 
                  (board_row['id'],))
        
        for task_row in c.fetchall():
            task = {
                'id': task_row['id'],
                'title': task_row['title'],
                'description': task_row['description'] or '',
                'status': task_row['status'],
                'priority': task_row['priority'],
                'assignee': task_row['assignee'] or 'unassigned',
                'blocked_reason': task_row['blocked_reason'] or '',
                'created_at': task_row['created_at']
            }
            board['tasks'].append(task)
        
        boards.append(board)
    
    conn.close()
    
    # Create output
    output = {
        'last_updated': datetime.now().isoformat(),
        'boards': boards
    }
    
    # Write JSON
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"✓ Exported {len(boards)} boards to {OUTPUT_PATH}")
    for b in boards:
        print(f"  - {b['id']}: {b['name']} ({len(b['tasks'])} tasks)")

if __name__ == '__main__':
    export_kanban()
