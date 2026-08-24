<?php
/**
 * Hermes Dashboard - Configuration
 * 
 * ⚠️ IMPORTANT: Edit these settings for your environment!
 * 
 * For shared hosting + VPS setup:
 * 1. Hermes gateway harus bisa diakses dari internet
 * 2. Atau gunakan reverse proxy/VPN
 */

// ============================================
// HERMES GATEWAY CONFIGURATION
// ============================================

// Option A: Jika gateway accessible dari internet (recommended)
define('HERMES_API_URL', 'https://hermes.yourdomain.com'); // ← GANTI dengan URL gateway Anda

// Option B: Jika menggunakan VPN/Tunnel (ngrok, cloudflare tunnel, dll)
// define('HERMES_API_URL', 'https://abc123.ngrok.io');

// Option C: Localhost (HANYA untuk testing di VPS langsung)
// define('HERMES_API_URL', 'http://localhost:9119');

// Authentication untuk Hermes Gateway (jika perlu)
define('HERMES_API_KEY', ''); // Kosongkan jika tidak pakai API key
define('HERMES_API_TOKEN', ''); // Atau gunakan token

// ============================================
// DASHBOARD CONFIGURATION
// ============================================

// Admin email (untuk notifikasi)
define('ADMIN_EMAIL', 'admin@yourdomain.com');

// Session lifetime (30 minutes)
define('SESSION_LIFETIME', 1800);

// Timezone
date_default_timezone_set('Asia/Jakarta');

// ============================================
// SECURITY SETTINGS
// ============================================

// Enable HTTPS only (recommended for production)
define('FORCE_HTTPS', true);

// CSRF protection (enable in future)
define('ENABLE_CSRF', false); // TODO: Implement CSRF protection

// Rate limiting for login (attempts, window seconds)
define('LOGIN_MAX_ATTEMPTS', 5);
define('LOGIN_LOCKOUT_TIME', 900); // 15 minutes

// ============================================
// FEATURE FLAGS
// ============================================

// Enable chat feature
define('ENABLE_CHAT', true);

// Enable task management
define('ENABLE_TASKS', true);

// Enable file manager
define('ENABLE_FILEMANAGER', false); // TODO: Implement

// Enable system stats
define('ENABLE_STATS', true);

// ============================================
// LOAD CONFIG
// ============================================

// Auto-load if constants not defined
if (!defined('DATA_DIR')) {
    define('DATA_DIR', __DIR__ . '/data');
}

if (!defined('HERMES_API_URL')) {
    define('HERMES_API_URL', 'http://localhost:9119');
}
