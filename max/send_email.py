#!/usr/bin/env python3
"""
Max Email Sender - Kirim email untuk notifikasi artikel
Usage: python3 send_email.py <recipient> <subject> <body>
"""

import smtplib
import sys
from email.message import EmailMessage
from pathlib import Path
import json

# Konfigurasi
SMTP_HOST = "mail.taraka.id"
SMTP_PORT = 465  # SSL
SMTP_USER = "blog@taraka.id"
SMTP_PASS = "Blog.215"

def send_email(recipient, subject, body, html=False):
    """Kirim email melalui SMTP SSL"""
    msg = EmailMessage()
    msg['From'] = SMTP_USER
    msg['To'] = recipient
    msg['Subject'] = subject
    
    if html:
        msg.add_alternative(body, subtype='html')
    else:
        msg.set_content(body)
    
    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        return True, f"Email berhasil dikirim ke {recipient}"
    except Exception as e:
        return False, f"Error: {e}"

def send_article_notification(article_path, recipient="tamimnasa@gmail.com"):
    """Kirim notifikasi artikel baru"""
    article = Path(article_path)
    if not article.exists():
        return False, "File tidak ditemukan"
    
    content = article.read_text()
    
    # Extract metadata
    lines = content.split('\n')
    title = ""
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
            break
    
    # Format HTML body
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h1 style="color: #667eea;">📚 New Article from Max</h1>
        <h2>{title}</h2>
        <hr>
        <pre style="background: #f5f5f5; padding: 15px; border-radius: 8px; overflow-x: auto;">
{content[:2000]}...
        </pre>
        <hr>
        <p><a href="https://github.com/labsdigital/hermes/tree/main/max/reports" 
               style="color: #667eea;">View on GitHub</a></p>
        <p style="color: #888; font-size: 12px;">Sent by Max AI Agent</p>
    </body>
    </html>
    """
    
    return send_email(recipient, f"📚 Max Article: {title}", html_body, html=True)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 send_email.py <recipient> <subject> <body>")
        print("Or: python3 send_email.py --article <path> [--recipient <email>]")
        sys.exit(1)
    
    if sys.argv[1] == "--article":
        article_path = sys.argv[2]
        recipient = sys.argv[4] if len(sys.argv) > 4 and sys.argv[3] == "--recipient" else "tamimnasa@gmail.com"
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
