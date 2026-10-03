// Requires Playwright; PLAYWRIGHT_MODULE can point to an existing installation.
// Usage: node scripts/og-image/generate-pullup.cjs [de en ...]
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const root = path.resolve(__dirname, '../..');
const copy = JSON.parse(fs.readFileSync(path.join(root, '_data/pullup_challenge.json'), 'utf8'));
const template = fs.readFileSync(path.join(__dirname, 'pullup.html'), 'utf8');
const escape = value => value.replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]));
(async () => {
  const browser = await chromium.launch();
  try {
    const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
    for (const lang of process.argv.slice(2).length ? process.argv.slice(2) : Object.keys(copy)) {
      const values = { LABEL: copy[lang].hero_credit, IMAGE: pathToFileURL(path.join(root, 'assets/images/pullup-hero-960.webp')).href, LANG: lang, NAME: copy[lang].name, TITLE: copy[lang].title,
        FONT: pathToFileURL(path.join(root, 'assets/fonts/BricolageGrotesque.woff2')).href,
        MONO: pathToFileURL(path.join(root, 'assets/fonts/JetBrainsMono.woff2')).href };
      // File navigation allows the local font assets to load without a server.
      await page.goto(pathToFileURL(path.join(__dirname, 'pullup.html')).href);
      await page.setContent(template.replace(/\{\{(\w+)\}\}/g, (_, key) => escape(values[key])));
      await page.evaluate(() => document.fonts.ready);
      await page.locator('.art img').evaluate(image => image.decode());
      const fits = await page.evaluate(() => [...document.querySelectorAll('h1,p,.url')].every(e => e.getBoundingClientRect().bottom <= 630));
      if (!fits) throw new Error(`Sharing image text overflows: ${lang}`);
      await page.screenshot({ path: path.join(root, `assets/og-pullup-${lang}.png`) });
      console.log(`${lang}: sharing image rendered`);
    }
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
