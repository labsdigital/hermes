#!/bin/bash
# Kanban CLI Wrapper untuk Hermes Agent
# Menyediakan command-line interface untuk Kanban system

set -e

# Paths
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
KANBAN_DB="$HERMES_HOME/kanban.db"
PYTHON="$(which python3)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
error_exit() {
    echo -e "${RED}ERROR: $1${NC}" >&2
    exit 1
}

info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

# Check database exists
check_db() {
    if [[ ! -f "$KANBAN_DB" ]]; then
        error_exit "Kanban database not found. Run setup first: python3 scripts/kanban_setup.py"
    fi
}

# Initialize database
cmd_init() {
    info "Initializing Kanban database..."
    $PYTHON /opt/data/hermes/scripts/kanban_setup.py
}

# List boards
cmd_list() {
    check_db
    info "Listing boards..."
    
    $PYTHON -c "
import sqlite3
conn = sqlite3.connect('$KANBAN_DB')
c = conn.cursor()
c.execute('SELECT id, name, description, created_at FROM boards ORDER BY id')
boards = c.fetchall()
conn.close()

if not boards:
    print('No boards found.')
    exit(0)

print('📋 KANBAN BOARDS')
print('='*50)
for bid, name, desc, created in boards:
    print(f'{GREEN}[{bid}]${NC} {name}')
    if desc:
        print(f'    {desc}')
    print(f'    Created: {created}')
    print()
"
}

# Show board with tasks
cmd_show() {
    check_db
    
    if [[ -z "$1" ]]; then
        error_exit "Usage: kanban.sh show <board_id>"
    fi
    
    local board_id="$1"
    
    $PYTHON -c "
import sqlite3
from datetime import datetime
conn = sqlite3.connect('$KANBAN_DB')
c = conn.cursor()

# Get board
c.execute('SELECT id, name, description FROM boards WHERE id = ?', (board_id,))
board = c.fetchone()
if not board:
    print(f'Board {board_id} not found')
    exit(1)

print(f'📁 {board[1]}')
print('='*60)
if board[2]:
    print(f'{board[2]}')
    print()

# Get tasks by status
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
    exit(0)

current_status = None
status_labels = {
    'todo': '⏳ TODO',
    'in-progress': '🔄 IN PROGRESS',
    'blocked': '🚫 BLOCKED',
    'done': '✅ DONE'
}

for tid, title, desc, status, priority, assignee, blocked, created in tasks:
    if status != current_status:
        current_status = status
        print(f'\n{status_labels.get(status, status)}')
        print('-'*60)
    
    priority_symbols = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}
    p_sym = priority_symbols.get(priority, '⚪')
    a_str = f'@{assignee}' if assignee else 'unassigned'
    
    print(f'  [{tid}] {p_sym} {title[:50]}')
    if desc:
        print(f'      {desc[:60]}')
    print(f'      Assignee: {a_str}')
    if blocked:
        print(f'      Blocked: {blocked}')
    print()
"
}

# Create task
cmd_create() {
    check_db
    
    local title=""
    local board_id=""
    local desc=""
    local priority="medium"
    local assignee=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --title|-t) title="$2"; shift 2;;
            --board|-b) board_id="$2"; shift 2;;
            --desc|-d) desc="$2"; shift 2;;
            --priority|-p) priority="$2"; shift 2;;
            --assignee|-a) assignee="$2"; shift 2;;
            *) echo "Unknown option: $1"; exit 1;;
        esac
    done
    
    [[ -z "$title" ]] && error_exit "Title is required (--title)"
    [[ -z "$board_id" ]] && error_exit "Board ID is required (--board)"
    
    $PYTHON -c "
import sqlite3
conn = sqlite3.connect('$KANBAN_DB')
c = conn.cursor()

# Check board exists
c.execute('SELECT id FROM boards WHERE id = ?', ($board_id,))
if not c.fetchone():
    print(f'Board {board_id} not found')
    conn.close()
    exit(1)

c.execute('''
    INSERT INTO tasks (board_id, title, description, priority, assignee)
    VALUES (?, ?, ?, ?, ?)
''', ($board_id, '$title', '$desc', '$priority', '$assignee'))

task_id = c.lastrowndi
conn.commit()
conn.close()
print(f'Created task [{task_id}]: $title')
"
}

# Complete task
cmd_complete() {
    check_db
    
    [[ -z "$1" ]] && error_exit "Usage: kanban.sh complete <task_id>"
    
    $PYTHON -c "
import sqlite3
from datetime import datetime
conn = sqlite3.connect('$KANBAN_DB')
c = conn.cursor()

c.execute('UPDATE tasks SET status = ?, completed_at = ? WHERE id = ?', 
          ('done', datetime.now(), $1))

if c.rowcount == 0:
    print(f'Task $1 not found')
    conn.close()
    exit(1)

conn.commit()
conn.close()
print(f'Task $1 marked as done')
"
}

