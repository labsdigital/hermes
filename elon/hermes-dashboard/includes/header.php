<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= $pageTitle ?? 'Dashboard' ?> - Hermes</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="assets/css/styles.css">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🤖</text></svg>">
</head>
<body>
    <header class="header">
        <div class="header-logo">
            <span>🤖</span>
            <span class="header-title">HERMES DASHBOARD</span>
        </div>
        <div class="header-user">
            <span class="header-username">Welcome, <?= htmlspecialchars($user['name'] ?? 'User') ?></span>
            <a href="logout.php" class="btn-logout">Logout</a>
        </div>
    </header>
