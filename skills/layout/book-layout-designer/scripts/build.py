"""One-command build: markdown chapters + book.yaml -> PDF and/or DOCX with book layout.

  python build.py path/to/book.yaml [--out DIR] [--formats pdf,docx] [--theme NAME]
                  [--no-embed] [--preview] [--keep]

See SKILL.md for the workflow and references/ for the dialect and design system.
"""
import argparse, glob, json, os, shutil, subprocess, sys, tempfile, warnings
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import parse_md, render_html, pages as pagesmod  # noqa: E402


def load_config(path):
    text = open(path, encoding="utf-8").read()
    if path.endswith((".yaml", ".yml")):
        import yaml
        cfg = yaml.safe_load(text)
    else:
        cfg = json.loads(text)
    cfg["_dir"] = os.path.dirname(os.path.abspath(path))
    return cfg


def load_theme(cfg, override=None):
    name = override or cfg.get("theme", "edukasi")
    p = name if os.path.exists(name) else os.path.join(cfg["_dir"], name)
    if not os.path.exists(p):
        p = os.path.join(SKILL, "assets", "themes", f"{name}.json")
    theme = json.load(open(p))
    ov = cfg.get("theme_overrides") or {}
    for k in ("colors", "fonts", "type"):
        theme.setdefault(k, {}).update(ov.get(k, {}))
    return theme


def chapter_files(cfg):
    pats = cfg.get("chapters") or ["chapters/*.md"]
    files = []
    for p in pats:
        full = p if os.path.isabs(p) else os.path.join(cfg["_dir"], p)
        hits = sorted(glob.glob(full))
        files += hits if hits else ([full] if os.path.exists(full) else [])
    if not files:
        sys.exit(f"No chapter files found for {pats}")
    return files


def node_env():
    env = dict(os.environ)
    extra = [os.path.join(SKILL, "node_modules")]
    try:
        extra.append(subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip())
    except Exception:
        pass
    env["NODE_PATH"] = os.pathsep.join(filter(None, [env.get("NODE_PATH")] + extra))
    return env


def node(script, *args):
    r = subprocess.run(["node", os.path.join(HERE, script), *map(str, args)], env=node_env(), capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"{script} failed:\n{r.stderr[-3000:]}")
    return r.stdout.strip()


