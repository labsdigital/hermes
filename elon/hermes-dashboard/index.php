<?php
/**
 * Hermes Dashboard - Main Entry Point
 * PHP wrapper untuk Hermes Agent Gateway API
 */

// Configuration
define('HERMES_API_URL', 'http://localhost:9119');
define('DATA_DIR', __DIR__ . '/data');
define('SESSION_LIFETIME', 1800); // 30 minutes

// Start session
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

// Redirect to login if not authenticated
if (!isset($_SESSION['authenticated']) || $_SESSION['authenticated'] !== true) {
    header('Location: login.php');
    exit;
}

// Load user data
function getUser() {
    $usersFile = DATA_DIR . '/users.json';
    if (!file_exists($usersFile)) {
        return null;
    }
    $users = json_decode(file_get_contents($usersFile), true);
    if (!isset($_SESSION['username'])) {
        return null;
    }
    foreach ($users['users'] as $user) {
        if ($user['username'] === $_SESSION['username']) {
            return $user;
        }
    }
    return null;
}

// Call Hermes API
function callHermesAPI($endpoint, $method = 'GET', $data = null) {
    $url = HERMES_API_URL . $endpoint;
    $ch = curl_init();
    
    $headers = [
        'Content-Type: application/json',
    ];
    
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 30);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    
    if ($method === 'POST' && $data) {
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    }
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    return [
        'status' => $httpCode,
        'body' => json_decode($response, true) ?: $response
    ];
}

// Get agent statistics from filesystem
function getAgentStats() {
    $hermesPath = '/opt/data/hermes';
    $agents = [
        'zetta' => ['name' => 'Zetta', 'role' => 'Main Agent', 'path' => ''],
        'max' => ['name' => 'Max', 'role' => 'Research Writer', 'path' => 'max/reports'],
        'elon' => ['name' => 'Elon', 'role' => 'Web Developer', 'path' => 'elon'],
        'chalbi' => ['name' => 'Chalbi', 'role' => 'Rumi Scholar', 'path' => 'chalbi/reports'],
        'taraka' => ['name' => 'Taraka', 'role' => 'Foundation Writer', 'path' => 'taraka/proposals']
    ];
    
    foreach ($agents as &$agent) {
        $path = $hermesPath . '/' . $agent['path'];
        if (file_exists($path)) {
            $files = glob($path . '/*.md');
            $agent['count'] = count($files);
            $agent['status'] = 'online';
        } else {
            $agent['count'] = 0;
            $agent['status'] = 'offline';
        }
    }
    
    return $agents;
}

// Get system statistics
function getSystemStats() {
    $stats = [];
    
    // Uptime
    if (file_exists('/proc/uptime')) {
        $uptime = explode(' ', file_get_contents('/proc/uptime'));
        $seconds = (int)$uptime[0];
        $stats['uptime'] = sprintf('%d days, %d hours', 
            floor($seconds / 86400), 
            floor(($seconds % 86400) / 3600)
        );
    }
    
    // Memory
    if (file_exists('/proc/meminfo')) {
        $mem = parse_ini_file('/proc/meminfo', true);
        $total = $mem['MemTotal'][0] / 1024; // KB to MB
        $free = $mem['MemFree'][0] / 1024;
        $stats['memory'] = [
            'total' => round($total / 1024, 2), // MB to GB
            'free' => round($free / 1024, 2),
            'used' => round(($total - $free) / 1024, 2),
            'percent' => round(($total - $free) / $total * 100, 1)
        ];
    }
    
    // CPU Load
    if (file_exists('/proc/loadavg')) {
        $load = explode(' ', file_get_contents('/proc/loadavg'));
        $stats['cpu'] = [
            'load_1' => $load[0],
            'load_5' => $load[1],
            'load_15' => $load[2]
        ];
    }
    
    // Disk
    $disk = disk_free_space('/');
    $totalDisk = disk_total_space('/');
    $stats['disk'] = [
        'total' => round($totalDisk / 1073741824, 2), // bytes to GB
        'free' => round($disk / 1073741824, 2),
        'used' => round(($totalDisk - $disk) / 1073741824, 2),
        'percent' => round(($totalDisk - $disk) / $totalDisk * 100, 1)
    ];
    
    return $stats;
}

// Get recent git activity
function getGitActivity($limit = 10) {
    $output = [];
    exec("cd /opt/data/hermes && git log --oneline -{$limit}", $output);
    
    $activities = [];
    foreach ($output as $line) {
        if (preg_match('/^([a-f0-9]+) (.+)$/', $line, $matches)) {
            $activities[] = [
                'hash' => $matches[1],
                'message' => $matches[2],
                'time' => time() - rand(60, 86400) // Simulated time
            ];
        }
    }
    return $activities;
}

// Get user
$user = getUser();
$pageTitle = 'Hermes Dashboard';

