// Render AST -> DOCX (docx-js), mirroring the PDF design.
// Usage: node render_docx.js job.json out.docx
// job.json is written by build.py: { ast, cfg, theme, labels, pngDir, page:{w,h,mt,mr,mb,ml} }
const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell, WidthType, ShadingType,
  BorderStyle, AlignmentType, HeadingLevel, Footer, TabStopType, PageNumber, TableOfContents,
  ExternalHyperlink, LevelFormat, VerticalAlign, HorizontalPositionRelativeFrom, VerticalPositionRelativeFrom,
  SectionType, TableLayoutType, HeightRule, PageBreak,
} = require('docx');

const job = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const OUT = process.argv[3];
const { ast, cfg, theme, labels: L, pngDir, page } = job;
const hex = (c) => c.replace('#', '').toUpperCase();
const C = Object.fromEntries(Object.entries(theme.colors).filter(([k, v]) => typeof v === 'string').map(([k, v]) => [k, hex(v)]));
const SERIES = theme.colors.series.map(hex);
const FH = theme.fonts.heading, FB = theme.fonts.body, FM = theme.fonts.mono;
const HW = (theme.type || {}).headingWeight || 700;
const HB = HW >= 600; // heading fonts rendered bold?
const BASE = Math.round(((cfg.base_size || (theme.type || {}).base || 10.2)) * 2); // half-points
const TW = (mm) => Math.round(mm * 56.6929);
const PW = TW(page.w), PGH = TW(page.h);
const MARG = { top: TW(page.mt), right: TW(page.mr), bottom: TW(page.mb), left: TW(page.ml) };
const W = PW - MARG.left - MARG.right; // content width (DXA)
const W_PX = Math.round(W / 15); // DXA -> px @96dpi
const PNG = (f) => fs.readFileSync(f);
const pngSize = (buf) => ({ w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) });

const CALLOUT_COL = {
  note: ['primary2', 'primaryLight'], tip: ['success', 'successLight'], analogy: ['accentDark', 'accentLight'],
  policy: ['info', 'infoLight'], warning: ['danger', 'dangerLight'], limits: ['danger', 'dangerLight'],
  check: ['success', 'successLight'], privacy: ['neutral', 'neutralLight'], exercise: ['accentDark', 'accentLight'],
  question: ['violet', 'violetLight'], example: ['info', 'infoLight'], summary: ['accent', 'primary'],
  card: ['primary2', 'paper'], goals: ['primary', 'primaryLight'],
};

// ---------- inline ----------
const PH = /\[([^\]]+)\]/g;
const isTag = (s) => /[A-Za-z]/.test(s) && s.toUpperCase() === s;
function splitPH(text, prompt) {
  if (cfg.highlight_placeholders === false) return [{ t: text, ph: false }];
  const out = []; let last = 0; let m; PH.lastIndex = 0;
  while ((m = PH.exec(text))) {
    const ok = prompt ? !isTag(m[1]) : (/[a-z]/.test(m[1]) && m[1].length > 2);
    if (!ok) continue;
    if (m.index > last) out.push({ t: text.slice(last, m.index), ph: false });
    out.push({ t: m[0], ph: true }); last = m.index + m[0].length;
  }
  if (last < text.length) out.push({ t: text.slice(last), ph: false });
  return out;
}
const T = (text, o = {}) => new TextRun({ text, font: o.font || FB, size: o.size || BASE, color: o.color || C.ink,
  bold: !!o.bold, italics: !!o.italics, characterSpacing: o.cs, allCaps: o.caps });
function runs(rs, o = {}) {
  const out = [];
  for (const r of rs) {
    const base = { font: o.font || FB, size: o.size || BASE, color: o.color || C.ink, bold: !!(r.b || o.bold), italics: !!(r.i || o.italics) };
    if (r.code) { out.push(new TextRun({ ...base, text: r.t, font: FM, size: (o.size || BASE) - 3, shading: { type: ShadingType.CLEAR, fill: C.codeBg, color: 'auto' } })); continue; }
    if (r.href) { out.push(new ExternalHyperlink({ link: r.href, children: [new TextRun({ ...base, text: r.t, color: C.primary2, underline: {} })] })); continue; }
    for (const s of splitPH(r.t, false)) {
      if (s.ph && !o.noPH) out.push(new TextRun({ ...base, text: s.t, color: '6E430A', shading: { type: ShadingType.CLEAR, fill: 'FFE9C2', color: 'auto' } }));
      else out.push(new TextRun({ ...base, text: s.t }));
    }
  }
  return out;
}

