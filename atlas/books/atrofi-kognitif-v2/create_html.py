#!/usr/bin/env python3
"""Convert Atrofi Kognitif V2 markdown chapters to single HTML book - Book Style."""

import re
from pathlib import Path

BASE_DIR = Path("/opt/data/hermes/atlas/books/atrofi-kognitif-v2")
CHAPTERS_DIR = BASE_DIR / "chapters"
OUTPUT_FILE = BASE_DIR / "atrofi-kognitif-v2.html"

chapters = []
for i in range(22):
    for f in sorted(CHAPTERS_DIR.glob(f"{i:02d}-*.md")):
        chapters.append(f)
        break

print(f"Found {len(chapters)} chapters")

chapter_meta = {
    "00": ("Pengantar", "Ketika Otak Lupa Cara Bekerja"),
    "01": ("Bab 1", "Kehilangan Pekerjaan"),
    "02": ("Bab 2", "Erosi Karier Pemula"),
    "03": ("Bab 3", "Oligarki Teknologi Baru"),
    "04": ("Bab 4", "Kolonialisme Digital"),
    "05": ("Bab 5", "Krisis Hak Cipta"),
    "06": ("Bab 6", "Atrofi Kognitif"),
    "07": ("Bab 7", "Hilangnya Productive Struggle"),
    "08": ("Bab 8", "Delusi Relasi Digital"),
    "09": ("Bab 9", "Tekanan Eksistensial"),
    "10": ("Bab 10", "Atrofi Moral"),
    "11": ("Bab 11", "Erosi Realitas"),
    "12": ("Bab 12", "Homogenisasi Budaya"),
    "13": ("Bab 13", "Polusi Informasi"),
    "14": ("Bab 14", "Komodifikasi Perhatian"),
    "15": ("Bab 15", "Disparitas Pendidikan"),
    "16": ("Bab 16", "Ketergantungan Infrastruktur"),
    "17": ("Bab 17", "Beban Lingkungan"),
    "18": ("Bab 18", "Kriminalitas Skala Industri"),
    "19": ("Bab 19", "Perang Otomatis"),
    "20": ("Bab 20", "Bioreaktor Digital"),
    "21": ("Epilog", "Manusia di Tengah Mesin"),
}

chapters_html = []
for f in chapters:
    content = f.read_text(encoding='utf-8')
    num = f.stem.split('-')[0]

    svg_blocks = re.findall(r'```svg\n(.*?)\n```', content, re.DOTALL)
    clean_content = re.sub(r'```svg\n.*?\n```', '', content, flags=re.DOTALL)
    clean_content = re.sub(r'^#\s+.+$\n', '', clean_content, count=1, flags=re.MULTILINE)
    clean_content = re.sub(r'^\*.*?\*\n', '', clean_content, count=1, flags=re.MULTILINE)
    clean_content = re.sub(r'^---\n', '', clean_content, count=1)

    clean_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', clean_content, flags=re.MULTILINE)
    clean_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', clean_content, flags=re.MULTILINE)
    clean_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', clean_content)
    clean_content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', clean_content)
    clean_content = re.sub(r'\n\n(.+?)\n\n', r'<p>\1</p>\n\n', clean_content)
    clean_content = re.sub(r'^-\s+(.+)$', r'<li>\1</li>', clean_content, flags=re.MULTILINE)
    clean_content = re.sub(r'^\d+\.\s+(.+)$', r'<li>\1</li>', clean_content, flags=re.MULTILINE)
    clean_content = re.sub(r'^>\s+(.+)$', r'<blockquote>\1</blockquote>', clean_content, flags=re.MULTILINE)
    clean_content = re.sub(r'^---$', '<hr>', clean_content, flags=re.MULTILINE)
    clean_content = re.sub(r'<p></p>', '', clean_content)
    clean_content = clean_content.strip()

    for idx, svg in enumerate(svg_blocks):
        svg_container = f'<div class="figure">{svg}<figcaption>Ilustrasi</figcaption></div>'
        if idx == 0:
            clean_content = svg_container + clean_content

    title_num, title_text = chapter_meta.get(num, (f"Bab {num}", ""))
    chapter_html = f'''
    <section class="chapter" id="{num}">
      <header class="chapter-header">
        <span class="chapter-number">{title_num}</span>
        <h1>{title_text}</h1>
      </header>
      <div class="chapter-body">
        {clean_content}
      </div>
    </section>
    '''
    chapters_html.append(chapter_html)

