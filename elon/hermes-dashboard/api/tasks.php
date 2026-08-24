<?php
/**
 * API Endpoint: Task Management
 * Spawn, list, and kill agent tasks
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, DELETE, OPTIONS');
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

$action = $_SERVER['REQUEST_METHOD'];
$tasksFile = __DIR__ . '/../data/tasks.json';

// Initialize tasks file if not exists
if (!file_exists($tasksFile)) {
    file_put_contents($tasksFile, json_encode(['tasks' => []], JSON_PRETTY_PRINT));
}

$tasks = json_decode(file_get_contents($tasksFile), true);

switch ($action) {
    case 'GET':
        // List tasks
        echo json_encode($tasks['tasks'] ?? []);
        break;
        
    case 'POST':
        // Spawn new task
        $input = json_decode(file_get_contents('php://input'), true);
        $agent = $input['agent'] ?? '';
        $prompt = $input['prompt'] ?? '';
        
        if (empty($agent) || empty($prompt)) {
            http_response_code(400);
            echo json_encode(['error' => 'Agent and prompt are required']);
            exit;
        }
        
        $taskId = 'task_' . uniqid();
        $task = [
            'id' => $taskId,
            'agent' => $agent,
            'prompt' => $prompt,
            'status' => 'running',
            'created_at' => date('c'),
            'started_at' => time()
        ];
        
        $tasks['tasks'][] = $task;
        file_put_contents($tasksFile, json_encode($tasks, JSON_PRETTY_PRINT));
        
        echo json_encode([
            'success' => true,
            'task' => $task
        ]);
        break;
        
    case 'DELETE':
        // Kill task
        $taskId = $_GET['id'] ?? '';
        
        if (empty($taskId)) {
            http_response_code(400);
            echo json_encode(['error' => 'Task ID is required']);
            exit;
        }
        
        $found = false;
        foreach ($tasks['tasks'] as &$t) {
            if ($t['id'] === $taskId) {
                $t['status'] = 'killed';
                $t['killed_at' => time();
                $found = true;
                break;
            }
        }
        
        if ($found) {
            file_put_contents($tasksFile, json_encode($tasks, JSON_PRETTY_PRINT));
            echo json_encode(['success' => true]);
        } else {
            http_response_code(404);
            echo json_encode(['error' => 'Task not found']);
        }
        break;
        
    default:
        http_response_code(405);
        echo json_encode(['error' => 'Method not allowed']);
}
