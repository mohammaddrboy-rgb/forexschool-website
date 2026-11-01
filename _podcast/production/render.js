const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--allow-file-access-from-files'] });
  const jobs = [['cover', 1000, 1000, 3, 'cover-3000.png'], ['show', 1000, 1000, 3, 'show-cover-3000.png'],
                ['vsq', 1000, 1000, 1.08, 'bg-square-1080.png'], ['reel', 1000, 1778, 1.08, 'bg-reel-1080x1920.png']];
  for (const [mode, w, h, scale, out] of jobs) {
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: scale });
    await p.goto('file://' + process.cwd() + '/design.html#' + mode);
    await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
    await p.locator('#card').screenshot({ path: out });
    await p.close();
  }
  await b.close();
})();
