"""Find the page number of every top-level heading.

  python pages.py outline book.pdf pages.json          # from PDF bookmarks (Chromium output)
  python pages.py search rendered.pdf titles.json pages.json   # by text search (LibreOffice render of the DOCX)
Keys are heading texts with all whitespace removed.
"""
import json, re, sys, warnings
warnings.filterwarnings("ignore")
nk = lambda s: re.sub(r"\s+", "", s)


def outline(pdf, out):
    from pypdf import PdfReader
    r = PdfReader(pdf)
    pages = {}
    for it in r.outline:
        if isinstance(it, list):
            continue
        try:
            pages[nk(it.title)] = r.get_destination_page_number(it) + 1
        except Exception:
            pass
    json.dump(pages, open(out, "w"), ensure_ascii=False, indent=1)
    return len(r.pages), pages


def search(pdf, titles_path, out, toc_word):
    import pdfplumber
    titles = json.load(open(titles_path))
    with pdfplumber.open(pdf) as p:
        texts = [nk(pg.extract_text() or "") for pg in p.pages]
    toc_pages = {i for i, t in enumerate(texts) if nk(toc_word) in t[:80]}
    res, cur = {}, 0
    for t in titles:
        key = nk(t)
        for i in range(cur, len(texts)):
            if i in toc_pages:
                continue
            if key and key in texts[i]:
                res[key] = i + 1
                cur = i
                break
    json.dump(res, open(out, "w"), ensure_ascii=False, indent=1)
    return len(texts), res


if __name__ == "__main__":
    if sys.argv[1] == "outline":
        n, p = outline(sys.argv[2], sys.argv[3])
    else:
        n, p = search(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else "Daftar Isi")
    print(f"{n} pages, {len(p)} headings located")
