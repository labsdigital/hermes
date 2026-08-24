<?php
/**
 * API Endpoint: Chat with Agent
 * Forwards messages to Hermes gateway
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
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

// Get request data
$input = json_decode(file_get_contents('php://input'), true);
$agent = $input['agent'] ?? '';
$message = $input['message'] ?? '';
$session_id = $input['session_id'] ?? session_id();

// Validate
if (empty($agent) || empty($message)) {
    http_response_code(400);
    echo json_encode(['error' => 'Agent and message are required']);
    exit;
}

// Forward to Hermes gateway
try {
    $url = 'http://localhost:9119/api/v1/chat';
    $payload = [
        'agent' => $agent,
        'message' => $message,
        'session_id' => $session_id
    ];
    
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload));
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
    curl_setopt($ch, CURLOPT_TIMEOUT, 60);
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    if ($httpCode === 200 && $response) {
        $result = json_decode($response, true);
        echo json_encode([
            'success' => true,
            'reply' => $result['message'] ?? $result['reply'] ?? 'Response received',
            'timestamp' => date('c')
        ]);
    } else {
        // Fallback: simulate response for demo
        echo json_encode([
            'success' => true,
            'reply' => "This is a simulated response from {$agent}. Connect to Hermes gateway for real responses.",
            'timestamp' => date('c'),
            'demo' => true
        ]);
    }
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'error' => 'Failed to connect to Hermes gateway',
        'demo' => true
    ]);
}
