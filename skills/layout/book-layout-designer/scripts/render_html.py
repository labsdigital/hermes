"""Render the AST + book config + theme into a single print-ready HTML file.

Chromium (render_pdf.js) turns it into the PDF; snapshot.js screenshots the
cover and figures from the same HTML so the DOCX shows identical visuals.
"""
import html, json, math, os, re

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAGE = {  # width, height (mm), margins top/right/bottom/left (mm), cover scale, figure zoom
    "A4": (210, 297, (18, 18, 20, 18), 1.0, 1.0),
    "Letter": (215.9, 279.4, (18, 19, 20, 19), 0.97, 1.0),
    "B5": (176, 250, (16, 15, 18, 15), 0.84, 0.86),
    "A5": (148, 210, (14, 13, 16, 13), 0.7, 0.7),
}

LABELS = {
    "id": {"note": "Catatan", "tip": "Tips", "analogy": "Analogi", "policy": "Kebijakan & Panduan",
           "warning": "Perhatian", "limits": "Uji Batas", "check": "Praktik Baik", "privacy": "Privasi Data",
           "exercise": "Latihan", "question": "Refleksi", "example": "Contoh", "summary": "Intisari",
           "card": "Kartu Ringkas", "goals": "Tujuan", "quote": "", "stats": "",
           "toc": "Daftar Isi", "front": "Bagian Awal", "parts": "Isi Utama", "back": "Penutup & Lampiran",
           "goals_head": "Setelah bagian ini, Anda mampu:", "templates_head": "Template di bagian ini",
           "contents_head": "Isi bagian ini", "do": "✓ ", "dont": "✗ ", "copy_hint": "salin → ganti [ … ]",
           "template": "Template", "figure": "Gambar"},
    "en": {"note": "Note", "tip": "Tip", "analogy": "Analogy", "policy": "Policy & Guidance",
           "warning": "Warning", "limits": "Limitations", "check": "Good Practice", "privacy": "Data Privacy",
           "exercise": "Exercise", "question": "Reflection", "example": "Example", "summary": "Key Takeaways",
           "card": "Quick Card", "goals": "Goals", "quote": "", "stats": "",
           "toc": "Contents", "front": "Front Matter", "parts": "Main Content", "back": "Closing & Appendices",
           "goals_head": "After this part you will be able to:", "templates_head": "Templates in this part",
           "contents_head": "In this part", "do": "✓ ", "dont": "✗ ", "copy_hint": "copy → replace [ … ]",
           "template": "Template", "figure": "Figure"},
}

# callout kind -> (colour, light background) theme keys
CALLOUT_COL = {
    "note": ("primary2", "primaryLight"), "tip": ("success", "successLight"), "analogy": ("accentDark", "accentLight"),
    "policy": ("info", "infoLight"), "warning": ("danger", "dangerLight"), "limits": ("danger", "dangerLight"),
    "check": ("success", "successLight"), "privacy": ("neutral", "neutralLight"), "exercise": ("accentDark", "accentLight"),
    "question": ("violet", "violetLight"), "example": ("info", "infoLight"), "summary": ("accent", "primary"),
    "card": ("primary2", "paper"), "goals": ("primary", "primaryLight"), "quote": ("accent", "paper"), "stats": ("primary", "primaryLight"),
}
ICON = {
    "note": '<circle cx="12" cy="12" r="10"/><path d="M12 11v6M12 7.5v.5"/>',
    "tip": '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z"/>',
    "analogy": '<path d="M4 12h6l2-3 2 6 2-3h4"/><circle cx="12" cy="12" r="10"/>',
    "policy": '<path d="M6 3h9l4 4v14H6z"/><path d="M14 3v5h5M9 13h7M9 17h7"/>',
    "warning": '<path d="M12 3l10 18H2z"/><path d="M12 10v5M12 18v.5"/>',
    "limits": '<path d="M12 3l10 18H2z"/><path d="M12 10v5M12 18v.5"/>',
    "check": '<circle cx="12" cy="12" r="10"/><path d="M7 12.5l3.5 3.5L17 9"/>',
    "privacy": '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
    "exercise": '<path d="M4 20l4-1 11-11-3-3L5 16z"/><path d="M14 6l3 3"/>',
    "question": '<circle cx="12" cy="12" r="10"/><path d="M9.5 9a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .9-1 1.6V14M12 17.5v.5"/>',
    "example": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 9h10M7 13h7"/>',
    "summary": '<path d="M12 2l2.9 6.9L22 9.6l-5.5 4.8L18.2 22 12 18.3 5.8 22l1.7-7.6L2 9.6l7.1-.7z"/>',
    "card": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M7 10h10M7 14h6"/>',
    "goals": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
}