// ---------- lists ----------
let listInstance = 0;
const numbering = { config: [
  { reference: 'bul', levels: [
    { level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 340, hanging: 220 } }, run: { color: C.primary2 } } },
    { level: 1, format: LevelFormat.BULLET, text: '–', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 680, hanging: 220 } }, run: { color: C.primary2 } } }] },
  { reference: 'num', levels: [
    { level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 300 } }, run: { color: C.primary2, bold: true, font: FH } } },
    { level: 1, format: LevelFormat.BULLET, text: '–', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 220 } }, run: { color: C.primary2 } } }] },
] };
function listParas(n, o = {}, level = 0, inst = null) {
  const out = []; const ref = n.ordered ? 'num' : 'bul';
  if (inst === null) inst = ++listInstance;
  for (const it of n.items) {
    out.push(new Paragraph({ numbering: { reference: ref, level: Math.min(level, 1), instance: inst }, spacing: { after: 60, line: 264 }, children: runs(it.runs, o) }));
    for (const ch of it.children) out.push(...listParas(ch, o, level + 1, ch.ordered === n.ordered ? inst : ++listInstance));
  }
  return out;
}

// ---------- helpers ----------
const noB = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const thin = (c = C.line) => ({ style: BorderStyle.SINGLE, size: 4, color: c });
const gap = (after = 140) => new Paragraph({ spacing: { after, line: 240 }, children: [] });
const box = (children, o = {}) => new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [W], layout: TableLayoutType.FIXED, rows: [
  new TableRow({ cantSplit: o.cantSplit !== false, children: [new TableCell({ width: { size: W, type: WidthType.DXA }, borders: o.borders,
    shading: { type: ShadingType.CLEAR, fill: o.fill || 'FFFFFF', color: 'auto' }, margins: o.margins || { top: 140, bottom: 80, left: 220, right: 220 }, children })] })] });

