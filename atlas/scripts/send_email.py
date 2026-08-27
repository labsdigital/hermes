#!/usr/bin/env python3
"""
Atlas Essay Email Sender
Sends essay via email with SVG illustration from GitHub Pages
"""

import argparse
import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import os

SMTP_SERVER = "mail.taraka.id"
SMTP_PORT = 465
SENDER = "blog@taraka.id"
PASSWORD = os.environ.get("EMAIL_PASSWORD", "Blog.215")
RECIPIENT = "tamimnasa.simbioma@blogger.com"

# GitHub Pages base URL
GITHUB_PAGES_URL = "https://taraka.id/hermes"

# Default SVG for articles (can be overridden)
DEFAULT_SVG_URL = f"{GITHUB_PAGES_URL}/atlas/assets/atrofi-kognitif-illustration.svg"


def md_to_html(md_text: str) -> str:
    """Convert markdown to HTML with proper line breaks and SVG handling."""
    # First, extract inline SVG blocks and replace with placeholders
    svg_placeholders = []
    def replace_svg(match):
        svg_code = match.group(1)
        placeholder = f"__SVG_PLACEHOLDER_{len(svg_placeholders)}__"
        svg_placeholders.append(svg_code)
        return placeholder

    # Replace ```svg ... ``` blocks with placeholders
    md_text = re.sub(r'```svg\s*\n(.*?)\n```', replace_svg, md_text, flags=re.DOTALL)

    paragraphs = md_text.split('\n\n')
    result = []

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        # Restore SVG placeholders as inline SVG
        if para.startswith('__SVG_PLACEHOLDER_'):
            idx = int(para.replace('__SVG_PLACEHOLDER_', '').replace('__', ''))
            svg_code = svg_placeholders[idx]
            result.append(f'<div class="illustration">{svg_code}</div>')
            continue

        # Handle headers
        if para.startswith('# '):
            content = para[2:].strip()
            result.append(f'<h1>{content}</h1>')
        elif para.startswith('## '):
            content = para[3:].strip()
            result.append(f'<h2>{content}</h2>')
        elif para.startswith('### '):
            content = para[4:].strip()
            result.append(f'<h3>{content}</h3>')
        # Handle blockquotes
        elif para.startswith('> '):
            lines = [l[2:] for l in para.split('\n') if l.startswith('> ')]
            content = '<br>'.join(lines)
            result.append(f'<blockquote>{content}</blockquote>')
        # Handle horizontal rules
        elif para.strip() == '---':
            result.append('<hr>')
        # Handle bold/italic
        else:
            # Replace **bold** with <strong>
            para = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', para)
            # Replace *italic* with <em>
            para = re.sub(r'\*(.+?)\*', r'<em>\1</em>', para)
            # Handle single line breaks within paragraph
            lines = para.split('\n')
            content = '<br>'.join(lines)
            result.append(f'<p>{content}</p>')

    return '\n'.join(result)


def send_email(article_path: str):
    """Send essay via email with SVG illustration from GitHub Pages."""
    article_file = Path(article_path)
    if not article_file.exists():
        print(f"Error: Article not found: {article_path}")
        return False

    # Read article
    content = article_file.read_text(encoding="utf-8")

    # Extract title from article (first line starting with #)
    title = "Esai Atlas"
    for line in content.split('\n'):
        if line.startswith('# '):
            title = line.lstrip('# ').strip()
            break

    # Extract date from filename
    date_str = article_file.stem.split('-')[-1] if '-' in article_file.stem else "2026-08-25"

    # Convert markdown to HTML
    html_content = md_to_html(content)

    # SVG Image URL from GitHub Pages (use article-specific SVG if exists)
    article_name = Path(article_path).stem
    svg_filename = f"{article_name}.svg"
    svg_path = Path(f"/opt/data/hermes/atlas/assets/{svg_filename}")
    
    if svg_path.exists():
        svg_url = f"{GITHUB_PAGES_URL}/atlas/assets/{svg_filename}"
    else:
        svg_url = DEFAULT_SVG_URL

    # Create email
    msg = MIMEMultipart("alternative")
    msg["Subject"] = title
    msg["From"] = SENDER
    msg["To"] = RECIPIENT

    # Plain text version (NO title, NO SVG code blocks - clean format for email)
    # Remove SVG code blocks for plain text
    clean_content = re.sub(r'```svg\s*\n.*?\n```', '[Diagram SVG]', content, flags=re.DOTALL)
    plain_text = f"""Oleh Atlas | {date_str}

{clean_content}
"""
    msg.attach(MIMEText(plain_text, "plain", "utf-8"))

    # HTML version with inline SVG image (NO title/author/date in body)
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: Georgia, 'Times New Roman', serif;
            line-height: 1.8;
            max-width: 700px;
            margin: 0 auto;
            padding: 30px;
            color: #334155;
            background-color: #fafafa;
        }}
        h1 {{
            color: #1e293b;
            margin-top: 0;
            margin-bottom: 10px;
            font-size: 28px;
            border-bottom: 3px solid #f97316;
            padding-bottom: 15px;
        }}
        h2 {{
            color: #1e293b;
            margin-top: 30px;
            margin-bottom: 15px;
            font-size: 22px;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 10px;
        }}
        h3 {{
            color: #334155;
            margin-top: 25px;
            margin-bottom: 10px;
            font-size: 18px;
        }}
        .illustration {{
            text-align: center;
            margin: 30px 0;
        }}
        .illustration img {{
            max-width: 100%;
            height: auto;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            border-radius: 12px;
        }}
        blockquote {{
            border-left: 4px solid #f97316;
            margin: 20px 0;
            padding-left: 20px;
            font-style: italic;
            color: #475569;
        }}
        p {{
            margin: 15px 0;
            text-align: justify;
        }}
        strong {{
            color: #1e293b;
        }}
        em {{
            font-style: italic;
            color: #475569;
        }}
        hr {{
            border: none;
            border-top: 1px solid #e2e8f0;
            margin: 30px 0;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>
"""

    msg.attach(MIMEText(html, "html", "utf-8"))

    # Send via SSL port 465
    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SENDER, PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"✅ Email sent to {RECIPIENT}")
        print(f"📧 Subject: {title}")
        print(f"🖼️  Image: {svg_url}")
        return True
    except Exception as e:
        print(f"❌ Email failed: {e}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send Atlas essay via email")
    parser.add_argument("--article", required=True, help="Path to article file")
    args = parser.parse_args()

    success = send_email(args.article)
    exit(0 if success else 1)
