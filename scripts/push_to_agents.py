#!/usr/bin/env python3
"""
Push Atlas articles to labsdigital/agents repo
Also updates index.html with new article links
Usage: python3 push_to_agents.py <filename>
"""
import subprocess
import sys
import os
import re
import json
from pathlib import Path

HERMES_REPO = "/opt/data/hermes"
AGENTS_CLONE = "/tmp/agents-clone"
AGENTS_REMOTE = "https://github.com/labsdigital/agents.git"
INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Atlas Essays - Labsdigital Agents</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            color: #e6e6e6;
            padding: 40px 20px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        header {
            text-align: center;
            margin-bottom: 50px;
            padding: 40px 20px;
            border-bottom: 2px solid #667eea;
        }
        header h1 {
            font-size: 2.5em;
            background: linear-gradient(90deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 15px;
        }
        header p {
            color: #8892b0;
            font-size: 1.1em;
        }
        .stats {
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 25px;
        }
        .stat-item {
            text-align: center;
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #64ffda;
        }
        .stat-label {
            font-size: 0.85em;
            color: #8892b0;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .article-list {
            display: grid;
            gap: 20px;
        }
        .article-card {
            background: rgba(22, 33, 62, 0.8);
            border-radius: 12px;
            padding: 25px;
            border: 1px solid rgba(102, 126, 234, 0.3);
            transition: transform 0.3s, box-shadow 0.3s;
            display: flex;
            gap: 20px;
            align-items: flex-start;
        }
        .article-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
            border-color: #667eea;
        }
        .article-number {
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2em;
            font-weight: bold;
            flex-shrink: 0;
        }
        .article-content {
            flex: 1;
        }
        .article-title {
            font-size: 1.3em;
            color: #fff;
            margin-bottom: 10px;
            text-decoration: none;
            display: block;
        }
        .article-title:hover {
            color: #64ffda;
        }
        .article-meta {
            font-size: 0.85em;
            color: #8892b0;
            margin-bottom: 10px;
        }
        .article-tags {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        .tag {
            background: rgba(102, 126, 234, 0.2);
            color: #667eea;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75em;
            text-transform: uppercase;
        }
        .article-links {
            display: flex;
            gap: 15px;
            margin-top: 15px;
        }
        .article-links a {
            color: #64ffda;
            text-decoration: none;
            font-size: 0.9em;
            padding: 8px 16px;
            border: 1px solid #64ffda;
            border-radius: 6px;
            transition: all 0.3s;
        }
        .article-links a:hover {
            background: #64ffda;
            color: #1a1a2e;
        }
        .footer {
            text-align: center;
            margin-top: 60px;
            padding-top: 30px;
            border-top: 1px solid rgba(255,255,255,0.1);
            color: #8892b0;
            font-size: 0.9em;
        }
        @media (max-width: 600px) {
            .article-card {
                flex-direction: column;
            }
            .stats {
                flex-direction: column;
                gap: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📚 Atlas Essays</h1>
            <p>Kumpulan Esai Non-Fiksi tentang AI, Teknologi & Masyarakat</p>
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-value" id="article-count">N</div>
                    <div class="stat-label">Artikel</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">AI</div>
                    <div class="stat-label">Tema Utama</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">2026</div>
                    <div class="stat-label">Tahun</div>
                </div>
            </div>
        </header>
        
        <div class="article-list" id="article-list">
            ARTICLES
        </div>
        
        <div class="footer">
            <p>Dibuat oleh <strong>Atlas</strong> - Agen Penulis Esai Non-Fiksi</p>
            <p style="margin-top: 10px;">Labsdigital Agents &copy; 2026</p>
        </div>
    </div>
    
    <script>
        const articles = ARTICLES_DATA;
        
        const container = document.getElementById('article-list');
        const countEl = document.getElementById('article-count');
        
        countEl.textContent = articles.length;
        
        articles.forEach(article => {
            const card = document.createElement('div');
            card.className = 'article-card';
            
            const tagsHtml = article.tags.map(tag => `<span class="tag">${tag}</span>`).join('');
            
            card.innerHTML = `
                <div class="article-number">${article.id}</div>
                <div class="article-content">
                    <a href="atlas/reports/${article.slug}.html" class="article-title">${article.title}</a>
                    <div class="article-meta">📅 ${article.date}</div>
                    <div class="article-tags">${tagsHtml}</div>
                    <div class="article-links">
                        <a href="atlas/reports/${article.slug}.html">📖 Baca HTML</a>
                        <a href="https://github.com/labsdigital/agents/blob/main/atlas/reports/${article.slug}.md" target="_blank">📝 Lihat MD</a>
                    </div>
                </div>
            `;
            
            container.appendChild(card);
        });
    </script>
</body>
</html>
"""


def get_article_slug(filename):
    """Extract slug from filename"""
    base = os.path.splitext(filename)[0]
    # Remove date suffix like -2026-08-28
    slug = re.sub(r'-\d{4}-\d{2}-\d{2}$', '', base)
    return slug


def extract_title_from_md(md_file):
    """Extract title from markdown file"""
    if os.path.exists(md_file):
        with open(md_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('# '):
                    return line[2:].strip()
    return "Untitled Article"


def get_existing_articles():
    """Get list of existing articles from agents clone"""
    articles = []
    reports_dir = os.path.join(AGENTS_CLONE, "atlas", "reports")
    
    if not os.path.exists(reports_dir):
        return articles
    
    # Find all .md files
    md_files = [f for f in os.listdir(reports_dir) if f.endswith('.md')]
    
    for md_file in sorted(md_files, reverse=True):
        base = os.path.splitext(md_file)[0]
        slug = get_article_slug(base)
        md_path = os.path.join(reports_dir, md_file)
        title = extract_title_from_md(md_path)
        
        # Extract date from filename
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', md_file)
        date = date_match.group(1).replace('-', ' ') if date_match else "2026"
        
        articles.append({
            'slug': slug,
            'title': title,
            'date': date,
            'tags': ['AI']
        })
    
    return articles


def generate_index_html(articles):
    """Generate index.html content"""
    articles_json = json.dumps(articles, ensure_ascii=False)
    html = INDEX_TEMPLATE.replace('ARTICLES_DATA', articles_json).replace('N', str(len(articles)))
    
    # Add article cards
    cards_html = ""
    for i, art in enumerate(articles, 1):
        tags_html = ' '.join([f'<span class="tag">{t}</span>' for t in art['tags']])
        cards_html += f'''
        <div class="article-card">
            <div class="article-number">{i}</div>
            <div class="article-content">
                <a href="atlas/reports/{art['slug']}.html" class="article-title">{art['title']}</a>
                <div class="article-meta">📅 {art['date']}</div>
                <div class="article-tags">{tags_html}</div>
                <div class="article-links">
                    <a href="atlas/reports/{art['slug']}.html">📖 Baca HTML</a>
                    <a href="https://github.com/labsdigital/agents/blob/main/atlas/reports/{art['slug']}.md" target="_blank">📝 Lihat MD</a>
                </div>
            </div>
        </div>'''
    
    html = html.replace('ARTICLES', cards_html)
    return html


def push_to_agents(filename):
    """Push file to agents repo and update index.html"""
    import json
    
    # Ensure agents clone exists
    if not os.path.exists(AGENTS_CLONE):
        subprocess.run(["git", "clone", AGENTS_REMOTE, AGENTS_CLONE], check=True)
    
    # Get base filename without extension
    base = os.path.splitext(filename)[0]
    slug = get_article_slug(base)
    
    # Copy all related files (MD, HTML, PNG, SVG)
    files_to_copy = [
        f"{base}.md",
        f"{base}.html",
        f"{base}-diagram.svg",
        f"{base}-artistik.png"
    ]
    
    copied = False
    for f in files_to_copy:
        src = os.path.join(HERMES_REPO, "atlas", "reports", f)
        dst = os.path.join(AGENTS_CLONE, "atlas", "reports", f)
        if os.path.exists(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            subprocess.run(["cp", src, dst], check=True)
            print(f"  📋 Copied: {f}")
            copied = True
    
    if not copied:
        print(f"  ⚠️ No files found to copy for {base}")
        return True
    
    # Commit and push
    subprocess.run(["git", "-C", AGENTS_CLONE, "add", "."], check=True)
    
    # Check if there are changes
    result = subprocess.run(["git", "-C", AGENTS_CLONE, "status", "--short"], capture_output=True, text=True)
    if result.stdout.strip():
        subprocess.run(["git", "-C", AGENTS_CLONE, "commit", "-m", f"Atlas: {base} - article + images"], check=True)
        subprocess.run(["git", "-C", AGENTS_CLONE, "push"], check=True)
        print(f"\n✅ Pushed article to: https://github.com/labsdigital/agents/tree/main/atlas/reports")
    else:
        print(f"\nℹ️  No changes to commit (files already up to date)")
    
    # Update index.html
    print("\n🔄 Updating index.html...")
    articles = get_existing_articles()
    
    # Add new article if not already present
    existing_slugs = [a['slug'] for a in articles]
    if slug not in existing_slugs:
        # Extract date from filename
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
        date = date_match.group(1).replace('-', ' ') if date_match else "2026"
        title = extract_title_from_md(os.path.join(HERMES_REPO, "atlas", "reports", f"{base}.md"))
        
        articles.insert(0, {
            'slug': slug,
            'title': title,
            'date': date,
            'tags': ['AI']
        })
    
    # Generate and save index.html
    index_content = generate_index_html(articles)
    index_path = os.path.join(AGENTS_CLONE, "index.html")
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    # Commit and push index.html
    subprocess.run(["git", "-C", AGENTS_CLONE, "add", "index.html"], check=True)
    result = subprocess.run(["git", "-C", AGENTS_CLONE, "diff", "--cached", "--quiet"], capture_output=True)
    if result.returncode != 0:
        subprocess.run(["git", "-C", AGENTS_CLONE, "commit", "-m", "Atlas: Update index.html with new article"], check=True)
        subprocess.run(["git", "-C", AGENTS_CLONE, "push"], check=True)
        print("✅ index.html updated")
    else:
        print("ℹ️  index.html already up to date")
    
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 push_to_agents.py <filename>")
        sys.exit(1)
    
    push_to_agents(sys.argv[1])