function colWidths(t) {
  const n = t.header.length;
  let w = t.widths && t.widths.length === n ? t.widths : null;
  const preset = { dodont: [20, 40, 40], compare: [50, 50], glossary: [26, 74], checklist: [7, 78, 15] };
  if (!w && preset[t.cls] && preset[t.cls].length === n) w = preset[t.cls];
  if (!w && t.cls === 'matrix' && n > 2) w = [20, ...Array(n - 1).fill(80 / (n - 1))];
  if (!w) {
    w = [];
    for (let c = 0; c < n; c++) {
      const cells = [t.header_text[c], ...t.rows_text.map(r => r[c] || '')];
      const avg = cells.reduce((a, x) => a + x.length, 0) / cells.length;
      const longest = Math.max(4, ...cells.flatMap(x => x.replace(/[*`]/g, '').split(/\s+/).map(wd => wd.length)));
      w.push(Math.max(6, longest * 1.6, Math.min(60, avg)));
    }
  }
  const s = w.reduce((a, b) => a + b, 0);
  const out = w.map(x => Math.round(W * x / s));
  out[out.length - 1] += W - out.reduce((a, b) => a + b, 0);
  return out;
}

function table(t) {
  const widths = colWidths(t);
  const hdrFill = (ci) => t.cls === 'dodont' && ci > 0 ? [C.success, C.danger][Math.min(ci - 1, 1)] : t.cls === 'compare' ? [C.danger, C.success][ci] || C.primary : C.primary;
  const pre = (ci) => t.cls === 'dodont' && ci > 0 ? [L.do, L.dont][Math.min(ci - 1, 1)] : t.cls === 'compare' ? [L.dont, L.do][ci] || '' : '';
  const m = { top: 70, bottom: 70, left: 110, right: 110 };
  const b = { top: thin(), bottom: thin(), left: thin(), right: thin() };
  const keyFirst = ['dodont', 'matrix', 'glossary', 'key'].includes(t.cls);
  const numFirst = ['checklist', 'numbered'].includes(t.cls);
  const sz = Math.round(BASE * 0.86);
  const header = new TableRow({ tableHeader: true, cantSplit: true, children: t.header.map((c, ci) => new TableCell({
    width: { size: widths[ci], type: WidthType.DXA }, margins: m, borders: b, verticalAlign: VerticalAlign.BOTTOM,
    shading: { type: ShadingType.CLEAR, fill: hdrFill(ci), color: 'auto' },
    children: [new Paragraph({ spacing: { after: 0, line: 252 }, children: [T(pre(ci), { color: 'FFFFFF', bold: true, size: sz, font: FH }), ...runs(c, { color: 'FFFFFF', bold: true, size: sz, font: FH, noPH: true })] })] })) });
  const rows = t.rows.map((r, ri) => new TableRow({ cantSplit: true, children: r.map((c, ci) => {
    let fill = ri % 2 === 1 ? C.zebra : 'FFFFFF';
    if (t.cls === 'dodont' && ci === 1) fill = C.successLight;
    if (t.cls === 'dodont' && ci === 2) fill = C.dangerLight;
    if (t.cls === 'compare') fill = ci === 0 ? C.dangerLight : C.successLight;
    const key = keyFirst && ci === 0, num = numFirst && ci === 0;
    const center = num || (t.cls === 'checklist' && ci === r.length - 1);
    const o = key ? { bold: true, color: C.primary, size: sz - 1, font: FH } : num ? { bold: true, color: C.accentDark, size: sz + 1, font: FH } : { size: sz };
    return new TableCell({ width: { size: widths[ci], type: WidthType.DXA }, margins: m, borders: b, shading: { type: ShadingType.CLEAR, fill, color: 'auto' },
      children: [new Paragraph({ alignment: center ? AlignmentType.CENTER : AlignmentType.LEFT, spacing: { after: 0, line: 252 }, children: runs(c, o) })] });
  }) }));
  return [new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: widths, layout: TableLayoutType.FIXED, rows: [header, ...rows] }), gap(120)];
}

function splitTitle(title) {
  const m = title.match(/^(\S+\s+[\w.\-]+)\s*·\s*(.*)$/);
  return m ? [m[1], m[2]] : ['', title];
}

function templateBox(p, isCode) {
  const [code, title] = isCode ? [p.lang || 'code', p.title] : splitTitle(p.title);
  const label = (code || L.template).toUpperCase();
  const body = [];
  for (const l of p.lines) {
    if (!isCode && l.startsWith('### ')) body.push(new Paragraph({ spacing: { before: 100, after: 20 }, keepNext: true, children: [T(l.slice(4).toUpperCase(), { bold: true, color: C.primary2, size: 15, cs: 10, font: FH })] }));
    else if (!l.trim()) body.push(new Paragraph({ spacing: { after: 0, line: 160 }, children: [] }));
    else body.push(new Paragraph({ spacing: { after: 0, line: 250 }, children: splitPH(l, !isCode).map(s => s.ph && !isCode
      ? new TextRun({ text: s.t, font: FM, size: 15, color: '6E430A', shading: { type: ShadingType.CLEAR, fill: 'FFE3B0', color: 'auto' } })
      : new TextRun({ text: s.t, font: FM, size: 15, color: C.ink })) }));
  }
  const b = { top: thin(), bottom: thin(), left: thin(), right: thin() };
  return [new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [W], layout: TableLayoutType.FIXED, rows: [
    new TableRow({ cantSplit: true, children: [new TableCell({ width: { size: W, type: WidthType.DXA }, borders: b, shading: { type: ShadingType.CLEAR, fill: C.codeHead, color: 'auto' },
      margins: { top: 90, bottom: 90, left: 160, right: 160 }, children: [new Paragraph({ spacing: { after: 0 }, keepNext: true, children: [
        new TextRun({ text: ` ${label} `, font: FH, size: 14, bold: true, color: C.ink, shading: { type: ShadingType.CLEAR, fill: C.accent, color: 'auto' } }),
        T('   ' + (title || ''), { color: 'FFFFFF', bold: true, size: 18, font: FH }),
        ...(isCode ? [] : [T('   ' + L.copy_hint, { color: 'B8C4CA', size: 13, font: FH })])] })] })] }),
    new TableRow({ children: [new TableCell({ width: { size: W, type: WidthType.DXA }, borders: b, shading: { type: ShadingType.CLEAR, fill: C.codeBg, color: 'auto' },
      margins: { top: 110, bottom: 130, left: 180, right: 180 }, children: body })] }) ] }), gap(140)];
}

function callout(c) {
  if (c.kind === 'stats') return stats(c);
  if (c.kind === 'quote') {
    const kids = [];
    (c.children || []).forEach(n => { if (n.type === 'p') kids.push(new Paragraph({ spacing: { after: 60, line: 300 }, children: runs(n.runs, { size: Math.round(BASE * 1.3), italics: true, color: C.primary }) })); });
    if (c.title) kids.push(new Paragraph({ spacing: { after: 0 }, children: [T('— ' + c.title, { size: 16, color: C.muted, font: FH })] }));
    return [box(kids, { borders: { top: noB, bottom: noB, right: noB, left: { style: BorderStyle.SINGLE, size: 36, color: C.accent } }, margins: { top: 60, bottom: 60, left: 300, right: 120 } }), gap(160)];
  }
  const [colK, lightK] = CALLOUT_COL[c.kind] || CALLOUT_COL.note;
  const col = C[colK], light = C[lightK];
  const inv = c.kind === 'summary';
  const o = inv ? { color: 'FFFFFF', size: BASE - 1 } : { size: BASE - 1 };
  const label = ((c.attrs || {}).label || L[c.kind] || '').toUpperCase();
  const kids = [];
  if (label) kids.push(new Paragraph({ spacing: { after: 20 }, keepNext: true, children: [T(label, { bold: true, color: col, size: 14, cs: 24, font: FH })] }));
  if (c.title) kids.push(new Paragraph({ spacing: { after: 80 }, keepNext: true, children: [T(c.title, { bold: true, size: inv ? BASE + 3 : BASE + 1, color: inv ? 'FFFFFF' : C.ink, font: FH })] }));
  const nodes = c.children || [];
  nodes.forEach((n, i) => {
    const last = i === nodes.length - 1;
    if (n.type === 'p') {
      if (inv && last && nodes.length > 1) kids.push(new Paragraph({ spacing: { before: 100, after: 40 }, border: { top: { style: BorderStyle.SINGLE, size: 4, color: C.primary2, space: 6 } },
        children: runs(n.runs, { color: C.accent, size: BASE - 1, font: FH }) }));
      else kids.push(new Paragraph({ spacing: { after: 90, line: 264 }, children: runs(n.runs, o) }));
    } else if (n.type === 'list') kids.push(...listParas(n, o));
    else kids.push(...block(n));
  });
  let borders;
  if (c.kind === 'card') { const d = { style: BorderStyle.DASHED, size: 12, color: C.primary2 }; borders = { top: d, bottom: d, left: d, right: d }; }
  else if (inv) borders = { top: noB, bottom: noB, left: noB, right: noB };
  else borders = { top: noB, bottom: noB, right: noB, left: { style: BorderStyle.SINGLE, size: 36, color: col } };
  return [box(kids, { borders, fill: light, cantSplit: !['exercise', 'limits'].includes(c.kind) }), gap(140)];
}

function stats(c) {
  const items = c.items || []; const n = Math.max(items.length, 1);
  const w = Array(n).fill(Math.floor(W / n)); w[n - 1] += W - w.reduce((a, b) => a + b, 0);
  const cells = items.map((it, k) => new TableCell({ width: { size: w[k], type: WidthType.DXA }, margins: { top: 140, bottom: 120, left: 160, right: 160 },
    shading: { type: ShadingType.CLEAR, fill: C.primaryLight, color: 'auto' },
    borders: { top: { style: BorderStyle.SINGLE, size: 24, color: SERIES[k % SERIES.length] }, bottom: noB, left: { style: BorderStyle.SINGLE, size: 12, color: 'FFFFFF' }, right: { style: BorderStyle.SINGLE, size: 12, color: 'FFFFFF' } },
    children: [new Paragraph({ spacing: { after: 20 }, children: [T(it.value, { bold: HB, size: Math.round(BASE * 2.1), color: C.primary, font: FH })] }),
      new Paragraph({ spacing: { after: 0 }, children: [T(it.label, { size: 16, color: C.muted, font: FH })] })] }));
  return [new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: w, layout: TableLayoutType.FIXED, rows: [new TableRow({ cantSplit: true, children: cells })] }), gap(160)];
}

let figN = 0;
function figure(n) {
  figN++;
  const ext = path.extname(n.src).toLowerCase();
  let file = path.join(pngDir, `fig-${figN}.png`), scale = 2.2;
  if (['.png', '.jpg', '.jpeg'].includes(ext) && fs.existsSync(n.src)) { file = n.src; scale = 1; }
  if (!fs.existsSync(file)) return [new Paragraph({ children: [T(`[${L.figure}: ${n.caption}]`, { italics: true, color: C.muted })] })];
  const buf = PNG(file);
  const type = ext === '.jpg' || ext === '.jpeg' ? (file === n.src ? 'jpg' : 'png') : 'png';
  let wpx, hpx;
  if (type === 'png') { const s = pngSize(buf); wpx = s.w / scale; hpx = s.h / scale; }
  else { wpx = W_PX; hpx = W_PX * 0.6; }
  const pct = n.opts && n.opts.width ? parseFloat(n.opts.width) / 100 : null;
  let width = Math.min(W_PX, pct ? W_PX * pct : wpx);
  if (scale === 1 && !pct) width = W_PX;
  const height = Math.round(hpx * width / wpx);
  const out = [new Paragraph({ alignment: AlignmentType.CENTER, keepNext: true, spacing: { before: 120, after: 40 },
    children: [new ImageRun({ type, data: buf, transformation: { width: Math.round(width), height } })] })];
  if (n.caption) out.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 }, children: [T(n.caption, { italics: true, size: 15, color: C.muted, font: FH })] }));
  return out;
}

function h2(n) {
  const m = n.text.match(/^(\d+[A-Za-z]?)\.\s+(.*)$/);
  const kids = m ? [new TextRun({ text: ` ${m[1]} `, bold: true, size: Math.round(BASE * 1.05), color: C.ink, font: FH, shading: { type: ShadingType.CLEAR, fill: C.accent, color: 'auto' } }),
    T('  ' + m[2].replace(/[*`]/g, ''), { bold: HB, size: Math.round(BASE * 1.42), color: C.primary, font: FH })]
    : runs(n.runs, { bold: HB, size: Math.round(BASE * 1.42), color: C.primary, font: FH });
  return [new Paragraph({ heading: HeadingLevel.HEADING_2, children: kids })];
}

function block(n) {
  switch (n.type) {
    case 'p': return [new Paragraph({ children: runs(n.runs) })];
    case 'h2': return h2(n);
    case 'h3': return [new Paragraph({ heading: HeadingLevel.HEADING_3, children: runs(n.runs, { bold: HB, color: C.primary2, size: Math.round(BASE * 1.1), font: FH }) })];
    case 'list': return listParas(n);
    case 'table': return table(n);
    case 'prompt': return templateBox(n, false);
    case 'code': return templateBox(n, true);
    case 'callout': return callout(n);
    case 'figure': return figure(n);
    case 'pagebreak': return [new Paragraph({ children: [new PageBreak()] })];
    default: return [];
  }
}

// ---------- chapter & part headers ----------
function chapterHead(h, noBreak, back) {
  const attrs = h.attrs || {};
  let kicker = attrs.kicker, title = h.title;
  const m = title.match(/^((?:Lampiran|Appendix|Lamp\.)\s+\S+)\s*·\s*(.*)$/);
  if (m && !kicker) kicker = m[1];
  if (!kicker) kicker = back ? L.back : L.front;
  if (!title) return [];
  return [
    new Paragraph({ pageBreakBefore: !noBreak, spacing: { before: attrs.nobreak ? 360 : 0, after: 40 }, keepNext: true, children: [T(kicker.toUpperCase(), { bold: true, color: C.accentDark, size: 16, cs: 40, font: FH })] }),
    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [T(title, { bold: HB, size: Math.round(BASE * 2.3), color: C.primary, font: FH })] }),
  ];
}

