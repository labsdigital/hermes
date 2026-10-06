// Screenshot cover, back cover and every <figure class="fig"> of book.html to PNG (used by the DOCX renderer).
// Usage: node snapshot.js book.html outDir pageWidthMm pageHeightMm
const path = require('path');
const fs = require('fs');
const { launch } = require('./browser');
(async () => {
  const [src, outDir, wmm, hmm] = process.argv.slice(2);
  fs.mkdirSync(outDir, { recursive: true });
  const w = Math.round(parseFloat(wmm) / 25.4 * 96), h = Math.round(parseFloat(hmm) / 25.4 * 96);
  const b = await launch();
  const p = await b.newPage({ deviceScaleFactor: 2.2, viewport: { width: w, height: h } });
  await p.goto('file://' + path.resolve(src), { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready);
  await p.addStyleTag({ content: `body{margin:0} .cover,.backcover{width:${w}px;height:${h}px;}` });
  const cover = await p.$('section.cover');
  if (cover) await cover.screenshot({ path: path.join(outDir, 'cover.png') });
  const back = await p.$('section.backcover');
  if (back) await back.screenshot({ path: path.join(outDir, 'back.png') });
  // figures: screenshot at a fixed content width so they match the page measure
  await p.setViewportSize({ width: 760, height: 1200 });
  const figs = await p.$$('figure.fig');
  let n = 0;
  for (const f of figs) {
    n++;
    const body = await f.$('.fig-body');
    await body.screenshot({ path: path.join(outDir, `fig-${n}.png`), omitBackground: false });
  }
  await b.close();
  console.log(`snapshots: cover=${!!cover} back=${!!back} figures=${n}`);
})().catch(e => { console.error(e); process.exit(1); });