# Block task
cmd_block() {
    check_db
    
    [[ -z "$1" ]] && error_exit "Usage: kanban.sh block <task_id> --reason '...'"
    
    local task_id="$1"
    shift
    local reason=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --reason|-r) reason="$2"; shift 2;;
            *) shift;;
        esac
    done
    
    [[ -z "$reason" ]] && error_exit "Reason is required (--reason)"
    
    $PYTHON -c "
import sqlite3
conn = sqlite3.connect('$KANBAN_DB')
c = conn.cursor()

c.execute('UPDATE tasks SET status = ?, blocked_reason = ? WHERE id = ?', 
          ('blocked', '$reason', $task_id))

if c.rowcount == 0:
    print(f'Task $task_id not found')
    conn.close()
    exit(1)

conn.commit()
conn.close()
print(f'Task $task_id blocked: $reason')
"
}

# Unblock task
cmd_unblock() {
    check_db
    
    [[ -z "$1" ]] && error_exit "Usage: kanban.sh unblock <task_id>"
    
    $PYTHON -c "
import sqlite3
conn = sqlite3.connect('$KANBAN_DB')
c = conn.cursor()

c.execute('UPDATE tasks SET status = ?, blocked_reason = NULL WHERE id = ?', 
          ('todo', $1))

if c.rowcount == 0:
    print(f'Task $1 not found')
    conn.close()
    exit(1)

conn.commit()
conn.close()
print(f'Task $1 unblocked')
"
}

# Add comment
cmd_comment() {
    check_db
    
    [[ -z "$1" ]] && error_exit "Usage: kanban.sh comment <task_id> --author 'Name' --text 'Comment'"
    
    local task_id="$1"
    shift
    local author="anonymous"
    local text=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --author|-a) author="$2"; shift 2;;
            --text|-t) text="$2"; shift 2;;
            *) shift;;
        esac
    done
    
    [[ -z "$text" ]] && error_exit "Text is required (--text)"
    
    $PYTHON -c "
import sqlite3
conn = sqlite3.connect('$KANBAN_DB')
c = conn.cursor()

c.execute('INSERT INTO comments (task_id, author, content) VALUES (?, ?, ?)',
          ($task_id, '$author', '$text'))

conn.commit()
conn.close()
print(f'Comment added to task $task_id')
"
}

# Stats
cmd_stats() {
    check_db
    
    $PYTHON -c "
import sqlite3
conn = sqlite3.connect('$KANBAN_DB')
c = conn.cursor()

c.execute('SELECT COUNT(*) FROM boards')
boards = c.fetchone()[0]

c.execute('SELECT COUNT(*) FROM tasks')
total_tasks = c.fetchone()[0]

c.execute(\"SELECT COUNT(*) FROM tasks WHERE status = 'todo'\")
todo = c.fetchone()[0]

c.execute(\"SELECT COUNT(*) FROM tasks WHERE status = 'in-progress'\")
in_progress = c.fetchone()[0]

c.execute(\"SELECT COUNT(*) FROM tasks WHERE status = 'blocked'\")
blocked = c.fetchone()[0]

c.execute(\"SELECT COUNT(*) FROM tasks WHERE status = 'done'\")
done = c.fetchone()[0]

conn.close()

print('📊 KANBAN STATISTICS')
print('='*40)
print(f'Boards:     {boards}')
print(f'Total Tasks: {total_tasks}')
print()
print(f'TODO:       {todo}')
print(f'In Progress:{in_progress}')
print(f'Blocked:    {blocked}')
print(f'Done:       {done}')
"
}

# Show usage
show_usage() {
    echo "📋 Hermes Kanban CLI"
    echo ""
    echo "Usage: kanban.sh <command> [options]"
    echo ""
    echo "Commands:"
    echo "  init              Initialize database"
    echo "  list              List all boards"
    echo "  show <id>         Show board with tasks"
    echo "  create [opts]     Create new task"
    echo "  complete <id>     Mark task as done"
    echo "  block <id>        Block task"
    echo "  unblock <id>      Unblock task"
    echo "  comment <id>      Add comment to task"
    echo "  stats             Show statistics"
    echo ""
    echo "Create options:"
    echo "  --title, -t       Task title (required)"
    echo "  --board, -b       Board ID (required)"
    echo "  --desc, -d        Description"
    echo "  --priority, -p    Priority: high/medium/low (default: medium)"
    echo "  --assignee, -a    Assignee profile name"
    echo ""
    echo "Examples:"
    echo "  kanban.sh init"
    echo "  kanban.sh create --title 'Write chapter' --board 1 --priority high"
    echo "  kanban.sh show 1"
    echo "  kanban.sh complete 5"
}

# Main dispatch
case "${1:-}" in
    init) cmd_init ;;
    list|ls) cmd_list ;;
    show) cmd_show "$2" ;;
    create) shift; cmd_create "$@" ;;
    complete) cmd_complete "$2" ;;
    block) shift; cmd_block "$@" ;;
    unblock) cmd_unblock "$2" ;;
    comment) shift; cmd_comment "$@" ;;
    stats) cmd_stats ;;
    help|--help|-h) show_usage ;;
    *) show_usage ;;
esac