function partOpener(p, body) {
  const num = /^\d+$/.test(p.num) ? p.num.padStart(2, '0') : p.num;
  const band = new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [W], layout: TableLayoutType.FIXED, rows: [
    new TableRow({ height: { value: Math.round(PGH * 0.36), rule: HeightRule.ATLEAST }, children: [new TableCell({ width: { size: W, type: WidthType.DXA },
      borders: { top: noB, bottom: noB, left: noB, right: noB }, verticalAlign: VerticalAlign.BOTTOM,
      shading: { type: ShadingType.CLEAR, fill: C.primary, color: 'auto' }, margins: { top: 500, bottom: 600, left: 600, right: 600 },
      children: [
        new Paragraph({ spacing: { after: 0 }, children: [T((cfg.part_label || 'Bab').toUpperCase(), { bold: true, color: C.accent, size: 20, cs: 80, font: FH })] }),
        new Paragraph({ spacing: { after: 120, line: 240 }, children: [T(num, { bold: HB, color: C.accent, size: 140, font: FH })] }),
        new Paragraph({ heading: HeadingLevel.HEADING_1, border: { bottom: noB }, spacing: { after: 160 }, children: [T(p.title, { bold: HB, color: 'FFFFFF', size: 46, font: FH })] }),
        new Paragraph({ spacing: { after: 0 }, children: [T(p.subtitle || '', { color: 'E6EEF0', size: 22, font: FH })] }),
      ] })] })] });
  const goals = p.goals ? p.goals.children.flatMap(n => n.type === 'list' ? listParas(n, { size: BASE - 1 }) : block(n)) : [];
  let items = body.filter(n => n.type === 'prompt').map(n => { const [code, t] = splitTitle(n.title); return [code.replace(/^\S+\s+/, ''), t]; });
  let head = L.templates_head;
  if (!items.length) {
    head = L.contents_head;
    items = body.filter(n => n.type === 'h2').map(n => { const m = n.text.match(/^(\d+[A-Za-z]?)\.\s+(.*)$/); return m ? [m[1], m[2].replace(/[*`]/g, '')] : ['•', n.text.replace(/[*`]/g, '')]; });
  }
  const list = items.slice(0, 12).map(([a, b]) => new Paragraph({ spacing: { after: 70 }, border: { bottom: { style: BorderStyle.DASHED, size: 4, color: C.line, space: 3 } },
    children: [T(a + '  ', { bold: true, color: C.accentDark, size: 16, font: FH }), T(b, { size: 16, font: FH })] }));
  const out = [band, gap(240)];
  const cols = [];
  if (goals.length) cols.push([L.goals_head, goals, C.accent, 'FFFFFF']);
  if (list.length) cols.push([head, list, C.primary2, C.zebra]);
  if (cols.length) {
    const cw = cols.length === 2 ? [Math.round(W * 0.56), W - Math.round(W * 0.56)] : [W];
    out.push(new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: cw, layout: TableLayoutType.FIXED, rows: [new TableRow({ children: cols.map(([h, kids, top, fill], i) => new TableCell({
      width: { size: cw[i], type: WidthType.DXA }, margins: { top: 200, bottom: 160, left: 240, right: 240 }, shading: { type: ShadingType.CLEAR, fill, color: 'auto' },
      borders: { top: { style: BorderStyle.SINGLE, size: 24, color: top }, bottom: thin(), left: thin(), right: thin() },
      children: [new Paragraph({ spacing: { after: 100 }, children: [T(h, { bold: true, color: C.primary, size: BASE, font: FH })] }), ...kids] })) })] }));
  }
  out.push(new Paragraph({ children: [new PageBreak()] }));
  return out;
}