PH = re.compile(r"\[([^\]]+)\]")


def esc(s):
    return html.escape(str(s), quote=False)


def ph_prompt(m):
    inner = m.group(1)
    if re.search(r"[A-Za-z]", inner) and inner.upper() == inner:
        return m.group(0)  # ALL-CAPS tags like [VERIFY] are literal
    return f'<span class="ph">{m.group(0)}</span>'


def ph_text(m):
    inner = m.group(1)
    return f'<span class="ph">{m.group(0)}</span>' if re.search(r"[a-z]", inner) and len(inner) > 2 else m.group(0)


class Renderer:
    def __init__(self, cfg, theme, pages=None):
        self.cfg, self.theme, self.pages = cfg, theme, pages or {}
        self.lang = cfg.get("lang", "id")
        self.L = dict(LABELS.get(self.lang, LABELS["id"]))
        self.L.update(cfg.get("labels", {}))
        self.C = theme["colors"]
        self.fig_n = 0
        self.hl_ph = cfg.get("highlight_placeholders", True)

    # ---------- inline ----------
    def runs(self, rs, prompt=False):
        out = []
        for r in rs:
            t = esc(r["t"])
            if r.get("code"):
                out.append(f"<code>{t}</code>")
                continue
            if self.hl_ph:
                t = PH.sub(ph_prompt if prompt else ph_text, t)
            if r.get("href"):
                t = f'<a href="{html.escape(r["href"])}">{t}</a>'
            if r.get("i"):
                t = f"<em>{t}</em>"
            if r.get("b"):
                t = f"<strong>{t}</strong>"
            out.append(t)
        return "".join(out)

    # ---------- blocks ----------
    def list_(self, n):
        tag = "ol" if n["ordered"] else "ul"
        cls = ' class="steps"' if n.get("steps") else ""
        items = "".join(f"<li>{self.runs(it['runs'])}{''.join(self.list_(c) for c in it['children'])}</li>" for it in n["items"])
        return f"<{tag}{cls}>{items}</{tag}>"

    def col_widths(self, t):
        n = len(t["header"])
        if t.get("widths") and len(t["widths"]) == n:
            w = t["widths"]
        else:
            preset = {"dodont": [20, 40, 40], "compare": [50, 50], "glossary": [26, 74], "checklist": [7, 78, 15]}
            w = preset.get(t["cls"]) if preset.get(t["cls"]) and len(preset[t["cls"]]) == n else None
            if not w and t["cls"] == "matrix" and n > 2:
                w = [20] + [80 / (n - 1)] * (n - 1)
            if not w:
                lens = []
                for c in range(n):
                    cells = [t["header_text"][c]] + [r[c] if c < len(r) else "" for r in t["rows_text"]]
                    avg = sum(len(x) for x in cells) / len(cells)
                    longest = max((len(wd) for x in cells for wd in re.sub(r"[*`]", "", x).split()), default=4)
                    lens.append(max(6, longest * 1.6, min(60, avg)))
                w = lens
        s = sum(w)
        return [round(100 * x / s, 2) for x in w]

    def table(self, t):
        w = self.col_widths(t)
        cols = "".join(f'<col style="width:{x}%">' for x in w)
        head = []
        for ci, c in enumerate(t["header"]):
            cls = ""
            if t["cls"] == "dodont" and ci > 0:
                cls = ["do", "dont"][min(ci - 1, 1)]
            if t["cls"] == "compare":
                cls = "dont" if ci == 0 else "do"
            pre = {"do": self.L["do"], "dont": self.L["dont"]}.get(cls, "")
            head.append(f'<th class="{cls}">{pre}{self.runs(c)}</th>')
        key_first = t["cls"] in ("dodont", "matrix", "glossary", "key")
        num_first = t["cls"] in ("checklist", "numbered")
        body = []
        for r in t["rows"]:
            tds = []
            for ci, c in enumerate(r):
                cls = "key" if (ci == 0 and key_first) else ("num" if (ci == 0 and num_first) else "")
                tds.append(f'<td class="{cls}">{self.runs(c)}</td>')
            body.append("<tr>" + "".join(tds) + "</tr>")
        return (f'<table class="t-{t["cls"]}"><colgroup>{cols}</colgroup><thead><tr>{"".join(head)}</tr></thead>'
                f'<tbody>{"".join(body)}</tbody></table>')

    def split_title(self, title):
        m = re.match(r"^(\S+\s+[\w.\-]+)\s*·\s*(.*)$", title)
        return (m.group(1), m.group(2)) if m else ("", title)

    def prompt(self, p):
        lines = []
        for l in p["lines"]:
            if l.startswith("### "):
                lines.append(f'<div class="pl-h">{esc(l[4:])}</div>')
            elif not l.strip():
                lines.append('<div class="pl-sp"></div>')
            else:
                lines.append(f'<div class="pl">{PH.sub(ph_prompt, esc(l)) if self.hl_ph else esc(l)}</div>')
        code, title = self.split_title(p["title"])
        chip = code or self.L["template"]
        return (f'<div class="prompt"><div class="p-head"><span class="p-chip">{esc(chip)}</span>'
                f'<span class="p-title">{esc(title)}</span><span class="p-hint">{esc(self.L["copy_hint"])}</span></div>'
                f'<div class="p-body">{"".join(lines)}</div></div>')

    def code(self, c):
        body = "".join(f'<div class="pl">{esc(l) if l.strip() else "&nbsp;"}</div>' for l in c["lines"])
        label = c["lang"] or "code"
        title = f'<span class="p-title">{esc(c["title"])}</span>' if c["title"] else '<span class="p-title"></span>'
        return (f'<div class="code"><div class="p-head"><span class="p-chip">{esc(label)}</span>{title}</div>'
                f'<div class="p-body">{body}</div></div>')

    def callout(self, c):
        kind = c["kind"]
        col, light = CALLOUT_COL.get(kind, CALLOUT_COL["note"])
        style = f'--c:{self.C[col]};--l:{self.C[light]}'
        if kind == "stats":
            cells = []
            for k, it in enumerate(c.get("items", [])):
                s = self.C["series"][k % len(self.C["series"])]
                cells.append(f'<div class="stat" style="--c:{s}"><div class="v">{esc(it["value"])}</div><div class="t">{esc(it["label"])}</div></div>')
            return f'<div class="stats">{"".join(cells)}</div>'
        inner = self.nodes(c.get("children", []))
        if kind == "quote":
            by = f'<div class="q-by">— {esc(c["title"])}</div>' if c["title"] else ""
            return f'<div class="callout k-quote" style="{style}"><div class="c-body">{inner}{by}</div></div>'
        label = c.get("attrs", {}).get("label") or self.L.get(kind, "")
        icon = f'<svg class="ic" viewBox="0 0 24 24">{ICON.get(kind, ICON["note"])}</svg>'
        title = f'<div class="c-title">{esc(c["title"])}</div>' if c["title"] else ""
        return (f'<div class="callout k-{kind}" style="{style}"><div class="c-head">{icon}<span class="c-label">{esc(label)}</span></div>'
                f'{title}<div class="c-body">{inner}</div></div>')

    def figure(self, n):
        self.fig_n += 1
        src, cap, opts = n["src"], n["caption"], n.get("opts", {})
        ext = os.path.splitext(src)[1].lower()
        width = opts.get("width")
        if ext in (".html", ".htm"):
            frag = open(src, encoding="utf-8").read()
            body = f'<div class="fig-html">{frag}</div>'
        elif ext == ".svg":
            body = open(src, encoding="utf-8").read()
            body = re.sub(r"<\?xml[^>]*>", "", body)
        else:
            st = f' style="width:{width}"' if width else ""
            body = f'<img src="file://{src}"{st}>'
        full = " full" if ext not in (".html", ".htm", ".svg") else ""
        capt = f"<figcaption>{esc(cap)}</figcaption>" if cap else ""
        return f'<figure class="fig" id="fig-{self.fig_n}" data-src="{html.escape(src)}"><div class="fig-body{full}">{body}</div>{capt}</figure>'

    def h2(self, n):
        from parse_md import inline
        m = re.match(r"^(\d+[A-Za-z]?)\.\s+(.*)$", n["text"])
        if m:
            return f'<h2 id="{n["id"]}"><span class="num">{m.group(1)}</span><span class="h2t">{self.runs(inline(m.group(2)))}</span></h2>'
        return f'<h2 id="{n["id"]}"><span class="h2t">{self.runs(n["runs"])}</span></h2>'

    def nodes(self, nodes):
        out = []
        for n in nodes:
            t = n["type"]
            if t == "p":
                out.append(f"<p>{self.runs(n['runs'])}</p>")
            elif t == "h2":
                out.append(self.h2(n))
            elif t == "h3":
                out.append(f"<h3>{self.runs(n['runs'])}</h3>")
            elif t == "list":
                out.append(self.list_(n))
            elif t == "table":
                out.append(self.table(n))
            elif t == "prompt":
                out.append(self.prompt(n))
            elif t == "code":
                out.append(self.code(n))
            elif t == "callout":
                out.append(self.callout(n))
            elif t == "figure":
                out.append(self.figure(n))
            elif t == "pagebreak":
                out.append('<div class="pb"></div>')
        return "".join(out)

    # ---------- decorative art ----------
    def art(self, motif):
        if motif == "helm":
            spokes, knobs = [], []
            for k in range(8):
                a = k * math.pi / 4
                spokes.append(f'<line x1="{16*math.cos(a):.1f}" y1="{16*math.sin(a):.1f}" x2="{90*math.cos(a):.1f}" y2="{90*math.sin(a):.1f}"/>')
                knobs.append(f'<circle cx="{96*math.cos(a):.1f}" cy="{96*math.sin(a):.1f}" r="10"/>')
            return ('<svg viewBox="-110 -110 220 220"><g fill="none" stroke="currentColor" stroke-linecap="round"><circle r="70" stroke-width="11"/>'
                    f'<circle r="50" stroke-width="2.5" opacity=".7"/><g stroke-width="7">{"".join(spokes)}</g></g>'
                    f'<circle r="17" fill="currentColor"/><g fill="currentColor">{"".join(knobs)}</g></svg>')
        if motif == "orbit":
            dots = "".join(f'<circle cx="{r*math.cos(a):.1f}" cy="{r*math.sin(a):.1f}" r="{s}" fill="currentColor"/>'
                           for r, a, s in [(95, 0.6, 9), (70, 2.4, 7), (45, 4.1, 6), (95, 3.7, 5), (70, 5.4, 8)])
            return ('<svg viewBox="-110 -110 220 220"><g fill="none" stroke="currentColor"><circle r="95" stroke-width="3"/>'
                    '<circle r="70" stroke-width="2.5" stroke-dasharray="6 7"/><circle r="45" stroke-width="3"/></g>'
                    f'<circle r="22" fill="currentColor"/>{dots}</svg>')
        if motif == "grid":
            cells = []
            for i in range(5):
                for j in range(5):
                    op = 0.25 + 0.75 * ((i + j) % 3 == 0)
                    shape = (f'<rect x="{-100+i*42}" y="{-100+j*42}" width="30" height="30" rx="7" fill="currentColor" opacity="{op:.2f}"/>'
                             if (i * j) % 2 == 0 else f'<circle cx="{-85+i*42}" cy="{-85+j*42}" r="14" fill="currentColor" opacity="{op:.2f}"/>')
                    cells.append(shape)
            return f'<svg viewBox="-110 -110 220 220">{"".join(cells)}</svg>'
        if motif == "waves":
            paths = "".join(f'<path d="M-110 {y} C -60 {y-24}, -20 {y+24}, 30 {y} S 110 {y-20}, 130 {y}" stroke-width="{w}"/>'
                            for y, w in [(-70, 9), (-35, 6), (0, 11), (35, 6), (70, 9)])
            return f'<svg viewBox="-110 -110 220 220"><g fill="none" stroke="currentColor" stroke-linecap="round">{paths}</g></svg>'
        if motif == "book":
            return ('<svg viewBox="-110 -110 220 220"><g fill="none" stroke="currentColor" stroke-width="7" stroke-linejoin="round">'
                    '<path d="M0 -55 C -30 -75, -70 -75, -95 -62 L -95 70 C -70 58, -30 58, 0 78 C 30 58, 70 58, 95 70 L 95 -62 C 70 -75, 30 -75, 0 -55 Z"/>'
                    '<path d="M0 -55 L0 78"/></g><g stroke="currentColor" stroke-width="4" opacity=".6">'
                    '<path d="M-75 -35 H-22 M-75 -10 H-22 M-75 15 H-22 M22 -35 H75 M22 -10 H75 M22 15 H75"/></g></svg>')
        return ""

    def cover_deco(self):
        a = self.C["accent"]
        return f'''<svg class="cv-deco" viewBox="0 0 210 297" preserveAspectRatio="none">
<circle cx="200" cy="10" r="60" fill="#fff" opacity=".07"/><circle cx="-10" cy="250" r="55" fill="#000" opacity=".16"/>
<g stroke="{a}" stroke-width=".35" opacity=".5" fill="none"><path d="M120 20 L150 38 L185 28 L200 60"/><path d="M150 38 L160 70 L195 88"/><path d="M160 70 L128 92"/></g>
<g fill="{a}" opacity=".85"><circle cx="120" cy="20" r="1.4"/><circle cx="150" cy="38" r="1.8"/><circle cx="185" cy="28" r="1.2"/>
<circle cx="200" cy="60" r="1.4"/><circle cx="160" cy="70" r="1.6"/><circle cx="195" cy="88" r="1.2"/><circle cx="128" cy="92" r="1.2"/></g></svg>'''

    def cover(self, n_templates, n_parts):
        cfg, cv = self.cfg, self.cfg.get("cover", {})
        lines = cv.get("title_lines")
        if lines:
            tl = []
            for l in lines:
                if isinstance(l, str):
                    tl.append(f'<span class="l-big">{esc(l)}</span>')
                else:
                    tl.append(f'<span class="l-{l.get("style", "big")}">{esc(l["text"])}</span>')
            title = "".join(tl)
        else:
            title = f'<span class="l-big">{esc(cfg["title"])}</span>'
        chip = f'<span class="cv-chip">{esc(cfg["edition"])}</span>' if cfg.get("edition") else ""
        kicker = f'<span class="cv-kicker">{esc(cfg.get("kicker", ""))}</span>' if cfg.get("kicker") else ""
        sub = f'<div class="cv-sub">{esc(cfg["subtitle"])}</div>' if cfg.get("subtitle") else ""
        author = ""
        if cfg.get("author"):
            inst = f'<span>{esc(cfg["institution"])}</span>' if cfg.get("institution") else ""
            author = f'<div class="cv-author">{esc(cfg["author"])}{inst}</div>'
        motif = cv.get("motif", "helm")
        bubble = f'<div class="cv-bubble">{esc(cv["tagline"])}</div>' if cv.get("tagline") else ""
        art = f'<div class="cv-art">{self.art(motif)}{bubble}</div>' if motif != "none" else ""
        hl = ""
        if cv.get("highlights"):
            items = []
            for k, h in enumerate(cv["highlights"]):
                col = self.C["series"][k % len(self.C["series"])]
                mark = h.get("mark", h.get("label", "?")[:1]) if isinstance(h, dict) else h[:1]
                lab = h.get("label", "") if isinstance(h, dict) else h
                items.append(f'<div class="hl"><div class="hlL" style="background:{col}">{esc(mark)}</div><div class="hlN">{esc(lab)}</div></div>')
            hl = f'<div class="cv-hl">{"".join(items)}</div>'
        chips = cv.get("chips")
        if chips is None:
            chips = []
            if n_parts:
                chips.append(f'{n_parts} {cfg.get("part_label", "Bab").title()}')
            if n_templates:
                chips.append(f'{n_templates} {self.L["template"]}')
        meta = f'<div class="cv-meta">{"".join(f"<span>{esc(c)}</span>" for c in chips)}</div>' if chips else ""
        return (f'<section class="cover">{self.cover_deco()}{art}<div class="cv-in"><div class="cv-top">{chip}{kicker}</div>'
                f'<div class="cv-title">{title}</div>{sub}{author}<div class="cv-spacer"></div>{hl}{meta}</div></section>')

    def back_cover(self):
        bc = self.cfg.get("back_cover")
        if not bc:
            return ""
        if bc is True:
            bc = {}
        quote = f'<div class="bc-quote">{esc(bc["quote"])}</div>' if bc.get("quote") else ""
        blurb = f'<p>{esc(bc["blurb"])}</p>' if bc.get("blurb") else ""
        bullets = "".join(f"<li>{esc(b)}</li>" for b in bc.get("bullets", []))
        bullets = f"<ul>{bullets}</ul>" if bullets else ""
        motif = self.cfg.get("cover", {}).get("motif", "helm")
        return (f'<section class="backcover"><div class="bc-in"><div class="bc-kicker">{esc(self.cfg["title"])}</div>'
                f'{quote}{blurb}{bullets}</div><div class="bc-art">{self.art(motif if motif != "none" else "orbit")}</div></section>')

    def opener(self, p, body):
        goals = self.nodes(p["goals"]["children"]) if p.get("goals") else ""
        items = []
        for n in body:
            if n["type"] == "prompt":
                code, title = self.split_title(n["title"])
                code = re.sub(r"^\S+\s+", "", code) if code else ""
                items.append((code, title))
        head = self.L["templates_head"]
        if not items:
            head = self.L["contents_head"]
            for n in body:
                if n["type"] == "h2":
                    m = re.match(r"^(\d+[A-Za-z]?)\.\s+(.*)$", n["text"])
                    items.append((m.group(1) if m else "•", re.sub(r"[*`]", "", m.group(2) if m else n["text"])))
        lst = "".join(f"<li><b>{esc(a)}</b> {esc(b)}</li>" for a, b in items[:12])
        num = p["num"].zfill(2) if p["num"].isdigit() else p["num"]
        goals_card = f'<div class="op-card op-goals"><div class="op-h">{esc(self.L["goals_head"])}</div>{goals}</div>' if goals else ""
        list_card = f'<div class="op-card op-list"><div class="op-h">{esc(head)}</div><ul>{lst}</ul></div>' if items else ""
        motif = self.cfg.get("cover", {}).get("motif", "helm")
        return f"""<section class="opener" id="{p['id']}"><div class="op-top"><div class="op-art">{self.art(motif if motif != 'none' else 'orbit')}</div>
<div class="op-label">{esc(self.cfg.get('part_label', 'Bab'))}</div><div class="op-num">{esc(num)}</div>
<h1 class="op-title">{esc(p['title'])}</h1><div class="op-sub">{esc(p['subtitle'])}</div></div>
<div class="op-bottom">{goals_card}{list_card}</div></section>"""

    def toc(self, entries):
        nk = lambda s: re.sub(r"\s+", "", s)
        rows = []
        for kind, title, sub, num in entries:
            pg = self.pages.get(nk(title)) or self.pages.get(nk(title.split("·", 1)[-1]), "")
            if kind == "part":
                badge = num.zfill(2) if num.isdigit() else num
                rows.append(f'<div class="toc-row toc-mod"><span class="toc-badge">{esc(badge)}</span><span class="toc-t">'
                            f'<span class="toc-mt">{esc(title)}</span><span class="toc-ms">{esc(sub)}</span></span>'
                            f'<span class="toc-dots"></span><span class="toc-p">{pg}</span></div>')
            elif kind == "group":
                rows.append(f'<div class="toc-group">{esc(title)}</div>')
            else:
                rows.append(f'<div class="toc-row"><span class="toc-t">{esc(title)}</span><span class="toc-dots"></span><span class="toc-p">{pg}</span></div>')
        return (f'<section class="toc chapter-sec" style="page:front"><div class="ch-kicker">{esc(self.L["front"])}</div>'
                f'<h1 class="ch-title">{esc(self.L["toc"])}</h1>{"".join(rows)}</section>')

    # ---------- fonts & variables ----------
    def font_css(self):
        reg = json.load(open(os.path.join(SKILL, "assets", "fonts", "fonts.json")))
        fams = {self.theme["fonts"][k] for k in ("heading", "body", "mono")}
        out = []
        wmap = {"regular": ("400", "normal"), "italic": ("400", "italic"), "medium": ("500", "normal"),
                "bold": ("700", "normal"), "boldItalic": ("700", "italic")}
        for fam in fams:
            for style, file in reg.get(fam, {}).items():
                w, s = wmap[style]
                path = os.path.join(SKILL, "assets", "fonts", file)
                out.append(f'@font-face{{font-family:"{fam}";src:url("file://{path}");font-weight:{w};font-style:{s};}}')
        return "".join(out)

    def vars_css(self):
        c, f, ty = self.C, self.theme["fonts"], self.theme.get("type", {})
        size = self.cfg.get("page_size", "A4")
        pw, ph, (mt, mr, mb, ml), cs, fz = PAGE.get(size, PAGE["A4"])
        base = self.cfg.get("base_size", ty.get("base", 10.2))
        if size in ("A5",):
            base = min(base, 9.6)
        hw = ty.get("headingWeight", 700)
        v = [f"--{k}:{val}" for k, val in c.items() if isinstance(val, str)]
        v += [f"--s{i}:{s}" for i, s in enumerate(c["series"])]
        v += [f'--f-head:"{f["heading"]}",Poppins,"DejaVu Sans",sans-serif', f'--f-body:"{f["body"]}",Lora,"DejaVu Serif",serif',
              f'--f-mono:"{f["mono"]}","DejaVu Sans Mono",monospace', f"--base:{base}pt", f"--leading:{ty.get('leading', 1.55)}",
              f"--hw:{hw}", f"--hw2:{700 if hw >= 600 else 400}", f"--ink-strong:{c['ink']}",
              f"--pw:{pw}mm", f"--ph:{ph}mm", f"--cs:{cs}", f"--fig-zoom:{fz}"]
        foot = self.cfg.get("footer_text", self.cfg["title"])
        fh = f['heading']
        page = (f'@page{{size:{pw}mm {ph}mm;margin:{mt}mm {mr}mm {mb}mm {ml}mm;'
                f'@bottom-left{{content:"{foot}";font-family:"{fh}";font-size:7.5pt;color:{c["muted"]};vertical-align:top;padding-top:5mm;}}'
                f'@bottom-right{{content:counter(page);font-family:"{fh}";font-weight:700;font-size:8.5pt;color:{c["primary"]};vertical-align:top;padding-top:4.5mm;}}}}'
                f'@page cover{{margin:0;@bottom-left{{content:none;}}@bottom-right{{content:none;}}}}'
                f'@page opener{{margin:0;@bottom-left{{content:none;}}@bottom-right{{content:none;}}}}')
        return ":root{" + ";".join(v) + "}" + page


