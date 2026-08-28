#!/usr/bin/env python3
"""
Update Kanban data and push to GitHub for real-time dashboard
"""
import subprocess
import json
import sqlite3
from datetime import datetime
import os

KANBAN_DB = "/opt/data/home/.hermes/kanban.db"
DASHBOARD_DIR = "/opt/data/hermes/kanban"
DATA_FILE = os.path.join(DASHBOARD_DIR, "kanban-data.json")

def export_data():
    """Export kanban data to JSON"""
    conn = sqlite3.connect(KANBAN_DB)
    c = conn.cursor()
    
    c.execute('SELECT id, name, description FROM boards ORDER BY id')
    boards = c.fetchall()
    
    result = {
        'last_updated': datetime.now().isoformat(),
        'boards': []
    }
    
    for bid, bname, bdesc in boards:
        c.execute('''
            SELECT id, title, description, status, priority, assignee, blocked_reason
            FROM tasks WHERE board_id = ?
            ORDER BY 
                CASE status WHEN 'todo' THEN 1 WHEN 'in-progress' THEN 2 WHEN 'blocked' THEN 3 WHEN 'done' THEN 4 END,
                CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 WHEN 'low' THEN 3 END
        ''', (bid,))
        
        tasks = []
        for tid, title, desc, status, priority, assignee, blocked in c.fetchall():
            tasks.append({
                'id': tid,
                'title': title,
                'description': desc or '',
                'status': status,
                'priority': priority,
                'assignee': assignee or 'unassigned',
                'blocked_reason': blocked or ''
            })
        
        result['boards'].append({
            'id': bid,
            'name': bname,
            'description': bdesc or '',
            'tasks': tasks
        })
    
    conn.close()
    
    with open(DATA_FILE, 'w') as f:
        json.dump(result, f, indent=2)
    
    return result

def commit_and_push():
    """Commit and push to GitHub"""
    os.chdir('/opt/data/hermes')
    
    # Add files
    subprocess.run(['git', 'add', 'kanban-dashboard/'], check=True)
    
    # Commit
    result = subprocess.run(
        ['git', 'commit', '-m', 'Dashboard: Update kanban data'],
        capture_output=True, text=True
    )
    
    if result.returncode == 0:
        # Push
        push_result = subprocess.run(
            ['git', 'push', 'origin', 'main'],
            capture_output=True, text=True
        )
        if push_result.returncode == 0:
            return True, "Pushed to GitHub"
        else:
            return False, push_result.stderr
    else:
        return False, result.stderr

def main():
    print("📊 Exporting Kanban data...")
    data = export_data()
    
    print(f"✓ Boards: {len(data['boards'])}")
    print(f"✓ Total tasks: {sum(len(b['tasks']) for b in data['boards'])}")
    print(f"✓ Data saved to: {DATA_FILE}")
    
    print("\n🐙 Committing to GitHub...")
    success, message = commit_and_push()
    
    if success:
        print(f"✓ {message}")
        print(f"\n🌐 Dashboard URL: https://labsdigital.github.io/hermes/kanban-dashboard/")
    else:
        print(f"✗ Error: {message}")

if __name__ == '__main__':
    main()
