<?php
/**
 * API Endpoint: System Statistics
 * Returns system resource usage
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

// Check authentication
session_start();
if (!isset($_SESSION['authenticated']) || $_SESSION['authenticated'] !== true) {
    http_response_code(401);
    echo json_encode(['error' => 'Unauthorized']);
    exit;
}

$stats = [];

// Uptime
if (file_exists('/proc/uptime')) {
    $uptime = explode(' ', file_get_contents('/proc/uptime'));
    $seconds = (int)$uptime[0];
    $stats['uptime'] = [
        'seconds' => $seconds,
        'formatted' => sprintf('%d days, %d hours', 
            floor($seconds / 86400), 
            floor(($seconds % 86400) / 3600)
        )
    ];
}

// Memory
if (file_exists('/proc/meminfo')) {
    $mem = parse_ini_file('/proc/meminfo', true);
    $total = $mem['MemTotal'][0] / 1024 / 1024; // GB
    $free = $mem['MemFree'][0] / 1024 / 1024;
    $available = isset($mem['MemAvailable']) ? $mem['MemAvailable'][0] / 1024 / 1024 : $free;
    $used = $total - $available;
    $stats['memory'] = [
        'total' => round($total, 2),
        'used' => round($used, 2),
        'free' => round($available, 2),
        'percent' => round($used / $total * 100, 1)
    ];
}

// CPU Load
if (file_exists('/proc/loadavg')) {
    $load = explode(' ', file_get_contents('/proc/loadavg'));
    $stats['cpu'] = [
        'load_1' => floatval($load[0]),
        'load_5' => floatval($load[1]),
        'load_15' => floatval($load[2])
    ];
}

// Disk
$diskTotal = disk_total_space('/');
$diskFree = disk_free_space('/');
$diskUsed = $diskTotal - $diskFree;
$stats['disk'] = [
    'total' => round($diskTotal / 1073741824, 2),
    'used' => round($diskUsed / 1073741824, 2),
    'free' => round($diskFree / 1073741824, 2),
    'percent' => round($diskUsed / $diskTotal * 100, 1)
];

// Count files in hermes repo
$hermesPath = '/opt/data/hermes';
$stats['files'] = [
    'articles' => count(glob($hermesPath . '/max/reports/*.md')),
    'presentations' => count(glob($hermesPath . '/elon/*.html')),
    'proposals' => count(glob($hermesPath . '/taraka/*.md')),
    'total_commits' => trim(exec("cd {$hermesPath} && git log --oneline | wc -l"))
];

echo json_encode([
    'success' => true,
    'timestamp' => date('c'),
    'stats' => $stats
]);