def soffice_pdf(docx, outdir):
    exe = shutil.which("soffice") or shutil.which("libreoffice")
    if not exe:
        return None
    home = tempfile.mkdtemp()
    subprocess.run([exe, "--headless", "--convert-to", "pdf", "--outdir", outdir, docx], env=dict(os.environ, HOME=home),
                   capture_output=True, timeout=600)
    pdf = os.path.join(outdir, os.path.splitext(os.path.basename(docx))[0] + ".pdf")
    return pdf if os.path.exists(pdf) else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--out")
    ap.add_argument("--formats")
    ap.add_argument("--theme")
    ap.add_argument("--no-embed", action="store_true", help="do not embed fonts in the DOCX")
    ap.add_argument("--preview", action="store_true", help="write contact sheets for visual QA")
    ap.add_argument("--keep", action="store_true", help="keep the _build work folder")
    a = ap.parse_args()

    cfg = load_config(a.config)
    theme = load_theme(cfg, a.theme)
    out = os.path.abspath(a.out or os.path.join(cfg["_dir"], cfg.get("output", {}).get("dir", "out")))
    work = os.path.join(out, "_build")
    os.makedirs(work, exist_ok=True)
    fmts = (a.formats or ",".join(cfg.get("output", {}).get("formats", ["pdf", "docx"]))).split(",")
    name = cfg.get("output", {}).get("name") or "".join(ch if ch.isalnum() else "-" for ch in cfg["title"]).strip("-")
    name = "-".join(filter(None, name.split("-")))

    json.dump(theme, open(os.path.join(work, "theme.json"), "w"), ensure_ascii=False, indent=1)
    files = chapter_files(cfg)
    ast = parse_md.parse_files(files)
    json.dump(ast, open(os.path.join(work, "ast.json"), "w"), ensure_ascii=False)
    print(f"parsed {len(files)} file(s): {sum(1 for n in ast if n['type'] == 'part')} parts, "
          f"{sum(1 for n in ast if n['type'] == 'chapter')} chapters, {sum(1 for n in ast if n['type'] == 'prompt')} templates")

    # ---- HTML + PDF (two passes so the TOC gets real page numbers) ----
    html_path = os.path.join(work, "book.html")
    doc, _ = render_html.render(ast, cfg, theme)
    open(html_path, "w", encoding="utf-8").write(doc)
    results = []
    if "pdf" in fmts:
        p1 = os.path.join(work, "pass1.pdf")
        node("render_pdf.js", html_path, p1)
        n, pages = pagesmod.outline(p1, os.path.join(work, "pages.json"))
        doc, _ = render_html.render(ast, cfg, theme, pages)
        open(html_path, "w", encoding="utf-8").write(doc)
        final = os.path.join(work, "book.pdf")
        node("render_pdf.js", html_path, final)
        n2, pages2 = pagesmod.outline(final, os.path.join(work, "pages_check.json"))
        if pages2 != pages:  # rare: TOC length changed pagination -> one more pass
            doc, _ = render_html.render(ast, cfg, theme, pages2)
            open(html_path, "w", encoding="utf-8").write(doc)
            node("render_pdf.js", html_path, final)
        from pypdf import PdfReader, PdfWriter
        w = PdfWriter(clone_from=PdfReader(final))
        w.add_metadata({"/Title": cfg["title"], "/Subject": cfg.get("subtitle", ""), "/Author": cfg.get("author", cfg["title"]),
                        "/Keywords": ", ".join(cfg.get("keywords", []))})
        pdf_out = os.path.join(out, name + ".pdf")
        w.write(pdf_out)
        results.append(pdf_out)
        print(f"PDF  {pdf_out}  ({n2} pages)")

    # ---- DOCX ----
    if "docx" in fmts:
        size = cfg.get("page_size", "A4")
        pw, ph, (mt, mr, mb, ml), _, _ = render_html.PAGE.get(size, render_html.PAGE["A4"])
        png = os.path.join(work, "png")
        print(node("snapshot.js", html_path, png, pw, ph))
        L = dict(render_html.LABELS.get(cfg.get("lang", "id"), render_html.LABELS["id"]))
        L.update(cfg.get("labels", {}))
        job = {"ast": ast, "cfg": {k: v for k, v in cfg.items() if not k.startswith("_")}, "theme": theme, "labels": L,
               "pngDir": png, "page": {"w": pw, "h": ph, "mt": mt, "mr": mr, "mb": mb, "ml": ml}}
        jp = os.path.join(work, "job.json")
        json.dump(job, open(jp, "w"), ensure_ascii=False)
        raw = os.path.join(work, "raw.docx")
        node("render_docx.js", jp, raw)
        tp = os.path.join(work, "theme.json")
        cw = round((pw - ml - mr) * 56.6929)
        emb = ["--no-embed"] if a.no_embed else []
        post = [sys.executable, os.path.join(HERE, "docx_post.py")]
        p1 = os.path.join(work, "pass1.docx")
        subprocess.run(post + [raw, p1, "--theme", tp, "--content-width", str(cw)] + emb, check=True, capture_output=True)
        docx_out = os.path.join(out, name + ".docx")
        rendered = soffice_pdf(p1, work)
        pages_json = os.path.join(work, "docx_pages.json")
        if rendered:
            pagesmod.search(rendered, p1 + ".titles.json", pages_json, L["toc"])
            r = subprocess.run(post + [raw, docx_out, "--theme", tp, "--pages", pages_json, "--content-width", str(cw)] + emb,
                               check=True, capture_output=True, text=True)
        else:
            r = subprocess.run(post + [raw, docx_out, "--theme", tp, "--content-width", str(cw)] + emb, check=True, capture_output=True, text=True)
        print(r.stdout.strip())
        results.append(docx_out)
        print(f"DOCX {docx_out}")
        if a.preview:
            rp = soffice_pdf(docx_out, work)
            if rp:
                sheets = subprocess.run([sys.executable, os.path.join(HERE, "preview.py"), rp, os.path.join(out, "preview-docx")],
                                        capture_output=True, text=True).stdout
                print("DOCX preview sheets:\n" + sheets)
    if a.preview and "pdf" in fmts:
        sheets = subprocess.run([sys.executable, os.path.join(HERE, "preview.py"), os.path.join(out, name + ".pdf"),
                                 os.path.join(out, "preview-pdf")], capture_output=True, text=True).stdout
        print("PDF preview sheets:\n" + sheets)
    if not a.keep:
        for f in ("pass1.pdf", "pass1.docx", "raw.docx", "job.json"):
            try:
                os.remove(os.path.join(work, f))
            except OSError:
                pass
    print("done:", *results, sep="\n  ")


if __name__ == "__main__":
    main()
