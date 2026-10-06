"""Parse the book markdown dialect into a JSON AST shared by the PDF and DOCX renderers.

See references/markdown-dialect.md for the full syntax. Usage:
    python parse_md.py chapter1.md chapter2.md ... -o ast.json
"""
import argparse, json, os, re

INLINE = re.compile(r"(`[^`]+`)|(\*\*.+?\*\*)|(\*[^*\s][^*]*?\*)|(\[[^\]]+\]\([^)]+\))")

# callout aliases (Indonesian + English) -> canonical kind
KIND_ALIAS = {
    "note": "note", "catatan": "note", "info": "note",
    "tip": "tip", "tips": "tip",
    "analogy": "analogy", "analogi": "analogy",
    "policy": "policy", "regulasi": "policy", "kebijakan": "policy",
    "warning": "warning", "peringatan": "warning", "perhatian": "warning",
    "limits": "limits", "uji": "limits", "batasan": "limits",
    "check": "check", "koreksi": "check", "praktik": "check",
    "privacy": "privacy", "privasi": "privacy",
    "exercise": "exercise", "latihan": "exercise",
    "question": "question", "dilema": "question", "refleksi": "question", "reflection": "question",
    "example": "example", "contoh": "example",
    "summary": "summary", "intisari": "summary", "ringkasan": "summary", "takeaways": "summary",
    "card": "card", "kartu": "card",
    "quote": "quote", "kutipan": "quote",
    "goals": "goals", "tujuan": "goals",
    "stats": "stats", "angka": "stats",
}
PART_TAGS = ("@part", "@modul", "@bab", "@chapter")


def inline(text, b=False, i=False):
    runs, pos = [], 0
    for m in INLINE.finditer(text):
        if m.start() > pos:
            runs.append({"t": text[pos:m.start()], "b": b, "i": i})
        tok = m.group(0)
        if m.group(1):
            runs.append({"t": tok[1:-1], "b": b, "i": i, "code": True})
        elif m.group(2):
            runs += inline(tok[2:-2], True, i)
        elif m.group(3):
            runs += inline(tok[1:-1], b, True)
        else:
            lm = re.match(r"\[([^\]]+)\]\(([^)]+)\)", tok)
            runs.append({"t": lm.group(1), "b": b, "i": i, "href": lm.group(2)})
        pos = m.end()
    if pos < len(text):
        runs.append({"t": text[pos:], "b": b, "i": i})
    return [r for r in runs if r["t"]]


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60] or "x"


def parse_attrs(s):
    """'{.cls key=val key2="a b" flag}' -> dict."""
    out = {}
    s = s.strip()[1:-1]
    for m in re.finditer(r'(\.[\w-]+)|([\w-]+)=("([^"]*)"|\S+)|([\w-]+)', s):
        if m.group(1):
            out["class"] = m.group(1)[1:]
        elif m.group(2):
            out[m.group(2)] = m.group(4) if m.group(4) is not None else m.group(3)
        elif m.group(5):
            out[m.group(5)] = True
    return out


def split_trailing_attrs(text):
    m = re.search(r"\s*(\{[^{}]*\})\s*$", text)
    if m and ("=" in m.group(1) or m.group(1).startswith("{.") or re.match(r"^\{\s*[\w-]+\s*\}$", m.group(1))):
        return text[:m.start()].strip(), parse_attrs(m.group(1))
    return text.strip(), {}


def split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


SPECIAL = re.compile(r"^(#|```|:::|@|\||\s*[-*]\s|\s*\d+\.\s|\{[.\w])")


