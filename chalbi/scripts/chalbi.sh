#!/bin/bash
# Chalbi CLI - Command Line Interface untuk Masnavi Rumi API
# Usage: ./chalbi.sh <command> [arguments]

set -e

API_BASE="https://masnavi.ai/api"
COLOR_RESET="\033[0m"
COLOR_GOLD="\033[38;5;178m"
COLOR_RED="\033[38;5;196m"
COLOR_GREEN="\033[38;5;82m"

# Colors for output
echo -e "${COLOR_GOLD}╔══════════════════════════════════════════════════════════════╗${COLOR_RESET}"
echo -e "${COLOR_GOLD}║         CHALBI - Rumi Masnavi CLI                           ║${COLOR_RESET}"
echo -e "${COLOR_GOLD}╚══════════════════════════════════════════════════════════════╝${COLOR_RESET}"
echo ""

# Show usage if no arguments
if [ $# -eq 0 ]; then
    echo "Usage: $0 <command> [options]"
    echo ""
    echo "Commands:"
    echo "  search <persian_text> [limit]     - Search by Persian text"
    echo "  meaning <query> [limit]           - Semantic search (any language)"
    echo "  lookup <citation>                 - Get specific beyt (e.g., M1:1)"
    echo "  verify <text>                     - Verify if quote is authentic"
    echo "  section <id>                      - Get full section"
    echo "  random [daftar]                   - Random beyt from daftar"
    echo "  toc [daftar]                      - Table of contents"
    echo "  corpus                            - Download full corpus"
    echo "  help                              - Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 meaning \"love\" 5"
    echo "  $0 lookup M1:1"
    echo "  $0 search عشق 10"
    exit 0
fi

COMMAND=$1
shift

case $COMMAND in
    search)
        QUERY="${*}"
        echo -e "${COLOR_GREEN}🔍 Searching for: ${QUERY}${COLOR_RESET}"
        curl -s "${API_BASE}/search?q=${QUERY}&limit=5" | python3 -m json.tool
        ;;
    
    meaning)
        QUERY="${*}"
        echo -e "${COLOR_GREEN}🎯 Semantic search for: ${QUERY}${COLOR_RESET}"
        curl -s "${API_BASE}/search_meaning?q=${QUERY}&limit=5" | python3 -m json.tool
        ;;
    
    lookup)
        CITATION="${*}"
        echo -e "${COLOR_GREEN}📖 Looking up: ${CITATION}${COLOR_RESET}"
        curl -s "${API_BASE}/lookup?citation=${CITATION}" | python3 -m json.tool
        ;;
    
    verify)
        TEXT=$(echo "$*" | sed 's/ /%20/g')
        echo -e "${COLOR_GREEN}✅ Verifying quote...${COLOR_RESET}"
        curl -s "${API_BASE}/verify?text=${TEXT}" | python3 -m json.tool
        ;;
    
    section)
        SECTION_ID="${*}"
        echo -e "${COLOR_GREEN}📚 Getting section: ${SECTION_ID}${COLOR_RESET}"
        curl -s "${API_BASE}/get_section?section_id=${SECTION_ID}" | python3 -m json.tool
        ;;
    
    random)
        DAFTAR="${*:-1}"
        echo -e "${COLOR_GREEN}🎲 Random beyt from Daftar ${DAFTAR}${COLOR_RESET}"
        curl -s "${API_BASE}/random_beyt?daftar=${DAFTAR}" | python3 -m json.tool
        ;;
    
    toc)
        DAFTAR="${*:-1}"
        echo -e "${COLOR_GREEN}📋 Table of Contents - Daftar ${DAFTAR}${COLOR_RESET}"
        curl -s "${API_BASE}/table_of_contents?daftar=${DAFTAR}" | python3 -m json.tool
        ;;
    
    corpus)
        echo -e "${COLOR_GREEN}⬇️  Downloading full corpus...${COLOR_RESET}"
        echo "This may take a while (25,635 beyts)..."
        curl -sL "https://masnavi.ai/corpus.jsonl" -o /tmp/corpus.jsonl
        echo "✅ Downloaded to /tmp/corpus.jsonl"
        echo "💡 Preview (first 5 lines):"
        head -5 /tmp/corpus.jsonl | python3 -m json.tool
        ;;
    
    help|--help|-h)
        # Already shown above
        ;;
    
    *)
        echo -e "${COLOR_RED}❌ Unknown command: ${COMMAND}${COLOR_RESET}"
        echo "Run without arguments to see usage"
        exit 1
        ;;
esac
