const puppeteer = require('puppeteer');
const path = require('path');

const INPUT = path.resolve(__dirname, 'claude.html');
const OUTPUT = path.resolve(__dirname, 'claude.pdf');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  await page.goto(`file://${INPUT}`, { waitUntil: 'networkidle0' });
  await page.evaluateHandle('document.fonts.ready');

  await page.pdf({
    path: OUTPUT,
    format: 'A4',
    printBackground: true,
    margin: { top: 0, bottom: 0, left: 0, right: 0 },
    preferCSSPageSize: true,
  });

  await browser.close();
  console.log(`Exported: ${OUTPUT}`);
})();
