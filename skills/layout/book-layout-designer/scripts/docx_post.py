"""Post-process the docx-js output.

1. Adds an explicit auto line rule to every spacing element (otherwise LibreOffice
   treats line spacing as exact and clips large text and images).
2. Bookmarks every Heading 1 and pre-fills the TOC field so the contents page is
   populated even before the reader updates fields (Word still recalculates it).
3. Embeds the theme's fonts (obfuscated per ECMA-376) so the DOCX looks like the
   PDF on machines that don't have those fonts installed.
4. Sets core document properties.

Usage: python docx_post.py raw.docx out.docx --theme theme.json [--pages pages.json] [--no-embed]
Writes out.docx.titles.json (heading texts, in order) for the page finder.
"""
import argparse, html, json, os, re, uuid, zipfile

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def fix_line(xml):
    return re.sub(r'<w:spacing((?:(?!/>)[^>])*?)w:line="(\d+)"((?:(?!/>)[^>])*)/>',
                  lambda m: m.group(0) if 'lineRule' in m.group(0) else
                  f'<w:spacing{m.group(1)}w:line="{m.group(2)}" w:lineRule="auto"{m.group(3)}/>', xml)


def add_bookmarks(doc):
    titles = []

    def repl(m):
        p = m.group(0)
        if '<w:pStyle w:val="Heading1"/>' not in p:
            return p
        text = ''.join(html.unescape(t) for t in re.findall(r'<w:t[^>]*>([^<]*)</w:t>', p))
        k = len(titles)
        titles.append(text)
        bid = 9000 + k
        p = p.replace('</w:pPr>', f'</w:pPr><w:bookmarkStart w:id="{bid}" w:name="_TocE{k}"/>', 1)
        return p[:-len('</w:p>')] + f'<w:bookmarkEnd w:id="{bid}"/></w:p>'
    doc = re.sub(r'<w:p>(?:(?!<w:p>).)*?</w:p>', repl, doc, flags=re.S)
    return doc, titles


def fill_toc(doc, titles, pages, theme, W):
    nk = lambda s: re.sub(r'\s+', '', s)
    c = theme['colors']
    prim, ink = c['primary'].lstrip('#'), c['ink'].lstrip('#')
    fh = theme['fonts']['heading']
    RF = f'<w:rFonts w:ascii="{fh}" w:cs="{fh}" w:eastAsia="{fh}" w:hAnsi="{fh}"/>'
    paras = []
    for k, t in enumerate(titles):
        pg = pages.get(nk(t)) or pages.get(nk(t.split('·', 1)[-1])) or ''
        lead = ('<w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve"> TOC \\o "1-1" \\h \\z \\u </w:instrText></w:r>'
                '<w:r><w:fldChar w:fldCharType="separate"/></w:r>') if k == 0 else ''
        paras.append(f'<w:p><w:pPr><w:pStyle w:val="TOC1"/><w:tabs><w:tab w:val="right" w:leader="dot" w:pos="{W - 10}"/></w:tabs>'
                     f'<w:spacing w:before="40" w:after="70"/></w:pPr>{lead}'
                     f'<w:hyperlink w:anchor="_TocE{k}" w:history="1"><w:r><w:rPr>{RF}<w:color w:val="{ink}"/><w:sz w:val="20"/></w:rPr>'
                     f'<w:t xml:space="preserve">{html.escape(t)}</w:t></w:r><w:r><w:rPr>{RF}<w:sz w:val="20"/></w:rPr><w:tab/></w:r>'
                     f'<w:r><w:rPr>{RF}<w:b/><w:color w:val="{prim}"/><w:sz w:val="20"/></w:rPr><w:t>{pg}</w:t></w:r></w:hyperlink></w:p>')
    if not paras:
        return doc
    paras.append('<w:p><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>')
    m = re.search(r'<w:sdtContent>.*?</w:sdtContent>', doc, flags=re.S)
    if not m:
        return doc
    return doc[:m.start()] + '<w:sdtContent>' + ''.join(paras) + '</w:sdtContent>' + doc[m.end():]


