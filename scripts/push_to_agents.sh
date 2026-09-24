#!/bin/bash
# Push Atlas article to labsdigital/agents repo
# Usage: ./push_to_agents.sh <filename>

set -e

FILE="${1:-ketika-algoritma-menjadi-hakim-2026-08-28.md}"
DIR=$(dirname "$FILE")
BASENAME=$(basename "$FILE" .md)
HERMES_REPO="/opt/data/hermes"
AGENTS_REPO="/tmp/agents-clone"

echo "=== Pushing to labsdigital/agents ==="
echo ""

# Clone agents repo if not exists
if [ ! -d "$AGENTS_REPO" ]; then
    echo "📥 Cloning agents repo..."
    git clone https://github.com/labsdigital/agents.git "$AGENTS_REPO" 2>/dev/null || {
        # If empty, initialize
        mkdir -p "$AGENTS_REPO"
        cd "$AGENTS_REPO"
        git init
        git config user.email "hermes@taraka.id"
        git config user.name "Hermes Agent"
    }
fi

cd "$AGENTS_REPO"

# Create atlas/reports directory
mkdir -p atlas/reports

# Copy files
echo "📋 Copying files..."
cp "$HERMES_REPO/$FILE" atlas/reports/ 2>/dev/null || true
cp "$HERMES_REPO/${BASENAME}-html.html" atlas/reports/ 2>/dev/null || true
cp "$HERMES_REPO/${BASENAME}-diagram.svg" atlas/reports/ 2>/dev/null || true
cp "$HERMES_REPO/${BASENAME}-artistik.png" atlas/reports/ 2>/dev/null || true

# Commit and push
echo "📤 Committing..."
git add .
git commit -m "Atlas: $BASENAME" 2>/dev/null || echo "No changes to commit"
git push origin main 2>&1 || git push -u origin main 2>&1

echo ""
echo "✅ Pushed to: https://github.com/labsdigital/agents/tree/main/atlas/reports"
echo ""
echo "🔗 Article URL:"
echo "   https://github.com/labsdigital/agents/blob/main/atlas/reports/$FILE"