// ---------- footers & sections ----------
function footer(text) {
  return { default: new Footer({ children: [new Paragraph({ tabStops: [{ type: TabStopType.RIGHT, position: W }],
    border: { top: { style: BorderStyle.SINGLE, size: 4, color: C.line, space: 6 } },
    children: [T(text, { size: 14, color: C.muted, font: FH }), new TextRun({ children: ['\t', PageNumber.CURRENT], bold: true, size: 17, color: C.primary, font: FH })] })] }) };
}
const blankFooter = { default: new Footer({ children: [new Paragraph({ children: [] })] }) };
const props = (margin = MARG) => ({ type: SectionType.NEXT_PAGE, page: { size: { width: PW, height: PGH }, margin: { ...margin, footer: 500, header: 500 } } });
function fullPage(file) {
  const buf = PNG(file);
  const wpx = Math.round(PW / 15), hpx = Math.round(PGH / 15);
  return new Paragraph({ spacing: { after: 0 }, children: [new ImageRun({ type: 'png', data: buf, transformation: { width: wpx, height: hpx },
    floating: { horizontalPosition: { relative: HorizontalPositionRelativeFrom.PAGE, offset: 0 }, verticalPosition: { relative: VerticalPositionRelativeFrom.PAGE, offset: 0 },
      behindDocument: true, allowOverlap: true } })] });
}
const tocBlock = () => [
  new Paragraph({ spacing: { after: 40 }, children: [T(L.front.toUpperCase(), { bold: true, color: C.accentDark, size: 16, cs: 40, font: FH })] }),
  new Paragraph({ spacing: { after: 240 }, border: { bottom: { style: BorderStyle.SINGLE, size: 18, color: C.primaryLight, space: 8 } },
    children: [T(L.toc, { bold: HB, size: Math.round(BASE * 2.3), color: C.primary, font: FH })] }),
  new TableOfContents(L.toc, { hyperlink: true, headingStyleRange: '1-1' }),
];