def embed_fonts(files, theme):
    reg = json.load(open(os.path.join(SKILL, 'assets', 'fonts', 'fonts.json')))
    fams = []
    for k in ('heading', 'body', 'mono'):
        f = theme['fonts'][k]
        if f in reg and f not in fams:
            fams.append(f)
    files = {n: v for n, v in files.items() if not n.startswith('word/fonts/')}
    ft = files['word/fontTable.xml'].decode('utf8')
    rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">']
    # drop any existing entries for these families (docx-js may have written some)
    for fam in fams:
        ft = re.sub(r'<w:font w:name="%s">.*?</w:font>' % re.escape(fam), '', ft, flags=re.S)
    entries, k = [], 0
    style_map = {'regular': 'Regular', 'bold': 'Bold', 'italic': 'Italic', 'boldItalic': 'BoldItalic'}
    for fam in fams:
        e = [f'<w:font w:name="{fam}"><w:charset w:val="00"/><w:family w:val="auto"/><w:pitch w:val="variable"/>']
        for key, tag in style_map.items():
            if key not in reg[fam]:
                continue
            k += 1
            g = str(uuid.uuid4()).upper()
            keyb = bytes.fromhex(g.replace('-', ''))[::-1]
            data = bytearray(open(os.path.join(SKILL, 'assets', 'fonts', reg[fam][key]), 'rb').read())
            for i in range(32):
                data[i] ^= keyb[i % 16]
            name = f'font{k}.odttf'
            files['word/fonts/' + name] = bytes(data)
            rels.append(f'<Relationship Id="rIdF{k}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/font" Target="fonts/{name}"/>')
            e.append(f'<w:embed{tag} r:id="rIdF{k}" w:fontKey="{{{g}}}"/>')
        e.append('</w:font>')
        entries.append(''.join(e))
    if 'xmlns:r=' not in ft[:600]:
        ft = ft.replace('<w:fonts ', '<w:fonts xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" ', 1)
    ft = re.sub(r'<w:fonts([^>]*?)/>', r'<w:fonts\1></w:fonts>', ft)
    ft = ft.replace('</w:fonts>', ''.join(entries) + '</w:fonts>')
    files['word/fontTable.xml'] = ft.encode('utf8')
    rels.append('</Relationships>')
    files['word/_rels/fontTable.xml.rels'] = ''.join(rels).encode('utf8')
    ct = files['[Content_Types].xml'].decode('utf8')
    ct = re.sub(r'<Override PartName="/word/fonts/[^"]*"[^>]*/>', '', ct)
    if 'Extension="odttf"' not in ct:
        ct = ct.replace('<Default ', '<Default Extension="odttf" ContentType="application/vnd.openxmlformats-officedocument.obfuscatedFont"/><Default ', 1)
    files['[Content_Types].xml'] = ct.encode('utf8')
    st = files['word/settings.xml'].decode('utf8')
    if 'embedTrueTypeFonts' not in st:
        st = re.sub(r'(<w:settings[^>]*>)', r'\1<w:embedTrueTypeFonts/>', st, 1)
    files['word/settings.xml'] = st.encode('utf8')
    return files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src'); ap.add_argument('out')
    ap.add_argument('--theme', required=True)
    ap.add_argument('--pages')
    ap.add_argument('--content-width', type=int, default=9638)
    ap.add_argument('--no-embed', action='store_true')
    a = ap.parse_args()
    theme = json.load(open(a.theme))
    pages = json.load(open(a.pages)) if a.pages and os.path.exists(a.pages) else {}
    z = zipfile.ZipFile(a.src)
    names = z.namelist()
    files = {n: z.read(n) for n in names}
    files['word/styles.xml'] = fix_line(files['word/styles.xml'].decode('utf8')).encode('utf8')
    doc = fix_line(files['word/document.xml'].decode('utf8'))
    doc, titles = add_bookmarks(doc)
    doc = fill_toc(doc, titles, pages, theme, a.content_width)
    files['word/document.xml'] = doc.encode('utf8')
    if not a.no_embed:
        files = embed_fonts(files, theme)
    order = [n for n in names if n in files] + [n for n in files if n not in names]
    with zipfile.ZipFile(a.out, 'w', zipfile.ZIP_DEFLATED) as zo:
        for n in order:
            zo.writestr(n, files[n])
    json.dump(titles, open(a.out + '.titles.json', 'w'), ensure_ascii=False)
    print(f'docx post: {len(titles)} headings, fonts embedded={not a.no_embed}, toc pages={"yes" if pages else "no"}')


if __name__ == '__main__':
    main()
