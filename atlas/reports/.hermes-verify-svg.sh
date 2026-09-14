#!/bin/bash
# Ad-hoc verification script for Atlas article SVG diagram
# Checks SVG validity, accessibility, and integration

set -e

SVG_FILE="/opt/data/hermes/atlas/reports/kapabilitas-edu-2026-09-02.svg"
REMOTE_URL="https://raw.githubusercontent.com/labsdigital/agents/main/atlas/reports/kapabilitas-edu-2026-09-02.svg"

echo "=== SVG Verification Report ==="
echo ""

# Check 1: File exists and is not empty
if [ ! -f "$SVG_FILE" ]; then
    echo "❌ FAIL: SVG file not found at $SVG_FILE"
    exit 1
fi

SIZE=$(stat -c%s "$SVG_FILE" 2>/dev/null || stat -f%z "$SVG_FILE" 2>/dev/null)
if [ "$SIZE" -eq 0 ]; then
    echo "❌ FAIL: SVG file is empty"
    exit 1
fi
echo "✅ Local file exists ($SIZE bytes)"

# Check 2: SVG structure validation
START_TAG=$(grep -c "<svg" "$SVG_FILE" || true)
END_TAG=$(grep -c "</svg>" "$SVG_FILE" || true)

if [ "$START_TAG" -ne 1 ] || [ "$END_TAG" -ne 1 ]; then
    echo "❌ FAIL: SVG structure invalid (found $START_TAG opening, $END_TAG closing tags)"
    exit 1
fi
echo "✅ SVG structure valid (properly opened/closed)"

# Check 3: Required attributes
if ! grep -q 'xmlns=' "$SVG_FILE"; then
    echo "❌ FAIL: Missing xmlns attribute"
    exit 1
fi
echo "✅ XML namespace defined"

if ! grep -q 'viewBox=' "$SVG_FILE"; then
    echo "⚠️  WARNING: Missing viewBox attribute (may cause scaling issues)"
else
    echo "✅ viewBox attribute present"
fi

# Check 4: Remote accessibility
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$REMOTE_URL" 2>/dev/null || echo "000")
REMOTE_SIZE=$(curl -s "$REMOTE_URL" 2>/dev/null | wc -c)

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Remote access OK (HTTP $HTTP_CODE, $REMOTE_SIZE bytes)"
else
    echo "❌ FAIL: Remote access failed (HTTP $HTTP_CODE)"
    exit 1
fi

# Check 5: Content sanity (no XML declaration issues)
if head -1 "$SVG_FILE" | grep -q '<?xml'; then
    echo "⚠️  WARNING: XML declaration found (may cause embedding issues in HTML)"
else
    echo "✅ No XML declaration (clean for HTML embedding)"
fi

# Check 6: Image references in article MD
MD_FILE="/opt/data/hermes/atlas/reports/kapabilitas-edu-2026-09-02.md"
if grep -q "kapabilitas-edu-2026-09-02.svg" "$MD_FILE"; then
    echo "✅ SVG referenced in article MD"
else
    echo "⚠️  WARNING: SVG not referenced in article MD"
fi

echo ""
echo "=== Summary ==="
echo "All checks passed. SVG is valid and accessible."
