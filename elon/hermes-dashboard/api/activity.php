<?php
/**
 * API Endpoint: Recent Activity
 * Returns recent git activity
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

// Get git activity
$limit = isset($_GET['limit']) ? intval($_GET['limit']) : 10;
$output = [];
exec("cd /opt/data/hermes && git log --oneline -{$limit} --pretty=format:'%h|%s|%at'", $output);

$activities = [];
foreach ($output as $line) {
    if ($line) {
        $parts = explode('|', $line);
        if (count($parts) === 3) {
            $activities[] = [
                'hash' => $parts[0],
                'message' => $parts[1],
                'time' => intval($parts[2])
            ];
        }
    }
}

echo json_encode($activities);
