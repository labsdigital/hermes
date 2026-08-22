#!/bin/bash
# Chalbi Sync Script - Sync articles to Airtable tblArticles
# Usage: bash sync_to_airtable.sh <article-file.md>

set -e

# Check for AIRTABLE_API_KEY
if [ -z "$AIRTABLE_API_KEY" ]; then
    # Try to read from .env file
    if [ -f "/opt/data/.env" ]; then
        export AIRTABLE_API_KEY=$(grep "AIRTABLE_API_KEY" /opt/data/.env | tail -1 | cut -d= -f2 | tr -d ' \n\r')
    fi
fi

if [ -z "$AIRTABLE_API_KEY" ]; then
    echo "❌ Error: AIRTABLE_API_KEY not found"
    exit 1
fi

# Get the article file
ARTICLE_FILE="$1"

if [ -z "$ARTICLE_FILE" ]; then
    echo "Usage: bash sync_to_airtable.sh <article-file.md>"
    echo "Example: bash sync_to_airtable.sh reports/cinta-ilahi-2026-08-20.md"
    exit 1
fi

# Check if file exists
if [ ! -f "$ARTICLE_FILE" ]; then
    echo "❌ Error: File not found: $ARTICLE_FILE"
    exit 1
fi

# Extract ID and title from filename
FILENAME=$(basename "$ARTICLE_FILE")
ARTICLE_ID="chalbi-${FILENAME%.md}"
ARTICLE_DATE=$(echo "$FILENAME" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' | head -1)

# Extract title from first line of markdown
TITLE=$(head -1 "$ARTICLE_FILE" | sed 's/^# //;s/\*.*//;s/-.*//' | xargs)

echo "📊 Syncing to Airtable..."
echo "   ID: $ARTICLE_ID"
echo "   Title: $TITLE"
echo "   Date: $ARTICLE_DATE"

# Read content (remove markdown header)
CONTENT=$(tail -n +3 "$ARTICLE_FILE")

# Create JSON payload
JSON_PAYLOAD=$(python3 -c "
import json
import sys

title = '''$TITLE'''
content = '''$CONTENT'''
article_id = '''$ARTICLE_ID'''
date = '''$ARTICLE_DATE'''

record = {
    'fields': {
        'id': article_id,
        'title': title,
        'content': content,
        'published_at': date
    }
}

print(json.dumps(record))
")

# Send to Airtable
echo "   Sending to Airtable..."
RESPONSE=$(curl -s -X POST \
    "https://api.airtable.com/v0/appHDwcERrnRH02YS/tblExdQkNbL9bZbgQ" \
    -H "Authorization: Bearer $AIRTABLE_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$JSON_PAYLOAD")

# Check response
if echo "$RESPONSE" | grep -q '"id"'; then
    RECORD_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
    echo "✅ Berhasil! Record ID: $RECORD_ID"
    echo ""
    echo "   Airtable URL: https://airtable.com/appHDwcERrnRH02YS/tblExdQkNbL9bZbgQ/$RECORD_ID"
else
    echo "❌ Error: Failed to sync to Airtable"
    echo "$RESPONSE"
    exit 1
fi
