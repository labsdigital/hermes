#!/usr/bin/env python3
"""
Chalbi Email Sender - Kirim email untuk notifikasi artikel
Usage: python3 send_email.py <recipient> <subject> <body>
       python3 send_email.py --article <path> [--recipient <email>]
"""

import smtplib
import sys
import re
from email.message import EmailMessage
from pathlib import Path

# Konfigurasi
SMTP_HOST = "mail.taraka.id"
SMTP_PORT = 465  # SSL
SMTP_USER = "blog@taraka.id"
SMTP_PASS = "Blog.215"

def md_to_html(md_text):
    """Convert markdown to HTML dengan styling Rumi"""
    lines = md_text.split('\n')
    html_lines = []
    in_code_block = False
    in_list = False
    in_quote = False
    
    for line in lines:
        # Code blocks
        if line.startswith('```'):
            if in_code_block:
                html_lines.append('</code></pre>')
                in_code_block = False
            else:
                html_lines.append('<pre><code style="background:#f8fafc;padding:12px;border-radius:8px;font-family:monospace;">')
                in_code_block = True
            continue
        
        if in_code_block:
            html_lines.append(line.replace('<', '&lt;').replace('>', '&gt;'))
            continue
        
        # Headers
        if line.startswith('### '):
            html_lines.append(f'<h3 style="color:#7c3aed;margin-top:24px;">{line[4:]}</h3>')
        elif line.startswith('## '):
            html_lines.append(f'<h2 style="color:#7c3aed;margin-top:32px;border-bottom:2px solid #ede9fe;padding-bottom:8px;">{line[3:]}</h2>')
        elif line.startswith('# '):
            html_lines.append(f'<h1 style="color:#581c87;font-size:28px;margin-bottom:20px;">{line[2:]}</h1>')
        # Horizontal rule
        elif line == '---':
            html_lines.append('<hr style="border:none;border-top:1px solid #e9d5ff;margin:24px 0;">')
        # Quote blocks (Rumi quotes)
        elif line.startswith('> ') or line.startswith('❝'):
            if not in_quote:
                html_lines.append('<blockquote style="border-left:4px solid #a855f7;padding-left:16px;margin:16px 0;background:#faf5ff;border-radius:0 8px 8px 0;font-style:italic;color:#6b21a8;">')
                in_quote = True
            content = line.lstrip('> ❝').strip()
            html_lines.append(f'<p style="margin:4px 0;">{content}</p>')
        elif in_quote and line.strip() == '':
            html_lines.append('</blockquote>')
            in_quote = False
        # Bold
        elif '**' in line:
            line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\\1</strong>', line)
            line = re.sub(r'\*(.+?)\*', r'<em>\\1</em>', line)
            html_lines.append(f'<p>{line}</p>')
        # Lists
        elif line.startswith('- '):
            if not in_list:
                html_lines.append('<ul style="line-height:1.8;">')
                in_list = True
            html_lines.append(f'<li>{line[2:]}</li>')
        elif line.strip() == '':
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            continue
        # Regular paragraph
        else:
            html_lines.append(f'<p style="line-height:1.8;">{line}</p>')
    
    if in_list:
        html_lines.append('</ul>')
    if in_quote:
        html_lines.append('</blockquote>')
    
    return '\n'.join(html_lines)

def send_email(recipient, subject, body_html):
    """Kirim email melalui SMTP SSL dengan HTML body"""
    msg = EmailMessage()
    msg['From'] = SMTP_USER
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.add_alternative(f"""\\\
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 700px; margin: 0 auto; padding: 20px; line-height: 1.6; background:#fafafa;">
<div style="background:linear-gradient(135deg,#7c3aed,#a855f7);color:white;padding:20px;border-radius:12px;margin-bottom:20px;text-align:center;">
<h1 style="margin:0;font-size:24px;">✨ Artikel Baru dari Chalbi</h1>
<p style="margin:8px 0 0 0;opacity:0.9;">Rumi & Masnavi Studies</p>
</div>
{body_html}
<div style="margin-top:40px;padding-top:20px;border-top:1px solid #e9d5ff;text-align:center;color:#8b5cf6;font-size:14px;">
<p>Dikirim oleh <strong>@chalbi</strong> — Ahli Sastra Rumi</p>
</div>
</body>
</html>
""", subtype='html')
    
    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        return True, f"Email berhasil dikirim ke {recipient}"
    except Exception as e:
        return False, f"Error: {e}"

def send_article_notification(article_path, recipient="tamimnasa.chalbi@blogger.com"):
    """Kirim notifikasi artikel baru"""
    article = Path(article_path)
    if not article.exists():
        return False, "File tidak ditemukan"
    
    content = article.read_text()
    lines = content.split('\n')
    
    # Extract title (first line starting with #)
    title = ""
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
            break
    
    # Remove title from content
    body_lines = []
    skipped_title = False
    for line in lines:
        if not skipped_title and line.startswith('# '):
            skipped_title = True
            continue
        body_lines.append(line)
    
    body_md = '\n'.join(body_lines).strip()
    body_html = md_to_html(body_md)
    
    return send_email(recipient, f"📜 {title}", body_html)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 send_email.py <recipient> <subject> <body>")
        print("Or: python3 send_email.py --article <path> [--recipient <email>]")
        sys.exit(1)
    
    if sys.argv[1] == "--article":
        article_path = sys.argv[2]
        recipient = "tamimnasa.chalbi@blogger.com"
        if len(sys.argv) > 3 and sys.argv[3] == "--recipient":
            recipient = sys.argv[4]
        success, msg = send_article_notification(article_path, recipient)
        print(msg)
        sys.exit(0 if success else 1)
    else:
        recipient = sys.argv[1]
        subject = sys.argv[2]
        body = sys.argv[3]
        success, msg = send_email(recipient, subject, body)
        print(msg)
        sys.exit(0 if success else 1)