// Include header
include 'includes/header.php';
?>

<div class="dashboard">
    <!-- Stats Cards -->
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-icon">🤖</div>
            <div class="stat-value" id="agentCount">5</div>
            <div class="stat-label">Total Agents</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">📄</div>
            <div class="stat-value" id="articleCount">-</div>
            <div class="stat-label">Articles</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">💾</div>
            <div class="stat-value" id="memoryUsage">-</div>
            <div class="stat-label">Memory Usage</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">⏱️</div>
            <div class="stat-value" id="uptime">-</div>
            <div class="stat-label">Uptime</div>
        </div>
    </div>

    <!-- Agents Section -->
    <div class="section">
        <div class="section-header">
            <h2>🤖 Agent Status</h2>
            <button class="btn-refresh" onclick="loadAgents()">🔄 Refresh</button>
        </div>
        <div class="agent-grid" id="agentGrid">
            <!-- Populated by JavaScript -->
        </div>
    </div>

    <!-- Activity Feed -->
    <div class="section">
        <div class="section-header">
            <h2>📝 Recent Activity</h2>
            <button class="btn-refresh" onclick="loadActivity()">🔄 Refresh</button>
        </div>
        <div class="activity-list" id="activityList">
            <!-- Populated by JavaScript -->
        </div>
    </div>

    <!-- Quick Actions -->
    <div class="section">
        <div class="section-header">
            <h2>⚡ Quick Actions</h2>
        </div>
        <div class="quick-actions">
            <a href="chat.php" class="action-card">
                <div class="action-icon">💬</div>
                <div class="action-title">Chat with Agent</div>
                <div class="action-desc">Interact with Hermes agents</div>
            </a>
            <a href="agents.php" class="action-card">
                <div class="action-icon">📊</div>
                <div class="action-title">Manage Agents</div>
                <div class="action-desc">Spawn, monitor, kill tasks</div>
            </a>
            <a href="files.php" class="action-card">
                <div class="action-icon">📁</div>
                <div class="action-title">File Manager</div>
                <div class="action-desc">Browse hermes repository</div>
            </a>
            <a href="settings.php" class="action-card">
                <div class="action-icon">⚙️</div>
                <div class="action-title">Settings</div>
                <div class="action-desc">Configure dashboard</div>
            </a>
        </div>
    </div>
</div>

<script>
const HERMES_API = '<?= HERMES_API_URL ?>';

async function loadAgents() {
    const response = await fetch('api/agents.php');
    const agents = await response.json();
    
    const grid = document.getElementById('agentGrid');
    grid.innerHTML = agents.map(agent => `
        <div class="agent-card status-${agent.status}">
            <div class="agent-header">
                <span class="agent-avatar">${agent.name.charAt(0)}</span>
                <div class="agent-info">
                    <h3>${agent.name}</h3>
                    <span class="agent-role">${agent.role}</span>
                </div>
                <span class="status-badge ${agent.status}">${agent.status}</span>
            </div>
            <div class="agent-stats">
                <div class="stat">
                    <span class="stat-number">${agent.count}</span>
                    <span class="stat-label">Items</span>
                </div>
            </div>
            <div class="agent-actions">
                <button class="btn-chat" onclick="chatWithAgent('${agent.id}')">💬 Chat</button>
                <button class="btn-log" onclick="viewLog('${agent.id}')">📄 Log</button>
            </div>
        </div>
    `).join('');
}

async function loadActivity() {
    const response = await fetch('api/activity.php');
    const activities = await response.json();
    
    const list = document.getElementById('activityList');
    list.innerHTML = activities.map(activity => `
        <div class="activity-item">
            <div class="activity-content">
                <span class="activity-hash">${activity.hash}</span>
                <span class="activity-message">${activity.message}</span>
            </div>
            <span class="activity-time">${timeAgo(activity.time)}</span>
        </div>
    `).join('');
}

function timeAgo(timestamp) {
    const seconds = Math.floor(Date.now() / 1000) - timestamp;
    if (seconds < 60) return 'Just now';
    if (seconds < 3600) return Math.floor(seconds / 60) + 'm ago';
    if (seconds < 86400) return Math.floor(seconds / 3600) + 'h ago';
    return Math.floor(seconds / 86400) + 'd ago';
}

function chatWithAgent(agentId) {
    window.location.href = `chat.php?agent=${agentId}`;
}

function viewLog(agentId) {
    window.location.href = `logs.php?agent=${agentId}`;
}

// Load data on page load
document.addEventListener('DOMContentLoaded', () => {
    loadAgents();
    loadActivity();
    
    // Auto-refresh every 30 seconds
    setInterval(() => {
        loadAgents();
        loadActivity();
    }, 30000);
});
</script>

<?php include 'includes/footer.php'; ?>
