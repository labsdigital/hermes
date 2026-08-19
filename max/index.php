<?php
/**
 * Max Articles Blog - Reader dari Airtable
 * Modern Minimalist Blog Style
 * Sorted by published_at (newest first)
 */

// Konfigurasi
$AIRTABLE_API_KEY = getenv('AIRTABLE_API_KEY') ?: (file_exists(__DIR__ . '/../.env') ? parse_env_file(__DIR__ . '/../.env')['AIRTABLE_API_KEY'] : '');
$AIRTABLE_BASE_ID = 'appHDwcERrnRH02YS';
$AIRTABLE_TABLE_ID = 'tbl9TvJ9QztbHeyaY';

function parse_env_file($path) {
    $vars = [];
    if (file_exists($path)) {
        foreach (file($path) as $line) {
            $line = trim($line);
            if ($line && !str_starts_with($line, '#')) {
                if (strpos($line, '=') !== false) {
                    [$key, $value] = explode('=', $line, 2);
                    $vars[trim($key)] = trim($value, "'\"");
                }
            }
        }
    }
    return $vars;
}

function fetchArticles() {
    global $AIRTABLE_API_KEY, $AIRTABLE_BASE_ID, $AIRTABLE_TABLE_ID;
    
    if (!$AIRTABLE_API_KEY) {
        return ['error' => 'Airtable API key tidak dikonfigurasi'];
    }
    
    // Sort by published_at descending, then createdTime
    $url = "https://api.airtable.com/v0/{$AIRTABLE_BASE_ID}/{$AIRTABLE_TABLE_ID}"
         . "?maxRecords=50"
         . "&sort[]=fieldName&sort[0]=published_at&sort[1]=desc"
         . "&filterByFormula=RECORD_ID()<>''";
    
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        "Authorization: Bearer {$AIRTABLE_API_KEY}",
        "Content-Type: application/json"
    ]);
    curl_setopt($ch, CURLOPT_TIMEOUT, 10);
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    if ($httpCode !== 200 || !$response) {
        // Fallback: fetch without sort
        $url = "https://api.airtable.com/v0/{$AIRTABLE_BASE_ID}/{$AIRTABLE_TABLE_ID}?maxRecords=50";
        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            "Authorization: Bearer {$AIRTABLE_API_KEY}",
            "Content-Type: application/json"
        ]);
        curl_setopt($ch, CURLOPT_TIMEOUT, 10);
        $response = curl_exec($ch);
        curl_close($ch);
    }
    
    if (!$response) {
        return ['error' => 'Gagal mengambil data dari Airtable'];
    }
    
    $data = json_decode($response, true);
    $records = $data['records'] ?? [];
    
    // Sort by date (published_at > ID date > createdTime), newest first
    usort($records, function($a, $b) {
        // Get date from published_at field
        $dateA = $a['fields']['published_at'] ?? null;
        $dateB = $b['fields']['published_at'] ?? null;
        
        // If not available, extract from ID
        if (!$dateA) {
            $idA = $a['fields']['id'] ?? '';
            preg_match('/(\d{4}-\d{2}-\d{2})/', $idA, $m);
            $dateA = $m[1] ?? $a['createdTime'];
        }
        if (!$dateB) {
            $idB = $b['fields']['id'] ?? '';
            preg_match('/(\d{4}-\d{2}-\d{2})/', $idB, $m);
            $dateB = $m[1] ?? $b['createdTime'];
        }
        
        return strtotime($dateB) - strtotime($dateA);
    });
    
    return $records;
}

