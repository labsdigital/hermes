#!/bin/bash
# Hermes Dashboard Setup Script
# Run this on your VPS/shared hosting

set -e

DASHBOARD_DIR="/opt/data/hermes/elon/hermes-dashboard"
WEB_ROOT="/var/www/html"  # Change to your web root

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║         Hermes Dashboard Setup                            ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check PHP
if ! command -v php &> /dev/null; then
    echo "❌ PHP is not installed. Installing..."
    apt-get update && apt-get install -y php php-cli php-curl php-json
fi

echo "✅ PHP detected: $(php -v | head -1)"
echo ""

# Generate password hash
echo "🔐 Generating password hash..."
HASH=$(php -r 'echo password_hash("hermes2024", PASSWORD_BCRYPT);')
echo "   Password: hermes2024"
echo "   Hash: $HASH"
echo ""

# Update users.json
echo "📝 Updating users.json..."
cat > "$DASHBOARD_DIR/data/users.json" << EOF
{
  "users": [
    {
      "id": "user_001",
      "username": "tamim",
      "name": "Master Tamim",
      "password_hash": "$HASH",
      "created_at": "$(date +%Y-%m-%d)",
      "last_login": null
    },
    {
      "id": "user_002",
      "username": "admin",
      "name": "Admin",
      "password_hash": "$HASH",
      "created_at": "$(date +%Y-%m-%d)",
      "last_login": null
    }
  ]
}
EOF
echo "✅ users.json updated"
echo ""

# Set permissions
echo "🔒 Setting permissions..."
chmod 755 "$DASHBOARD_DIR"
chmod 755 "$DASHBOARD_DIR/api"
chmod 755 "$DASHBOARD_DIR/data"
chmod 755 "$DASHBOARD_DIR/data/logs"
chmod 600 "$DASHBOARD_DIR/data/users.json"
chmod 644 "$DASHBOARD_DIR/data/agents.json"
echo "✅ Permissions set"
echo ""

# Create web symlink (optional)
if [ -d "$WEB_ROOT" ]; then
    echo "🌐 Creating web symlink..."
    ln -sf "$DASHBOARD_DIR" "$WEB_ROOT/hermes-dashboard"
    echo "✅ Dashboard accessible at: http://localhost/hermes-dashboard/"
else
    echo "⚠️  Web root not found at $WEB_ROOT"
    echo "   Upload files to your shared hosting via FTP/cPanel"
fi
echo ""

echo "═══════════════════════════════════════════════════════════"
echo "                    SETUP COMPLETE!                        ║"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "📍 Access Dashboard:"
echo "   Local:  http://localhost/hermes-dashboard/"
echo "   GitHub: https://github.com/labsdigital/hermes/tree/main/elon/hermes-dashboard"
echo ""
echo "🔑 Default Login:"
echo "   Username: tamim"
echo "   Password: hermes2024"
echo ""
echo "⚠️  IMPORTANT: Change password after first login!"
echo "   Edit: $DASHBOARD_DIR/data/users.json"
echo ""
echo "📚 Hermes API:"
echo "   Gateway: http://localhost:9119"
echo "   Dashboard will proxy to this endpoint"
echo ""