toc_items = []
for i in range(22):
    num = f"{i:02d}"
    title_num, title_text = chapter_meta.get(num, (f"Bab {i}", ""))
    toc_items.append(f'<li><a href="#{num}"><span class="toc-num">{title_num}</span> {title_text}</a></li>')

toc_html = '\n'.join(toc_items)

css = r"""
    :root {
      --bg: #faf9f7;
      --surface: #ffffff;
      --text: #1a1a1a;
      --text-muted: #6b7280;
      --accent: #c2410c;
      --accent-light: #fff7ed;
      --border: #e5e5e5;
      --sidebar-w: 280px;
      --font-serif: 'Georgia', 'Times New Roman', serif;
      --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; scroll-padding-top: 80px; }
    body {
      font-family: var(--font-serif);
      background: var(--bg);
      color: var(--text);
      line-height: 1.8;
      font-size: 17px;
    }
    .sidebar {
      position: fixed;
      top: 0; left: 0;
      width: var(--sidebar-w);
      height: 100vh;
      background: var(--surface);
      border-right: 1px solid var(--border);
      overflow-y: auto;
      z-index: 100;
      transition: transform 0.3s ease;
    }
    .sidebar-header {
      padding: 24px 20px;
      border-bottom: 1px solid var(--border);
      position: sticky;
      top: 0;
      background: var(--surface);
      z-index: 10;
    }
    .sidebar-header h2 {
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.15em;
      color: var(--text-muted);
      font-family: var(--font-sans);
      margin-bottom: 6px;
    }
    .sidebar-header .book-title {
      font-size: 17px;
      font-weight: normal;
      color: var(--text);
    }
    .toc { list-style: none; padding: 12px 0; }
    .toc li { border-bottom: 1px solid #f5f5f5; }
    .toc a {
      display: flex;
      align-items: baseline;
      gap: 10px;
      padding: 11px 20px;
      text-decoration: none;
      color: var(--text-muted);
      font-family: var(--font-sans);
      font-size: 13px;
      transition: all 0.2s;
    }
    .toc a:hover, .toc a.active {
      color: var(--accent);
      background: var(--accent-light);
    }
    .toc .toc-num {
      font-weight: 600;
      min-width: 50px;
      color: var(--accent);
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .main { margin-left: var(--sidebar-w); min-height: 100vh; }
    .cover {
      background: linear-gradient(160deg, #1e293b 0%, #334155 50%, #475569 100%);
      color: white;
      padding: 80px 60px;
      text-align: center;
    }
    .cover img {
      max-width: 280px;
      width: 100%;
      border-radius: 8px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.4);
      margin-bottom: 40px;
    }
    .cover h1 {
      font-size: 3.2em;
      font-weight: normal;
      letter-spacing: 0.08em;
      margin-bottom: 16px;
      line-height: 1.1;
    }
    .cover .subtitle {
      font-size: 1.15em;
      opacity: 0.85;
      font-style: italic;
      margin-bottom: 40px;
      max-width: 500px;
      margin-left: auto;
      margin-right: auto;
      line-height: 1.6;
    }
    .cover .author {
      font-family: var(--font-sans);
      font-size: 0.85em;
      opacity: 0.7;
      margin-top: 40px;
      letter-spacing: 0.05em;
    }
    .chapter {
      max-width: 680px;
      margin: 0 auto;
      padding: 60px 40px;
      border-bottom: 1px solid var(--border);
    }
    .chapter:last-child { border-bottom: none; }
    .chapter-header {
      margin-bottom: 40px;
      padding-bottom: 20px;
      border-bottom: 2px solid var(--accent);
    }
    .chapter-number {
      font-family: var(--font-sans);
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.15em;
      color: var(--accent);
      font-weight: 600;
      display: block;
      margin-bottom: 8px;
    }
    .chapter h1 {
      font-size: 2.2em;
      font-weight: normal;
      line-height: 1.2;
      color: var(--text);
      margin: 0;
    }
    .chapter-body h2 {
      font-size: 1.4em;
      font-weight: normal;
      margin-top: 48px;
      margin-bottom: 20px;
      color: var(--text);
      line-height: 1.3;
    }
    .chapter-body h3 {
      font-size: 1.15em;
      font-weight: 600;
      margin-top: 36px;
      margin-bottom: 16px;
      color: var(--text);
    }
    .chapter-body p { margin-bottom: 20px; text-align: justify; hyphens: auto; }
    .chapter-body strong { font-weight: 600; }
    .chapter-body em { font-style: italic; }
    .figure { margin: 40px 0; text-align: center; }
    .figure svg, .figure img { max-width: 100%; height: auto; border-radius: 6px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
    .figure figcaption {
      font-family: var(--font-sans);
      font-size: 0.82em;
      color: var(--text-muted);
      margin-top: 12px;
      font-style: italic;
    }
    .chapter-body blockquote {
      border-left: 3px solid var(--accent);
      padding-left: 20px;
      margin: 30px 0;
      font-style: italic;
      color: var(--text-muted);
    }
    .quote-box {
      background: var(--accent-light);
      border: 1px solid #fed7aa;
      padding: 24px;
      margin: 40px 0;
      border-radius: 8px;
    }
    .quote-box p { font-style: italic; color: #78350f; margin: 0; text-align: left; }
    .chapter-body ul, .chapter-body ol { margin: 20px 0; padding-left: 24px; }
    .chapter-body li { margin-bottom: 8px; }
    hr { border: none; height: 1px; background: var(--border); margin: 40px 0; }
    .menu-toggle {
      display: none;
      position: fixed;
      top: 16px; left: 16px;
      z-index: 200;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 10px 14px;
      cursor: pointer;
      font-size: 18px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .overlay {
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.5);
      z-index: 90;
    }
    @media (max-width: 900px) {
      .sidebar { transform: translateX(-100%); }
      .sidebar.open { transform: translateX(0); }
      .main { margin-left: 0; }
      .menu-toggle { display: block; }
      .overlay.open { display: block; }
      .cover { padding: 60px 24px; }
      .cover h1 { font-size: 2.2em; }
      .chapter { padding: 40px 24px; }
      .chapter h1 { font-size: 1.6em; }
    }
    @media print {
      .sidebar, .menu-toggle { display: none; }
      .main { margin-left: 0; }
      .chapter { page-break-before: always; }
      .cover { page-break-after: always; }
    }
    .sidebar::-webkit-scrollbar { width: 4px; }
    .sidebar::-webkit-scrollbar-track { background: transparent; }
    .sidebar::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
"""