function mdToHtml($md) {
    if (!$md) return '';
    
    $md = htmlspecialchars($md, ENT_QUOTES, 'UTF-8');
    
    $md = preg_replace('/^### (.+)$/m', '<h3>$1</h3>', $md);
    $md = preg_replace('/^## (.+)$/m', '<h2>$1</h2>', $md);
    $md = preg_replace('/^# (.+)$/m', '<h1>$1</h1>', $md);
    
    $md = preg_replace('/\*\*(.+?)\*\*/', '<strong>$1</strong>', $md);
    $md = preg_replace('/\*(.+?)\*/', '<em>$1</em>', $md);
    
    $md = preg_replace('/\[([^\]]+)\]\(([^)]+)\)/', '<a href="$2">$1</a>', $md);
    
    $md = preg_replace('/```(\w+)?\n([\s\S]*?)```/', '<pre><code>$2</code></pre>', $md);
    $md = preg_replace('/`([^`]+)`/', '<code>$1</code>', $md);
    
    $md = preg_replace('/^\> (.+)$/m', '<blockquote>$1</blockquote>', $md);
    $md = preg_replace('/^---$/m', '<hr>', $md);
    
    $md = preg_replace('/^- (.+)$/m', '<li>$1</li>', $md);
    $md = preg_replace('/(<li>.*<\/li>\n?)+/', '<ul>$0</ul>', $md);
    
    $md = preg_replace('/\n\n/', '</p><p>', $md);
    $md = preg_replace('/\n/', '<br>', $md);
    
    if (!preg_match('/^<[\w]/', $md)) {
        $md = '<p>' . $md . '</p>';
    }
    
    return $md;
}

function extractTitle($content) {
    if (!$content) return 'Untitled';
    $lines = explode("\n", $content);
    foreach ($lines as $line) {
        if (preg_match('/^# (.+)$/', trim($line), $matches)) {
            return html_entity_decode($matches[1]);
        }
    }
    return substr(html_entity_decode($lines[0]), 0, 60) . '...';
}

function extractDate($record) {
    // Try published_at field first
    $published = $record['fields']['published_at'] ?? '';
    if ($published) {
        return date('d M Y', strtotime($published));
    }
    
    // Fallback: extract from ID (format: max-article-name-YYYY-MM-DD)
    $id = $record['fields']['id'] ?? '';
    $match = preg_match('/(\d{4}-\d{2}-\d{2})/', $id, $matches);
    if ($match) {
        return date('d M Y', strtotime($matches[1]));
    }
    
    // Last resort: use createdTime
    return date('d M Y', strtotime($record['createdTime']));
}

function getReadingTime($content) {
    return max(1, round(strlen($content) / 500));
}

function getExcerpt($content, $len = 150) {
    $text = preg_replace('/^#+.+/m', '', $content);
    $text = strip_tags($text);
    return mb_substr($text, 0, $len) . (mb_strlen($text) > $len ? '...' : '');
}

$articles = fetchArticles();