def build_entries(sections, L):
    entries, seen, first_part = [], set(), None
    for idx, s in enumerate(sections):
        if s["head"]["type"] == "part":
            first_part = idx if first_part is None else first_part
    last_part = max([i for i, s in enumerate(sections) if s["head"]["type"] == "part"], default=None)
    for idx, s in enumerate(sections):
        h = s["head"]
        if h["type"] == "part":
            if "parts" not in seen:
                entries.append(("group", L["parts"], "", "")); seen.add("parts")
            entries.append(("part", h["title"], h["subtitle"], h["num"]))
        else:
            if h.get("attrs", {}).get("notoc"):
                continue
            grp = "back" if (last_part is not None and idx > last_part) else "front"
            if first_part is None:
                grp = "front"
            if grp not in seen:
                entries.append(("group", L[grp], "", "")); seen.add(grp)
            entries.append(("chapter", h["title"], "", ""))
    return entries


def render(ast, cfg, theme, pages=None):
    R = Renderer(cfg, theme, pages)
    sections, cur, pre = [], None, []
    for n in ast:
        if n["type"] in ("chapter", "part"):
            cur = {"head": n, "body": []}
            sections.append(cur)
        elif cur is None:
            pre.append(n)
        else:
            cur["body"].append(n)
    if pre:
        sections.insert(0, {"head": {"type": "chapter", "title": cfg.get("preface_title", ""), "id": "pre", "attrs": {"notoc": True}}, "body": pre})
    n_templates = sum(1 for n in ast if n["type"] == "prompt")
    n_parts = sum(1 for s in sections if s["head"]["type"] == "part")
    entries = build_entries(sections, R.L)
    last_part = max([i for i, s in enumerate(sections) if s["head"]["type"] == "part"], default=None)
    parts, page_css = [R.cover(n_templates, n_parts)], []
    toc_after = cfg.get("toc_after")
    want_toc = cfg.get("toc", True)
    if want_toc and not toc_after:
        parts.append(R.toc(entries))
    plabel = cfg.get("part_label", "Bab").title()
    back_foot = cfg.get("footer_back", R.L["back"])
    for idx, s in enumerate(sections):
        h = s["head"]
        if h["type"] == "part":
            pid = "p" + re.sub(r"[^A-Za-z0-9]", "", h["num"])
            short = h.get("short") or (h["title"] if len(h["title"]) < 48 else h["title"][:45] + "…")
            page_css.append(f'@page {pid}{{@bottom-left{{content:"{plabel} {h["num"]} · {short}";}}}}')
            parts.append(R.opener(h, s["body"]))
            parts.append(f'<section class="partbody" style="page:{pid}">{R.nodes(s["body"])}</section>')
        else:
            back = last_part is not None and idx > last_part
            phase = "back" if back else "front"
            attrs = h.get("attrs", {})
            t = h["title"]
            kicker, title = attrs.get("kicker"), t
            m = re.match(r"^((?:Lampiran|Appendix|Lamp\.)\s+\S+)\s*·\s*(.*)$", t)
            if m and not kicker:
                kicker, title = m.group(1), m.group(2)
            if kicker is None:
                kicker = R.L["back"] if back else R.L["front"]
            nb = " nobreak" if attrs.get("nobreak") else ""
            head = (f'<div class="ch-kicker">{esc(kicker)}</div><h1 class="ch-title">{esc(title)}</h1>') if t else ""
            parts.append(f'<section class="chapter-sec{nb}" id="{h["id"]}" style="page:{phase}">{head}{R.nodes(s["body"])}</section>')
            if want_toc and toc_after and t == toc_after:
                parts.append(R.toc(entries))
    parts.append(R.back_cover())
    page_css.append(f'@page back{{@bottom-left{{content:"{back_foot}";}}}}')
    css = open(os.path.join(SKILL, "assets", "book.css"), encoding="utf-8").read()
    extra = cfg.get("extra_css", "")
    doc = (f'<!doctype html><html lang="{R.lang}"><head><meta charset="utf-8"><title>{esc(cfg["title"])}</title>'
           f'<style>{R.font_css()}{R.vars_css()}{css}{"".join(page_css)}{extra}</style></head><body>{"".join(parts)}</body></html>')
    return doc, entries