def parse_blocks(lines, base_dir):
    nodes, i, pending = [], 0, None
    while i < len(lines):
        s = lines[i].rstrip()
        st = s.strip()
        if not st or st.startswith("<!--"):
            i += 1
            continue
        low = st.split(" ", 1)[0].lower()
        if low in PART_TAGS:
            parts = [x.strip() for x in st.split(" ", 1)[1].split("|")]
            num, title = parts[0], parts[1]
            sub = parts[2] if len(parts) > 2 else ""
            short = parts[3] if len(parts) > 3 else ""
            nodes.append({"type": "part", "num": num, "title": title, "subtitle": sub, "short": short,
                          "id": f"part-{slug(num)}"})
            i += 1
            continue
        if low == "@figure":
            parts = [x.strip() for x in st.split(" ", 1)[1].split("|")]
            src = parts[0]
            cap = parts[1] if len(parts) > 1 else ""
            opts = {}
            for p in parts[2:]:
                if "=" in p:
                    k, v = p.split("=", 1)
                    opts[k.strip()] = v.strip()
            path = src if os.path.isabs(src) else os.path.normpath(os.path.join(base_dir, src))
            nodes.append({"type": "figure", "src": path, "caption": cap, "opts": opts})
            i += 1
            continue
        if low == "@pagebreak":
            nodes.append({"type": "pagebreak"})
            i += 1
            continue
        if re.match(r"^\{[.\w][^{}]*\}$", st):
            pending = parse_attrs(st)
            i += 1
            continue
        if s.startswith("# "):
            title, attrs = split_trailing_attrs(s[2:])
            nodes.append({"type": "chapter", "title": title, "id": slug(title), "attrs": attrs})
            i += 1
            continue
        if s.startswith("## "):
            t, attrs = split_trailing_attrs(s[3:])
            nodes.append({"type": "h2", "runs": inline(t), "text": t, "id": slug(t)})
            i += 1
            continue
        if s.startswith("### "):
            t, attrs = split_trailing_attrs(s[4:])
            nodes.append({"type": "h3", "runs": inline(t), "text": t})
            i += 1
            continue
        if st.startswith("```"):
            info = st[3:].strip()
            lang, _, title = info.partition(" ")
            body = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                body.append(lines[i].rstrip("\n"))
                i += 1
            i += 1
            while body and not body[-1].strip():
                body.pop()
            if lang.lower() in ("prompt", "template"):
                nodes.append({"type": "prompt", "title": title.strip(), "lines": body})
            else:
                nodes.append({"type": "code", "lang": lang, "title": title.strip(), "lines": body})
            continue
        if st.startswith(":::") and st != ":::":
            m = re.match(r":::(\w+)(\{[^}]*\})?\s*(.*)", st)
            raw_kind, attr_s, title = m.group(1).lower(), m.group(2), m.group(3).strip()
            attrs = parse_attrs(attr_s) if attr_s else {}
            body, depth = [], 0
            i += 1
            while i < len(lines):
                l = lines[i].strip()
                if l == ":::" and depth == 0:
                    break
                if l.startswith(":::") and l != ":::":
                    depth += 1
                elif l == ":::":
                    depth -= 1
                body.append(lines[i])
                i += 1
            i += 1
            kind = KIND_ALIAS.get(raw_kind, "note")
            node = {"type": "callout", "kind": kind, "title": title, "attrs": attrs}
            if kind == "stats":
                items = []
                for l in body:
                    l = l.strip()
                    if l.startswith(("-", "*")):
                        v, _, lab = l[1:].strip().partition("|")
                        items.append({"value": v.strip(), "label": lab.strip()})
                node["items"] = items
            else:
                node["children"] = parse_blocks(body, base_dir)
            nodes.append(node)
            continue
        if st.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            header = rows[0]
            body = [r for r in rows[1:] if not all(re.match(r"^:?-{2,}:?$", c) for c in r)]
            attrs = pending or {}
            widths = None
            if attrs.get("widths"):
                widths = [float(x) for x in str(attrs["widths"]).split(",")]
            nodes.append({"type": "table", "cls": attrs.get("class", "default"), "widths": widths,
                          "header": [inline(c) for c in header], "header_text": header,
                          "rows": [[inline(c) for c in r] for r in body], "rows_text": body})
            pending = None
            continue
        if re.match(r"^(\s*)([-*]|\d+\.)\s+", s):
            lst, i = parse_list(lines, i, len(re.match(r"^(\s*)", s).group(1)))
            if pending and pending.get("class") == "steps":
                lst["steps"] = True
                pending = None
            nodes.append(lst)
            continue
        para = [st]
        i += 1
        while i < len(lines) and lines[i].strip() and not SPECIAL.match(lines[i]):
            para.append(lines[i].strip())
            i += 1
        nodes.append({"type": "p", "runs": inline(" ".join(para))})
    return nodes


def parse_list(lines, i, indent):
    first = re.match(r"^(\s*)([-*]|\d+\.)\s+", lines[i])
    ordered = first.group(2)[0].isdigit()
    items = []
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            j = i + 1
            if j < len(lines) and re.match(r"^\s*([-*]|\d+\.)\s+", lines[j]) \
                    and len(re.match(r"^(\s*)", lines[j]).group(1)) == indent:
                i = j
                continue
            break
        m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)", line)
        if not m:
            if items and len(re.match(r"^(\s*)", line).group(1)) > indent:
                # continuation line of previous item
                items[-1]["runs"] += inline(" " + line.strip())
                items[-1]["text"] += " " + line.strip()
                i += 1
                continue
            break
        ind = len(m.group(1))
        if ind < indent:
            break
        if ind > indent:
            sub, i = parse_list(lines, i, ind)
            items[-1]["children"].append(sub)
            continue
        items.append({"runs": inline(m.group(3)), "text": m.group(3), "children": []})
        i += 1
    return {"type": "list", "ordered": ordered, "items": items}, i


def attach_goals(nodes):
    out = []
    for n in nodes:
        if n["type"] == "callout" and n["kind"] == "goals" and out and out[-1]["type"] == "part" \
                and "goals" not in out[-1]:
            out[-1]["goals"] = n
            continue
        out.append(n)
    return out


def parse_files(paths):
    nodes = []
    for f in paths:
        with open(f, encoding="utf-8") as fh:
            text = fh.read()
        # optional YAML-ish front matter is ignored
        if text.startswith("---\n"):
            end = text.find("\n---", 4)
            if end > 0:
                text = text[end + 4:]
        nodes += parse_blocks(text.split("\n"), os.path.dirname(os.path.abspath(f)))
    return attach_goals(nodes)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("-o", "--out", required=True)
    a = ap.parse_args()
    ast = parse_files(a.files)
    json.dump(ast, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    kinds = {}
    for n in ast:
        kinds[n["type"]] = kinds.get(n["type"], 0) + 1
    print(kinds)
