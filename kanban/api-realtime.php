<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

$dbPath = '/opt/data/home/.hermes/kanban.db';

if (!file_exists($dbPath)) {
    echo json_encode(['error' => 'Database not found']);
    exit;
}

try {
    $pdo = new PDO("sqlite:$dbPath");
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    $stmt = $pdo->query("SELECT id, name, description FROM boards WHERE status = 'active' ORDER BY id");
    $boards = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
    $result = ['last_updated' => date('c'), 'boards' => []];
    
    foreach ($boards as $board) {
        $tasksStmt = $pdo->prepare("
            SELECT id, title, description, status, priority, assignee, blocked_reason, created_at
            FROM tasks WHERE board_id = ? 
            ORDER BY 
                CASE status WHEN 'todo' THEN 1 WHEN 'in-progress' THEN 2 WHEN 'blocked' THEN 3 WHEN 'done' THEN 4 END,
                CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 WHEN 'low' THEN 3 END
        ");
        $tasksStmt->execute([$board['id']]);
        $tasks = $tasksStmt->fetchAll(PDO::FETCH_ASSOC);
        
        $result['boards'][] = [
            'id' => $board['id'],
            'name' => $board['name'],
            'description' => $board['description'],
            'tasks' => $tasks
        ];
    }
    
    echo json_encode($result);
    
} catch (Exception $e) {
    echo json_encode(['error' => $e->getMessage()]);
}
