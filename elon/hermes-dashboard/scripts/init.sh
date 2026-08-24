#!/bin/bash
# Initialize Hermes Dashboard data directory
set -e

DATA_DIR="/opt/data/hermes/elon/hermes-dashboard/data"

echo "Initializing Hermes Dashboard..."
echo ""

# Create directories
mkdir -p "$DATA_DIR/logs"
mkdir -p "$DATA_DIR/sessions"

# Set permissions
chmod 755 "$DATA_DIR"
chmod 755 "$DATA_DIR/logs"
chmod 600 "$DATA_DIR/users.json"
chmod 644 "$DATA_DIR/agents.json"

# Generate default password hash if needed
if [ ! -f "$DATA_DIR/users.json" ]; then
    echo "Creating default users.json..."
    cat > "$DATA_DIR/users.json" << 'EOF'
{
  "users": [
    {
      "id": "user_001",
      "username": "tamim",
      "name": "Master Tamim",
      "password_hash": "$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi",
      "created_at": "2026-08-24",
      "last_login": null
    }
  ]
}
EOF
fi

echo ""
echo "✅ Initialization complete!"
echo ""
echo "Default credentials:"
echo "  Username: tamim"
echo "  Password: hermes2024"
echo ""
echo "To change password, run:"
echo "  php -r 'echo password_hash(\"newpassword\", PASSWORD_BCRYPT);'"
echo ""
echo "Access dashboard at: http://your-server/hermes-dashboard/"
