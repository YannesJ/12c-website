// Rendert die selbst gezeichneten Display-Inhalte; Bezel-Dateien bleiben lokal.
const {chromium} = require(process.env.WATCH_PLAYWRIGHT_MODULE || 'playwright');
const fs = require('fs'), path = require('path');
const root = path.resolve(__dirname, '../..');
const copy = JSON.parse(fs.readFileSync(path.join(root, '_data/apple_watch_copy.json'), 'utf8'));
const output = process.argv[2], languages = process.argv.slice(3);
const escapeXml = text => text.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
(async () => {
  const browser = await chromium.launch({headless:true});
  try {
    const page = await browser.newPage({viewport:{width:416,height:496}, deviceScaleFactor:1});
    for (const lang of languages) for (const kind of ['single','single-done','progress','done','streak']) {
      let svg = fs.readFileSync(path.join(__dirname, 'watch-complication-screens', kind+'.svg'), 'utf8');
      for (const [key,value] of Object.entries(copy[lang].face)) svg = svg.replaceAll('@'+key.toUpperCase()+'@', escapeXml(value));
      await page.setContent('<html><body style="margin:0">'+svg+'</body></html>');
      await page.locator('svg').screenshot({path:path.join(output,kind+'-'+lang+'.png')});
    }
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });
