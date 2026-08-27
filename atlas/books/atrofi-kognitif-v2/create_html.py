#!/usr/bin/env python3
"""Convert Atrofi Kognitif V2 markdown chapters to single HTML book."""

import os
import re
from pathlib import Path

BASE_DIR = Path("/opt/data/hermes/atlas/books/atrofi-kognitif-v2")
CHAPTERS_DIR = BASE_DIR / "chapters"
OUTPUT_FILE = BASE_DIR / "atrofi-kognitif-v2.html"

# Read all chapters
chapters = []
for i in range(22):  # 00-21
    filename = f"{i:02d}-*.md"
    for f in sorted(CHAPTERS_DIR.glob(filename)):
        chapters.append(f)
        break

print(f"Found {len(chapters)} chapters")

# HTML template
html_template = """<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Atrofi Kognitif - Dampak AI pada Manusia, Masyarakat, dan Masa Depan Kemanusiaan</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            line-height: 1.8;
            color: #1e293b;
            background: #fafafa;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }
        
        /* Cover */
        .cover {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            color: white;
            padding: 100px 40px;
            text-align: center;
        }
        
        .cover h1 {
            font-size: 3em;
            margin-bottom: 20px;
            font-weight: normal;
            letter-spacing: 2px;
        }
        
        .cover .subtitle {
            font-size: 1.2em;
            opacity: 0.9;
            margin-bottom: 40px;
            font-style: italic;
        }
        
        .cover .author {
            font-size: 1.1em;
            margin-top: 60px;
            opacity: 0.8;
        }
        
        /* Table of Contents */
        .toc {
            padding: 60px 40px;
            background: #f8fafc;
            border-bottom: 1px solid #e2e8f0;
        }
        
        .toc h2 {
            font-size: 1.8em;
            margin-bottom: 30px;
            color: #1e293b;
            text-align: center;
        }
        
        .toc ul {
            list-style: none;
            max-width: 600px;
            margin: 0 auto;
        }
        
        .toc li {
            padding: 12px 0;
            border-bottom: 1px solid #e2e8f0;
        }
        
        .toc a {
            color: #475569;
            text-decoration: none;
            display: flex;
            justify-content: space-between;
        }
        
        .toc a:hover {
            color: #1e40af;
        }
        
        .toc .chapter-num {
            color: #94a3b8;
            font-size: 0.9em;
        }
        
        /* Chapters */
        .chapter {
            padding: 60px 40px;
            border-bottom: 1px solid #e2e8f0;
        }
        
        .chapter:last-child {
            border-bottom: none;
        }
        
        .chapter h1 {
            font-size: 2em;
            margin-bottom: 10px;
            color: #1e293b;
            font-weight: normal;
        }
        
        .chapter .chapter-meta {
            font-size: 0.9em;
            color: #64748b;
            margin-bottom: 30px;
            font-style: italic;
        }
        
        .chapter h2 {
            font-size: 1.4em;
            margin-top: 40px;
            margin-bottom: 20px;
            color: #334155;
        }
        
        .chapter h3 {
            font-size: 1.2em;
            margin-top: 30px;
            margin-bottom: 15px;
            color: #475569;
        }
        
        .chapter p {
            margin-bottom: 20px;
            text-align: justify;
        }
        
        .chapter blockquote {
            border-left: 4px solid #f97316;
            padding-left: 20px;
            margin: 30px 0;
            font-style: italic;
            color: #475569;
        }
        
        .chapter strong {
            color: #1e293b;
        }
        
        /* SVG containers */
        .svg-container {
            margin: 40px 0;
            text-align: center;
        }
        
        .svg-container svg {
            max-width: 100%;
            height: auto;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border-radius: 8px;
        }
        
        /* Quote box */
        .quote-box {
            background: #fff7ed;
            border: 1px solid #fed7aa;
            padding: 25px;
            margin: 40px 0;
            border-radius: 8px;
        }
        
        .quote-box p {
            font-style: italic;
            color: #78350f;
            margin: 0;
        }
        
        /* Navigation */
        .nav {
            padding: 40px;
            text-align: center;
            background: #f8fafc;
            border-top: 1px solid #e2e8f0;
        }
        
        .nav a {
            color: #3b82f6;
            text-decoration: none;
            margin: 0 20px;
            padding: 10px 20px;
            border: 1px solid #3b82f6;
            border-radius: 5px;
        }
        
        .nav a:hover {
            background: #3b82f6;
            color: white;
        }
        
        /* Print styles */
        @media print {
            .cover {
                page-break-after: always;
            }
            .chapter {
                page-break-before: always;
            }
        }
        
        /* Responsive */
        @media (max-width: 600px) {
            .cover h1 {
                font-size: 2em;
            }
            .chapter {
                padding: 40px 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Cover -->
        <div class="cover">
            <h1>ATROFI KOGNITIF</h1>
            <p class="subtitle">Dampak AI pada Manusia, Masyarakat, dan Masa Depan Kemanusiaan</p>
            <p class="author">oleh Atlas<br>Agustus 2026</p>
        </div>
        
        <!-- Table of Contents -->
        <div class="toc">
            <h2>Daftar Isi</h2>
            <ul>
"""

