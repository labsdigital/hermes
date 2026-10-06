"""Check a theme's colour pairs against WCAG 2.x contrast ratios.

Every pair listed here is a real pairing used by the stylesheet / DOCX renderer,
so a theme that passes renders legibly everywhere. Usage:
    python check_contrast.py assets/themes/edukasi.json [more.json ...]
    python check_contrast.py --all          # every theme in assets/themes
Exit code 1 if any required pair fails.
"""
import json, sys, os, glob


def lum(hex_):
    h = hex_.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


# (foreground, background, minimum, where it is used)
PAIRS = [
    ("ink", "paper", 7.0, "body text"),
    ("muted", "paper", 4.5, "captions, footers, secondary text"),
    ("primary", "paper", 4.5, "headings"),
    ("primary2", "paper", 4.5, "sub-headings, links"),
    ("#FFFFFF", "primary", 4.5, "table headers, summary box text"),
    ("#FFFFFF", "primaryDark", 7.0, "cover / opener title"),
    ("#FFFFFF", "success", 4.5, "'do' table header"),
    ("#FFFFFF", "danger", 4.5, "'avoid' table header"),
    ("#FFFFFF", "codeHead", 4.5, "template box header"),
    ("accent", "primaryDark", 3.0, "big numbers / accent title on cover (large text)"),
    ("accent", "primary", 3.0, "opener number, summary one-liner (large/bold)"),
    ("ink", "accent", 4.5, "chips and number badges"),
    ("accentDark", "accentLight", 4.5, "analogy / exercise callout label"),
    ("accentDark", "paper", 4.5, "kickers, template codes"),
    ("primary2", "primaryLight", 4.5, "note callout label"),
    ("success", "successLight", 4.5, "tip / good-practice callout label"),
    ("danger", "dangerLight", 4.5, "warning / limits callout label"),
    ("info", "infoLight", 4.5, "policy callout label"),
    ("violet", "violetLight", 4.5, "question callout label"),
    ("neutral", "neutralLight", 4.5, "privacy callout label"),
    ("ink", "zebra", 7.0, "table zebra rows"),
    ("ink", "codeBg", 7.0, "template / code text"),
]


def resolve(colors, key):
    return key if key.startswith("#") else colors[key]


def check(path):
    t = json.load(open(path))
    c = t["colors"]
    fails = 0
    print(f"\n== {t.get('label', os.path.basename(path))}")
    for fg, bg, need, use in PAIRS:
        r = ratio(resolve(c, fg), resolve(c, bg))
        ok = r >= need
        fails += not ok
        mark = "OK  " if ok else "FAIL"
        print(f"  {mark} {r:5.2f} (≥{need:>3}) {fg:>10} on {bg:<12} {use}")
    for i, s in enumerate(c.get("series", [])):
        r = ratio("#FFFFFF", s)
        ok = r >= 4.5
        fails += not ok
        print(f"  {'OK  ' if ok else 'FAIL'} {r:5.2f} (≥4.5) white on series[{i}] {s}  badges/diagram fills")
    return fails


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    paths = sys.argv[1:]
    if not paths or paths == ["--all"]:
        paths = sorted(glob.glob(os.path.join(here, "..", "assets", "themes", "*.json")))
    total = sum(check(p) for p in paths)
    print(f"\n{'ALL PASS' if total == 0 else str(total) + ' FAILING PAIR(S)'}")
    sys.exit(1 if total else 0)
