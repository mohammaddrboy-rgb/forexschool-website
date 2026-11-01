const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--allow-file-access-from-files'] });
  const p = await b.newPage({ viewport: { width: 1000, height: 1778 }, deviceScaleFactor: 1.08 });
  await p.goto('file://' + process.cwd() + '/design.html#reelcover');
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
  await p.locator('#card').screenshot({ path: 'rc-bg.png' });
  const z = await p.evaluate(() => { const r = document.querySelector('.wavezone').getBoundingClientRect(); return [r.left, r.top, r.width, r.height]; });
  console.log(JSON.stringify(z.map(v => Math.round(v * 1.08))));
  await b.close();
})();
