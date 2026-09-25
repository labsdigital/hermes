#!/usr/bin/env python3
"""
Email Tracking for Atlas Articles
Prevents double-sending by tracking which articles have been emailed
"""

import json
from pathlib import Path
from datetime import datetime


SENT_TRACKER_FILE = Path("/opt/data/hermes/atlas/reports/.email_sent.json")


def load_sent_log() -> dict:
    """Load email sent tracking log."""
    if SENT_TRACKER_FILE.exists():
        try:
            return json.loads(SENT_TRACKER_FILE.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_sent_log(sent_log: dict):
    """Save email sent tracking log."""
    SENT_TRACKER_FILE.write_text(
        json.dumps(sent_log, indent=2, ensure_ascii=False),
        encoding='utf-8'
    )


def is_already_sent(article_path: str) -> bool:
    """Check if article has already been sent via email."""
    sent_log = load_sent_log()
    article_name = Path(article_path).stem
    
    # Check by article name
    if article_name in sent_log:
        return True
    
    # Check by full path
    if article_path in sent_log:
        return True
    
    return False


def mark_as_sent(article_path: str, recipient: str = "", subject: str = ""):
    """Mark article as sent via email."""
    sent_log = load_sent_log()
    article_name = Path(article_path).stem
    timestamp = datetime.now().isoformat()
    
    sent_log[article_name] = {
        "path": article_path,
        "sent_at": timestamp,
        "recipient": recipient,
        "subject": subject
    }
    
    # Also save by full path for exact matching
    sent_log[article_path] = sent_log[article_name]
    
    save_sent_log(sent_log)


def get_sent_articles() -> list:
    """Get list of all articles that have been sent."""
    sent_log = load_sent_log()
    return [
        {
            "article": name,
            "sent_at": data.get("sent_at", ""),
            "recipient": data.get("recipient", "")
        }
        for name, data in sent_log.items()
        if not name.startswith('.')  # Exclude internal entries
    ]


def clear_sent_log():
    """Clear the sent log (for debugging/testing)."""
    if SENT_TRACKER_FILE.exists():
        SENT_TRACKER_FILE.unlink()
    save_sent_log({})


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Email tracking utility")
    parser.add_argument("action", choices=["check", "mark", "list", "clear"])
    parser.add_argument("--article", help="Article path")
    args = parser.parse_args()
    
    if args.action == "check":
        if args.article and is_already_sent(args.article):
            print(f"ALREADY_SENT: {args.article}")
            exit(1)
        else:
            print("NOT_SENT")
            exit(0)
    
    elif args.action == "mark":
        if args.article:
            mark_as_sent(args.article)
            print(f"MARKED: {args.article}")
    
    elif args.action == "list":
        articles = get_sent_articles()
        if articles:
            for art in articles[-10:]:  # Show last 10
                print(f"{art['article']}: {art['sent_at']}")
        else:
            print("No emails sent yet")
    
    elif args.action == "clear":
        clear_sent_log()
        print("Sent log cleared")
