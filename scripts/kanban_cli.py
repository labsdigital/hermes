#!/usr/bin/env python3
"""
Kanban CLI untuk Hermes Agent
Command-line interface untuk Kanban system
"""

import sqlite3
import argparse
import sys
from datetime import datetime
from pathlib import Path

# Paths
HERMES_HOME = Path("/opt/data/home/.hermes")
KANBAN_DB = HERMES_HOME / "kanban.db"

# Colors
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'

def get_connection():
    """Get database connection"""
    if not KANBAN_DB.exists():
        print(f"{Colors.RED}ERROR: Database not found. Run setup first.{Colors.NC}", file=sys.stderr)
        sys.exit(1)
    return sqlite3.connect(KANBAN_DB)

def cmd_list():
    """List all boards"""
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT id, name, description, created_at FROM boards ORDER BY id')
    boards = c.fetchall()
    conn.close()
    
    if not boards:
        print("No boards found.")
        return
    
    print(f"\n{Colors.BLUE}📋 KANBAN BOARDS{Colors.NC}")
    print("="*50)
    for bid, name, desc, created in boards:
        print(f"{Colors.GREEN}[{bid}]{Colors.NC} {name}")
        if desc:
            print(f"    {desc}")
        print(f"    Created: {created}")
        print()

def cmd_show(board_id):
    """Show board with tasks"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('SELECT id, name, description FROM boards WHERE id = ?', (board_id,))
    board = c.fetchone()
    if not board:
        print(f"Board {board_id} not found")
        conn.close()
        return
    
    print(f"\n{Colors.BLUE}📁 {board[1]}{Colors.NC}")
    print("="*60)
    if board[2]:
        print(f"{board[2]}")
        print()
    
    c.execute('''
        SELECT id, title, description, status, priority, assignee, blocked_reason, created_at
        FROM tasks 
        WHERE board_id = ?
        ORDER BY 
            CASE status 
                WHEN 'todo' THEN 1 
                WHEN 'in-progress' THEN 2 
                WHEN 'blocked' THEN 3 
                WHEN 'done' THEN 4 
            END,
            CASE priority 
                WHEN 'high' THEN 1 
                WHEN 'medium' THEN 2 
                WHEN 'low' THEN 3 
            END
    ''', (board_id,))
    
    tasks = c.fetchall()
    conn.close()
    
    if not tasks:
        print('No tasks in this board.')
        return
    
    current_status = None
    current_priority = None
    status_labels = {
        'todo': '⏳ TODO',
        'in-progress': '🔄 IN PROGRESS',
        'blocked': '🚫 BLOCKED',
        'done': '✅ DONE'
    }
    priority_labels = {
        'high': '🔴 HIGH',
        'medium': '🟡 MEDIUM',
        'low': '🟢 LOW'
    }
    
    for tid, title, desc, status, priority, assignee, blocked, created in tasks:
        if status != current_status:
            current_status = status
            current_priority = None
            print(f"\n{status_labels.get(status, status)}")
            print("-"*60)
        
        if priority != current_priority:
            current_priority = priority
            print(f"\n  {priority_labels.get(priority, priority)} Priority:")
        
        a_str = f"@{assignee}" if assignee else "Unassigned"
        title_display = title[:55] if title else ""
        
        print(f"  [{tid}] {title_display}")
        if desc:
            print(f"      {desc[:70]}")
        print(f"      Assignee: {a_str}")
        if blocked:
            print(f"      Blocked: {blocked}")
        print()

def cmd_create(args):
    """Create new task"""
    conn = get_connection()
    c = conn.cursor()
    
    # Check board exists
    c.execute('SELECT id FROM boards WHERE id = ?', (args.board,))
    if not c.fetchone():
        print(f"Board {args.board} not found")
        conn.close()
        return
    
    c.execute('''
        INSERT INTO tasks (board_id, title, description, priority, assignee)
        VALUES (?, ?, ?, ?, ?)
    ''', (args.board, args.title, args.desc or '', args.priority, args.assignee))
    
    task_id = c.lastrowid
    conn.commit()
    conn.close()
    print(f"Created task [{task_id}]: {args.title}")

def cmd_complete(task_id):
    """Mark task as done"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('UPDATE tasks SET status = ?, completed_at = ? WHERE id = ?', 
              ('done', datetime.now(), task_id))
    
    if c.rowcount == 0:
        print(f"Task {task_id} not found")
        conn.close()
        return
    
    conn.commit()
    conn.close()
    print(f"Task {task_id} marked as done")