js = r"""
    function toggleMenu() {
      document.getElementById('sidebar').classList.toggle('open');
      document.getElementById('overlay').classList.toggle('open');
    }
    const chapters = document.querySelectorAll('.chapter');
    const tocLinks = document.querySelectorAll('.toc a');
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const id = entry.target.id;
          tocLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + id) {
              link.classList.add('active');
            }
          });
        }
      });
    }, { rootMargin: '-20% 0px -80% 0px' });
    chapters.forEach(ch => observer.observe(ch));
"""

html_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Atrofi Kognitif &mdash; Atlas</title>
  <style>{css}</style>
</head>
<body>
  <button class="menu-toggle" onclick="toggleMenu()" aria-label="Toggle menu">&#9776;</button>
  <div class="overlay" id="overlay" onclick="toggleMenu()"></div>

  <aside class="sidebar" id="sidebar">
    <div class="sidebar-header">
      <h2>Daftar Isi</h2>
      <div class="book-title">Atrofi Kognitif</div>
    </div>
    <nav>
      <ul class="toc">
{toc_html}
      </ul>
    </nav>
  </aside>

  <main class="main">
    <div class="cover">
      <img src="cover-art.png" alt="Ilustrasi Cover Atrofi Kognitif">
      <h1>ATROFI KOGNITIF</h1>
      <p class="subtitle">Dampak AI pada Manusia, Masyarakat, dan Masa Depan Kemanusiaan</p>
      <p class="author">oleh Atlas &middot; Agustus 2026</p>
    </div>

{"".join(chapters_html)}
    <footer style="padding: 60px 40px; text-align: center; color: var(--text-muted); font-family: var(--font-sans); font-size: 0.85em; border-top: 1px solid var(--border);">
      <p>&copy; 2026 Atlas &middot; labsdigital</p>
      <p style="margin-top: 8px;"><a href="https://github.com/labsdigital/hermes" style="color: var(--accent); text-decoration: none;">GitHub Repository</a></p>
    </footer>
  </main>

  <script>{js}</script>
</body>
</html>
"""

OUTPUT_FILE.write_text(html_content, encoding='utf-8')
print(f"OK: {OUTPUT_FILE}")
print(f"Size: {OUTPUT_FILE.stat().st_size / 1024:.1f} KB")
