#!/bin/bash
# Update Kanban Dashboard - Run via cron or manually
# Location: /opt/data/hermes/scripts/update_dashboard.sh

set -e

SCRIPT="/opt/data/hermes/scripts/export_kanban_json.py"
REPO="/opt/data/hermes"
LOG_FILE="/opt/data/hermes/logs/dashboard-update.log"

mkdir -p "$(dirname $LOG_FILE)"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting dashboard update..." >> $LOG_FILE

# Run export script
python3 $SCRIPT >> $LOG_FILE 2>&1

# Check if JSON changed
cd $REPO
git diff --quiet kanban/kanban-data.json && echo "[$(date)] No changes" >> $LOG_FILE || {
    echo "[$(date)] Changes detected, committing..." >> $LOG_FILE
    git add kanban/kanban-data.json
    git commit -m "Dashboard: Auto-update kanban data" >> $LOG_FILE 2>&1
    git push origin main >> $LOG_FILE 2>&1
    echo "[$(date)] Pushed to GitHub" >> $LOG_FILE
}

echo "[$(date)] Done" >> $LOG_FILE
