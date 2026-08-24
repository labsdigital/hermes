<?php
/**
 * Hermes Dashboard - Login Page
 * Simple file-based authentication
 */

// Configuration
define('DATA_DIR', __DIR__ . '/data');
define('MAX_LOGIN_ATTEMPTS', 5);
define('LOCKOUT_TIME', 900); // 15 minutes

// Start session
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

// Check if already logged in
if (isset($_SESSION['authenticated']) && $_SESSION['authenticated'] === true) {
    header('Location: index.php');
    exit;
}

// Check lockout
$lockoutFile = DATA_DIR . '/lockout.json';
if (file_exists($lockoutFile)) {
    $lockout = json_decode(file_get_contents($lockoutFile), true);
    if (isset($lockout['until']) && $lockout['until'] > time()) {
        $remaining = $lockout['until'] - time();
        $error = "Too many failed attempts. Please try again in {$remaining} seconds.";
    }
}

// Handle login
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = trim($_POST['username'] ?? '');
    $password = $_POST['password'] ?? '';
    
    if (empty($username) || empty($password)) {
        $error = 'Please enter both username and password.';
    } else {
        // Load users
        $usersFile = DATA_DIR . '/users.json';
        if (!file_exists($usersFile)) {
            $error = 'Authentication system not configured.';
        } else {
            $users = json_decode(file_get_contents($usersFile), true);
            $user = null;
            
            foreach ($users['users'] as $u) {
                if ($u['username'] === $username) {
                    $user = $u;
                    break;
                }
            }
            
            if (!$user) {
                $error = 'Invalid username or password.';
            } elseif (!password_verify($password, $user['password_hash'])) {
                $error = 'Invalid username or password.';
            } else {
                // Successful login
                session_regenerate_id(true);
                $_SESSION['authenticated'] = true;
                $_SESSION['username'] = $username;
                $_SESSION['user_name'] = $user['name'];
                $_SESSION['login_time'] = time();
                
                // Update last login
                $user['last_login'] = date('Y-m-d H:i:s');
                file_put_contents($usersFile, json_encode($users, JSON_PRETTY_PRINT));
                
                // Clear lockout
                if (file_exists($lockoutFile)) {
                    unlink($lockoutFile);
                }
                
                header('Location: index.php');
                exit;
            }
        }
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Hermes Dashboard</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --color-dark: #0f172a;
            --color-white: #ffffff;
            --color-orange: #f97316;
            --color-bg: #f8fafc;
            --color-muted: #64748b;
            --color-border: #e2e8f0;
            --color-danger: #ef4444;
            --color-success: #10b981;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--color-bg);
            color: var(--color-dark);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .login-container {
            width: 100%;
            max-width: 420px;
        }
        
        .login-header {
            text-align: center;
            margin-bottom: 32px;
        }
        
        .login-logo {
            font-size: 48px;
            margin-bottom: 16px;
        }
        
        .login-title {
            font-size: 28px;
            font-weight: 800;
            color: var(--color-dark);
            margin-bottom: 8px;
        }
        
        .login-subtitle {
            font-size: 14px;
            color: var(--color-muted);
        }
        
        .login-card {
            background: var(--color-white);
            border-radius: 16px;
            padding: 32px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-label {
            display: block;
            font-size: 14px;
            font-weight: 600;
            color: var(--color-dark);
            margin-bottom: 8px;
        }
        
        .form-input {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid var(--color-border);
            border-radius: 8px;
            font-size: 16px;
            font-family: inherit;
            transition: border-color 0.2s, box-shadow 0.2s;
        }
        
        .form-input:focus {
            outline: none;
            border-color: var(--color-orange);
            box-shadow: 0 0 0 3px rgba(249, 115, 22, 0.1);
        }
        
        .btn-login {
            width: 100%;
            padding: 14px 24px;
            background: var(--color-orange);
            color: var(--color-white);
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            font-family: inherit;
            cursor: pointer;
            transition: background 0.2s, transform 0.1s;
        }
        
        .btn-login:hover {
            background: #ea6c0a;
        }
        
        .btn-login:active {
            transform: scale(0.98);
        }
        
        .error-message {
            background: #fef2f2;
            border: 1px solid #fecaca;
            color: var(--color-danger);
            padding: 12px 16px;
            border-radius: 8px;
            font-size: 14px;
            margin-bottom: 20px;
        }
        
        .login-footer {
            text-align: center;
            margin-top: 24px;
            font-size: 13px;
            color: var(--color-muted);
        }
        
        .login-footer a {
            color: var(--color-orange);
            text-decoration: none;
        }
        
        .login-footer a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="login-header">
            <div class="login-logo">🤖</div>
            <h1 class="login-title">HERMES DASHBOARD</h1>
            <p class="login-subtitle">Multi-Agent System Control Panel</p>
        </div>
        
        <div class="login-card">
            <?php if (isset($error)): ?>
                <div class="error-message"><?= htmlspecialchars($error) ?></div>
            <?php endif; ?>
            
            <form method="POST" action="">
                <div class="form-group">
                    <label class="form-label" for="username">Username</label>
                    <input 
                        type="text" 
                        id="username" 
                        name="username" 
                        class="form-input" 
                        placeholder="Enter your username"
                        autofocus
                        autocomplete="username"
                    >
                </div>
                
                <div class="form-group">
                    <label class="form-label" for="password">Password</label>
                    <input 
                        type="password" 
                        id="password" 
                        name="password" 
                        class="form-input" 
                        placeholder="Enter your password"
                        autocomplete="current-password"
                    >
                </div>
                
                <button type="submit" class="btn-login">
                    Sign In
                </button>
            </form>
        </div>
        
        <div class="login-footer">
            <p>Hermes Agent System v1.0.0</p>
            <p style="margin-top: 8px;">
                <a href="https://github.com/labsdigital/hermes" target="_blank">
                    GitHub Repository
                </a>
            </p>
        </div>
    </div>
</body>
</html>
