#!/bin/bash
# Script untuk sync artikel ke Airtable
# Usage: ./sync_to_airtable.sh <filename>

AIRTABLE_TOKEN="${AIRTABLE_API_KEY}"
if [ -z "$AIRTABLE_TOKEN" ]; then
    echo "❌ AIRTABLE_API_KEY tidak ditemukan di environment"
    exit 1
fi

ARTICLE_FILE="/opt/data/hermes/max/reports/${1}"
if [ ! -f "$ARTICLE_FILE" ]; then
    echo "❌ File tidak ditemukan: $ARTICLE_FILE"
    exit 1
fi

# Extract ID dari filename
FILENAME=$(basename "$ARTICLE_FILE" .md)
ARTICLE_ID="max-${FILENAME}"

echo "📊 Syncing ke Airtable..."
echo "   ID: $ARTICLE_ID"

# Read content dan encode sebagai JSON
CONTENT=$(python3 -c "import json,sys; print(json.dumps(sys.stdin.read()))" < "$ARTICLE_FILE")

# Kirim ke Airtable
RESPONSE=$(curl -s -X POST "https://api.airtable.com/v0/appHDwcERrnRH02YS/tbl9TvJ9QztbHeyaY" \
    -H "Authorization: Bearer $AIRTABLE_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"records\":[{\"fields\":{\"id\":\"$ARTICLE_ID\",\"content\":$CONTENT}}]}")

# Check response
if echo "$RESPONSE" | grep -q '"id"'; then
    RECORD_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['records'][0]['id'])")
    echo "✅ Berhasil! Record ID: $RECORD_ID"
else
    echo "⚠️  Sync gagal:"
    echo "$RESPONSE"
    exit 1
fi