# Build TOC
chapter_titles = {
    "00": "Pengantar: Ketika Otak Lupa Cara Bekerja",
    "01": "Kehilangan Pekerjaan (Job Loss)",
    "02": "Erosi Karier Pemula",
    "03": "Oligarki Teknologi Baru",
    "04": "Kolonialisme Digital",
    "05": "Krisis Hak Cipta",
    "06": "Atrofi Kognitif (Eskalator Kognitif)",
    "07": "Hilangnya Productive Struggle",
    "08": "Delusi Relasi Digital",
    "09": "Tekanan Eksistensial (AI Anxiety)",
    "10": "Atrofi Moral",
    "11": "Erosi Realitas (Krisis Epistemik)",
    "12": "Homogenisasi Budaya",
    "13": "Polusi Informasi (Model Collapse)",
    "14": "Komodifikasi Perhatian (Hiper-Silo)",
    "15": "Disparitas Pendidikan",
    "16": "Ketergantungan Infrastruktur Global",
    "17": "Beban Lingkungan Ekstrem",
    "18": "Kriminalitas Skala Industri",
    "19": "Perang Otomatis (Senjata Otonom)",
    "20": "Bioreaktor Digital",
    "21": "Epilog: Manusia di Tengah Mesin"
}

toc_items = []
for i in range(22):
    num = f"{i:02d}"
    title = chapter_titles.get(num, f"Bab {i}")
    toc_items.append(f'                <li><a href="#chapter-{num}"><span>{title}</span><span class="chapter-num">Bab {i}</span></a></li>')

toc_html = '\n'.join(toc_items)

html_after_toc = """
            </ul>
        </div>
        
        <!-- Chapters will be inserted here -->
"""

# Process each chapter
chapters_html = []
for f in chapters:
    content = f.read_text(encoding='utf-8')
    num = f.stem.split('-')[0]
    
    # Extract title from first line
    title_match = re.search(r'#\s+(.+)', content)
    title = title_match.group(1) if title_match else f"Bab {num}"
    
    # Extract SVG content
    svg_blocks = re.findall(r'```svg\n(.*?)\n```', content, re.DOTALL)
    
    # Remove markdown code blocks containing SVGs
    clean_content = re.sub(r'```svg\n.*?\n```', '', content, flags=re.DOTALL)
    
    # Convert markdown to HTML
    # Headers
    clean_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', clean_content, flags=re.MULTILINE)
    clean_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', clean_content, flags=re.MULTILINE)
    
    # Bold
    clean_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', clean_content)
    
    # Italic
    clean_content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', clean_content)
    
    # Paragraphs
    clean_content = re.sub(r'\n\n(.+?)\n\n', r'<p>\1</p>\n\n', clean_content)
    
    # Handle SVGs - insert after extraction
    for idx, svg in enumerate(svg_blocks):
        svg_container = f'<div class="svg-container">{svg}</div>'
        # Insert at beginning of content after title
        if idx == 0:
            clean_content = svg_container + clean_content
    
    # Clean up empty paragraphs
    clean_content = re.sub(r'<p></p>', '', clean_content)
    clean_content = clean_content.strip()
    
    if not clean_content:
        clean_content = "<p>...</p>"
    
    chapter_html = f'''
        <!-- Chapter {num} -->
        <div class="chapter" id="chapter-{num}">
            <h1>{title}</h1>
            <p class="chapter-meta">Esai Non-Fiksi | Agustus 2026</p>
            {clean_content}
        </div>
    '''
    chapters_html.append(chapter_html)

# Combine all
full_html = html_template + toc_html + html_after_toc + '\n'.join(chapters_html) + """
        <!-- Navigation -->
        <div class="nav">
            <a href="#chapter-00">← Pengantar</a>
            <a href="#chapter-21">Epilog →</a>
        </div>
        
        <!-- Footer -->
        <div style="padding: 40px; text-align: center; color: #94a3b8; font-size: 0.9em; border-top: 1px solid #e2e8f0;">
            <p>© 2026 Atlas | labsdigital</p>
            <p>Diterbitkan oleh GitHub → <a href="https://github.com/labsdigital/hermes" style="color: #3b82f6;">labsdigital/hermes</a></p>
        </div>
    </div>
</body>
</html>
"""

# Write output
OUTPUT_FILE.write_text(full_html, encoding='utf-8')
print(f"✅ HTML book created: {OUTPUT_FILE}")
print(f"📊 Size: {OUTPUT_FILE.stat().st_size / 1024:.1f} KB")