$articleId = $_GET['id'] ?? null;
$currentArticle = null;
if ($articleId) {
    foreach ($articles as $article) {
        if ($article['id'] === $articleId) {
            $currentArticle = $article;
            break;
        }
    }
}
?>
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Max Articles Blog</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #fafafa;
            --surface: #ffffff;
            --text: #1a1a1a;
            --text-muted: #6b7280;
            --accent: #2563eb;
            --accent-light: #3b82f6;
            --border: #e5e7eb;
            --shadow: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06);
            --shadow-lg: 0 10px 25px rgba(0,0,0,0.08);
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.7;
            min-height: 100vh;
        }
        
        header {
            background: var(--surface);
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .header-inner {
            max-width: 1200px;
            margin: 0 auto;
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            font-family: 'Playfair Display', serif;
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--text);
            text-decoration: none;
            letter-spacing: -0.5px;
        }
        
        .logo span { color: var(--accent); }
        
        nav a {
            color: var(--text-muted);
            text-decoration: none;
            font-size: 0.875rem;
            font-weight: 500;
            margin-left: 2rem;
            transition: color 0.2s;
        }
        
        nav a:hover { color: var(--accent); }
        
        main {
            max-width: 1200px;
            margin: 0 auto;
            padding: 3rem 2rem;
        }
        
        .hero {
            text-align: center;
            padding: 4rem 0;
            margin-bottom: 3rem;
            border-bottom: 1px solid var(--border);
        }
        
        .hero h1 {
            font-family: 'Playfair Display', serif;
            font-size: 3rem;
            font-weight: 600;
            margin-bottom: 1rem;
            letter-spacing: -1px;
        }
        
        .hero p {
            color: var(--text-muted);
            font-size: 1.125rem;
            max-width: 600px;
            margin: 0 auto;
        }
        
        .articles-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
            gap: 2rem;
        }
        
        .article-card {
            background: var(--surface);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: var(--shadow);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            cursor: pointer;
            text-decoration: none;
            color: inherit;
            display: block;
        }
        
        .article-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-lg);
        }
        
        /* Prevent any link styling inside card */
        .article-card a,
        .article-card h2,
        .article-card h3,
        .article-card p,
        .article-card span {
            text-decoration: none;
            color: inherit;
        }
        
        .card-accent {
            height: 4px;
            background: linear-gradient(90deg, var(--accent), var(--accent-light));
        }
        
        .card-body {
            padding: 1.5rem;
        }
        
        .card-meta {
            display: flex;
            gap: 1rem;
            font-size: 0.75rem;
            color: var(--text-muted);
            margin-bottom: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 500;
        }
        
        .card-title {
            font-family: 'Playfair Display', serif;
            font-size: 1.375rem;
            font-weight: 600;
            line-height: 1.3;
            margin-bottom: 0.75rem;
            letter-spacing: -0.3px;
            color: var(--text);
        }
        
        /* Prevent title from changing on hover */
        .article-card:hover .card-title {
            color: var(--text) !important;
            text-decoration: none !important;
        }

        /* Override any link styles inside card */
        .article-card h2,
        .article-card h3,
        .article-card p,
        .article-card span {
            color: inherit;
        }
        
        .card-excerpt {
            color: var(--text-muted);
            font-size: 0.9375rem;
            line-height: 1.6;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        
        .card-footer {
            padding: 1rem 1.5rem;
            border-top: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.875rem;
            color: var(--text-muted);
        }
        
        .read-more {
            color: var(--accent);
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }
        
        .read-more::after {
            content: '→';
            transition: transform 0.2s;
        }
        
        .article-card:hover .read-more::after {
            transform: translateX(4px);
        }
        
        .article-view {
            max-width: 760px;
            margin: 0 auto;
        }
        
        .article-header {
            margin-bottom: 2.5rem;
            padding-bottom: 2rem;
            border-bottom: 1px solid var(--border);
        }
        
        .article-header .card-meta {
            margin-bottom: 1rem;
        }
        
        .article-header h1 {
            font-family: 'Playfair Display', serif;
            font-size: 2.5rem;
            font-weight: 600;
            line-height: 1.2;
            letter-spacing: -1px;
            margin-bottom: 1rem;
        }
        
        .back-link {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--text-muted);
            text-decoration: none;
            font-size: 0.875rem;
            margin-bottom: 2rem;
            transition: color 0.2s;
        }
        
        .back-link:hover { color: var(--accent); }
        
        .article-content {
            font-size: 1.0625rem;
            line-height: 1.8;
        }
        
        .article-content h1,
        .article-content h2,
        .article-content h3 {
            font-family: 'Playfair Display', serif;
            margin-top: 2.5rem;
            margin-bottom: 1rem;
            letter-spacing: -0.3px;
        }
        
        .article-content h1 { font-size: 1.75rem; }
        .article-content h2 { font-size: 1.5rem; }
        .article-content h3 { font-size: 1.25rem; }
        
        .article-content p { margin-bottom: 1.25rem; }
        
        .article-content ul,
        .article-content ol {
            margin-bottom: 1.25rem;
            padding-left: 1.5rem;
        }
        
        .article-content li { margin-bottom: 0.5rem; }
        
        .article-content blockquote {
            border-left: 3px solid var(--accent);
            padding-left: 1.25rem;
            margin: 1.5rem 0;
            color: var(--text-muted);
            font-style: italic;
        }
        
        .article-content code {
            background: var(--bg);
            padding: 0.2em 0.4em;
            border-radius: 4px;
            font-size: 0.9em;
        }
        
        .article-content pre {
            background: var(--bg);
            padding: 1.25rem;
            border-radius: 8px;
            overflow-x: auto;
            margin: 1.5rem 0;
        }
        
        .article-content pre code {
            background: none;
            padding: 0;
        }
        
        .article-content hr {
            border: none;
            border-top: 1px solid var(--border);
            margin: 2rem 0;
        }
        
        .article-content strong { color: var(--text); }
        .article-content em { color: var(--text-muted); }
        
        .article-content a {
            color: var(--accent);
            text-decoration: none;
        }
        
        .article-content a:hover { text-decoration: underline; }
        
        .state-message {
            text-align: center;
            padding: 4rem 2rem;
            color: var(--text-muted);
        }
        
        .state-message svg {
            width: 48px;
            height: 48px;
            margin-bottom: 1rem;
            opacity: 0.5;
        }
        
        footer {
            border-top: 1px solid var(--border);
            padding: 2rem;
            text-align: center;
            color: var(--text-muted);
            font-size: 0.875rem;
            margin-top: 4rem;
        }
        
        footer a { color: var(--accent); text-decoration: none; }
        
        @media (max-width: 768px) {
            .header-inner { padding: 1rem; }
            main { padding: 2rem 1rem; }
            .hero h1 { font-size: 2rem; }
            .articles-grid { grid-template-columns: 1fr; }
            .article-header h1 { font-size: 1.75rem; }
        }
    </style>