def cmd_block(args):
    """Block task"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('UPDATE tasks SET status = ?, blocked_reason = ? WHERE id = ?', 
              ('blocked', args.reason, args.task_id))
    
    if c.rowcount == 0:
        print(f"Task {args.task_id} not found")
        conn.close()
        return
    
    conn.commit()
    conn.close()
    print(f"Task {args.task_id} blocked: {args.reason}")

def cmd_unblock(task_id):
    """Unblock task"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('UPDATE tasks SET status = ?, blocked_reason = NULL WHERE id = ?', 
              ('todo', task_id))
    
    if c.rowcount == 0:
        print(f"Task {task_id} not found")
        conn.close()
        return
    
    conn.commit()
    conn.close()
    print(f"Task {task_id} unblocked")

def cmd_comment(args):
    """Add comment to task"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('INSERT INTO comments (task_id, author, content) VALUES (?, ?, ?)',
              (args.task_id, args.author, args.text))
    
    comment_id = c.lastrowid
    conn.commit()
    conn.close()
    print(f"Comment added to task {args.task_id}")

def cmd_stats():
    """Show statistics"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('SELECT COUNT(*) FROM boards')
    boards = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM tasks')
    total_tasks = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM tasks WHERE status = 'todo'")
    todo = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM tasks WHERE status = 'in-progress'")
    in_progress = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM tasks WHERE status = 'blocked'")
    blocked = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM tasks WHERE status = 'done'")
    done = c.fetchone()[0]
    
    conn.close()
    
    print(f"\n{Colors.BLUE}📊 KANBAN STATISTICS{Colors.NC}")
    print("="*40)
    print(f"Boards:      {boards}")
    print(f"Total Tasks: {total_tasks}")
    print()
    print(f"TODO:        {todo}")
    print(f"In Progress: {in_progress}")
    print(f"Blocked:     {blocked}")
    print(f"Done:        {done}")

def main():
    parser = argparse.ArgumentParser(description='Hermes Kanban CLI')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # List
    subparsers.add_parser('list', help='List all boards')
    
    # Show
    show_parser = subparsers.add_parser('show', help='Show board with tasks')
    show_parser.add_argument('board_id', type=int, help='Board ID')
    
    # Create
    create_parser = subparsers.add_parser('create', help='Create new task')
    create_parser.add_argument('--title', '-t', required=True, help='Task title')
    create_parser.add_argument('--board', '-b', type=int, required=True, help='Board ID')
    create_parser.add_argument('--desc', '-d', help='Description')
    create_parser.add_argument('--priority', '-p', default='medium', choices=['high', 'medium', 'low'])
    create_parser.add_argument('--assignee', '-a', help='Assignee profile name')
    
    # Complete
    complete_parser = subparsers.add_parser('complete', help='Mark task as done')
    complete_parser.add_argument('task_id', type=int, help='Task ID')
    
    # Block
    block_parser = subparsers.add_parser('block', help='Block task')
    block_parser.add_argument('task_id', type=int, help='Task ID')
    block_parser.add_argument('--reason', '-r', required=True, help='Block reason')
    
    # Unblock
    unblock_parser = subparsers.add_parser('unblock', help='Unblock task')
    unblock_parser.add_argument('task_id', type=int, help='Task ID')
    
    # Comment
    comment_parser = subparsers.add_parser('comment', help='Add comment')
    comment_parser.add_argument('task_id', type=int, help='Task ID')
    comment_parser.add_argument('--author', '-a', default='anonymous')
    comment_parser.add_argument('--text', '-t', required=True, help='Comment text')
    
    # Stats
    subparsers.add_parser('stats', help='Show statistics')
    
    args = parser.parse_args()
    
    if args.command == 'list':
        cmd_list()
    elif args.command == 'show':
        cmd_show(args.board_id)
    elif args.command == 'create':
        cmd_create(args)
    elif args.command == 'complete':
        cmd_complete(args.task_id)
    elif args.command == 'block':
        cmd_block(args)
    elif args.command == 'unblock':
        cmd_unblock(args.task_id)
    elif args.command == 'comment':
        cmd_comment(args)
    elif args.command == 'stats':
        cmd_stats()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