// group AST
const groups = []; let cur = null; const pre = [];
for (const n of ast) {
  if (n.type === 'chapter' || n.type === 'part') { cur = { head: n, body: [] }; groups.push(cur); }
  else if (!cur) pre.push(n); else cur.body.push(n);
}
if (pre.length) groups.unshift({ head: { type: 'chapter', title: '', attrs: { notoc: true } }, body: pre });
const lastPart = groups.map(g => g.head.type).lastIndexOf('part');
const sections = [];
const zero = { top: 0, right: 0, bottom: 0, left: 0 };
if (fs.existsSync(path.join(pngDir, 'cover.png'))) sections.push({ properties: props(zero), footers: blankFooter, children: [fullPage(path.join(pngDir, 'cover.png'))] });

const wantToc = cfg.toc !== false; const tocAfter = cfg.toc_after;
let front = wantToc && !tocAfter ? tocBlock() : [];
let firstFront = front.length === 0;
let back = [];
const partLabel = (cfg.part_label || 'Bab'); const plTitle = partLabel.charAt(0).toUpperCase() + partLabel.slice(1).toLowerCase();
const partSections = [];
groups.forEach((g, idx) => {
  const h = g.head;
  if (h.type === 'part') {
    const short = h.short || (h.title.length < 48 ? h.title : h.title.slice(0, 45) + '…');
    partSections.push({ properties: props(), footers: footer(`${plTitle} ${h.num} · ${short}`), children: [...partOpener(h, g.body), ...g.body.flatMap(block)] });
  } else if (lastPart >= 0 && idx > lastPart) {
    back.push(...chapterHead(h, back.length === 0 || (h.attrs || {}).nobreak, true), ...g.body.flatMap(block));
  } else {
    front.push(...chapterHead(h, firstFront || (h.attrs || {}).nobreak, false), ...g.body.flatMap(block));
    firstFront = false;
    if (wantToc && tocAfter && h.title === tocAfter) { const tb = tocBlock(); tb[0] = new Paragraph({ pageBreakBefore: true, spacing: { after: 40 }, children: [T(L.front.toUpperCase(), { bold: true, color: C.accentDark, size: 16, cs: 40, font: FH })] }); front.push(...tb); }
  }
});
const foot = cfg.footer_text || cfg.title;
if (front.length) sections.push({ properties: props(), footers: footer(foot), children: front });
sections.push(...partSections);
if (back.length) sections.push({ properties: props(), footers: footer(cfg.footer_back || L.back), children: back });
if (fs.existsSync(path.join(pngDir, 'back.png'))) sections.push({ properties: props(zero), footers: blankFooter, children: [fullPage(path.join(pngDir, 'back.png'))] });

