// Shared Chromium launcher: tries Playwright's bundled browser, then common paths / CHROMIUM_PATH.
const fs = require('fs');
async function launch() {
  let chromium;
  try { ({ chromium } = require('playwright')); }
  catch (e) { ({ chromium } = require('playwright-core')); }
  const tries = [{}];
  const cands = [process.env.CHROMIUM_PATH, '/opt/pw-browsers/chromium', '/usr/bin/chromium', '/usr/bin/chromium-browser',
    '/usr/bin/google-chrome', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'].filter(Boolean);
  for (const c of cands) if (fs.existsSync(c) && fs.statSync(c).isFile()) tries.push({ executablePath: c });
  let err;
  for (const opt of tries) {
    try { return await chromium.launch({ ...opt, args: ['--allow-file-access-from-files'] }); } catch (e) { err = e; }
  }
  throw err;
}
module.exports = { launch };