</head>
<body>
    <header>
        <div class="header-inner">
            <a href="index.php" class="logo">Max<span>Articles</span></a>
            <nav>
                <a href="index.php">Semua</a>
                <a href="https://github.com/labsdigital/hermes" target="_blank">GitHub</a>
            </nav>
        </div>
    </header>

    <main>
        <?php if ($currentArticle): ?>
            <article class="article-view">
                <a href="index.php" class="back-link">← Kembali ke semua artikel</a>
                
                <header class="article-header">
                    <div class="card-meta">
                        <span><?php echo extractDate($currentArticle); ?></span>
                        <span><?php echo getReadingTime($currentArticle['fields']['content'] ?? ''); ?> min read</span>
                    </div>
                    <h1><?php echo extractTitle($currentArticle['fields']['content'] ?? ''); ?></h1>
                </header>
                
                <div class="article-content">
                    <?php echo mdToHtml($currentArticle['fields']['content'] ?? ''); ?>
                </div>
            </article>
        <?php else: ?>
            <section class="hero">
                <h1>Koleksi Artikel</h1>
                <p>Kumpulan tulisan dari subagent Max tentang AI, teknologi, dan masa depan</p>
            </section>
            
            <?php if (isset($articles['error'])): ?>
                <div class="state-message">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                    </svg>
                    <p><?php echo $articles['error']; ?></p>
                </div>
            <?php elseif (empty($articles)): ?>
                <div class="state-message">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                    </svg>
                    <p>Belum ada artikel</p>
                </div>
            <?php else: ?>
                <div class="articles-grid">
                    <?php foreach ($articles as $article): 
                        $title = extractTitle($article['fields']['content'] ?? '');
                        $date = extractDate($article);
                        $content = $article['fields']['content'] ?? '';
                        $excerpt = getExcerpt($content);
                        $readTime = getReadingTime($content);
                    ?>
                        <a href="index.php?id=<?php echo $article['id']; ?>" class="article-card">
                            <div class="card-accent"></div>
                            <div class="card-body">
                                <div class="card-meta">
                                    <span><?php echo $date; ?></span>
                                    <span><?php echo $readTime; ?> min</span>
                                </div>
                                <h2 class="card-title"><?php echo htmlspecialchars($title); ?></h2>
                                <p class="card-excerpt"><?php echo htmlspecialchars($excerpt); ?></p>
                            </div>
                            <div class="card-footer">
                                <span>Baca selengkapnya</span>
                                <span class="read-more">Baca</span>
                            </div>
                        </a>
                    <?php endforeach; ?>
                </div>
            <?php endif; ?>
        <?php endif; ?>
    </main>

    <footer>
        <p>Max Articles Blog &copy; 2026 | Data dari <a href="https://airtable.com/appHDwcERrnRH02YS/tbl9TvJ9QztbHeyaY" target="_blank">Airtable</a> | <a href="https://github.com/labsdigital/hermes" target="_blank">GitHub</a></p>
    </footer>
</body>
</html>
