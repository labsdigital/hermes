<?php
/**
 * API Endpoint: Agent Status
 * Returns list of agents with their status
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
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

// Load agents data
$agentsFile = __DIR__ . '/../data/agents.json';
if (!file_exists($agentsFile)) {
    http_response_code(500);
    echo json_encode(['error' => 'Agents data not found']);
    exit;
}

$agents = json_decode(file_get_contents($agentsFile), true);

// Try to get real status from Hermes gateway
try {
    $ch = curl_init('http://localhost:9119/api/v1/agents');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 5);
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    if ($httpCode === 200 && $response) {
        $apiAgents = json_decode($response, true);
        if (is_array($apiAgents)) {
            // Merge API data with local data
            foreach ($agents['agents'] as &$agent) {
                foreach ($apiAgents as $apiAgent) {
                    if ($apiAgent['id'] === $agent['id']) {
                        $agent['status'] = $apiAgent['status'] ?? $agent['status'];
                        $agent['last_seen'] = $apiAgent['last_seen'] ?? $agent['last_seen'];
                    }
                }
            }
        }
    }
} catch (Exception $e) {
    // Fall back to static data
    error_log('Hermes API error: ' . $e->getMessage());
}

echo json_encode($agents['agents']);