const doc = new Document({
  creator: cfg.author || cfg.title, title: cfg.title, description: cfg.subtitle || '',
  features: { updateFields: true }, numbering,
  styles: {
    default: { document: { run: { font: FB, size: BASE, color: C.ink }, paragraph: { spacing: { after: 120, line: Math.round(240 * Math.min((theme.type || {}).leading || 1.5, 1.6) * 0.8) } } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FH, size: Math.round(BASE * 2.3), bold: HB, color: C.primary },
        paragraph: { spacing: { before: 0, after: 280 }, keepNext: true, outlineLevel: 0, border: { bottom: { style: BorderStyle.SINGLE, size: 18, color: C.primaryLight, space: 8 } } } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FH, size: Math.round(BASE * 1.42), bold: HB, color: C.primary },
        paragraph: { spacing: { before: 320, after: 140 }, keepNext: true, keepLines: true, outlineLevel: 1 } },
      { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FH, size: Math.round(BASE * 1.1), bold: HB, color: C.primary2 },
        paragraph: { spacing: { before: 220, after: 90 }, keepNext: true, outlineLevel: 2 } },
      { id: 'TOC1', name: 'toc 1', basedOn: 'Normal', next: 'Normal', run: { font: FH, size: BASE }, paragraph: { spacing: { after: 80 } } },
    ],
  },
  sections,
});
Packer.toBuffer(doc).then(buf => { fs.writeFileSync(OUT, buf); console.log('docx', OUT, buf.length); });
