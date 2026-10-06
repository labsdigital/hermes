// Usage: node render_pdf.js book.html out.pdf
const path = require('path');
const { launch } = require('./browser');
(async () => {
  const [src, out] = process.argv.slice(2);
  const b = await launch();
  const p = await b.newPage();
  await p.goto('file://' + path.resolve(src), { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: out, preferCSSPageSize: true, printBackground: true, outline: true, tagged: true });
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
