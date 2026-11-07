// Browser audit of the deck: RTL alignment, navigation, overflow.
// Run: cd tests && npm install --ignore-scripts && npm run check
import { chromium } from 'playwright';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const HTML = fileURLToPath(new URL('../index.html', import.meta.url));
const URL_ = `file://${HTML}`;
const GUTTER_EDGE = 1512;          // 1600 stage minus the 88px gutter
const TOLERANCE = 1.5;

let failed = 0;
const check = (name, ok, detail = '') => {
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${!ok && detail ? `\n      ${detail}` : ''}`);
  if (!ok) failed++;
};

/* Static: no physical left or right in the stylesheet */
const css = readFileSync(HTML, 'utf8').match(/<style>([\s\S]*?)<\/style>/)[1]
  .replace(/\/\*[\s\S]*?\*\//g, '')
  .replace(/\.ltr-block\s*{[^}]*}/, '');          // the documented exception
const physical = css.match(/(?:^|[;{\s])(?:margin|padding|border)-(?:left|right)\b|(?:^|[;{\s])(?:left|right)\s*:|text-align:\s*(?:left|right)|float\s*:/gm) || [];
check('CSS has no physical left or right properties', physical.length === 0, physical.join(', '));

const browser = await chromium.launch({
  channel: 'chrome', headless: true,
  args: ['--enable-webgl', '--ignore-gpu-blocklist', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'],
});
const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
const errors = [];
page.on('pageerror', e => errors.push(e.message));
page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
await page.goto(URL_);
await page.evaluate(() => document.fonts.ready);

const slideCount = await page.$$eval('.slide', s => s.length);
check('Deck has 10 slides', slideCount === 10, `found ${slideCount}`);

check('Document is Hebrew and RTL', await page.evaluate(() =>
  document.documentElement.dir === 'rtl' && document.documentElement.lang === 'he'));

const fonts = await page.evaluate(() => ({
  suez: document.fonts.check('40px "Suez One"', 'אבג'),
  heebo: document.fonts.check('24px "Heebo"', 'אבג'),
}));
check('Google Fonts loaded with Hebrew glyphs', fonts.suez && fonts.heebo, JSON.stringify(fonts));

/* Per-slide audit, run inside the page */
const audit = () => {
  const slide = document.querySelector('.slide.active');
  const issues = [];
  const name = el => `${el.tagName.toLowerCase()}${el.id ? '#' + el.id : ''}${el.className && typeof el.className === 'string' ? '.' + el.className.split(' ')[0] : ''}`;
  const isLtrZone = el => el.closest('[dir="ltr"], .ltr-block');
  const visible = el => {
    const s = getComputedStyle(el), r = el.getBoundingClientRect();
    return s.visibility !== 'hidden' && s.display !== 'none' && r.width > 0 && r.height > 0;
  };

  const walker = document.createTreeWalker(slide, NodeFilter.SHOW_TEXT);
  for (let n = walker.nextNode(); n; n = walker.nextNode()) {
    const text = n.textContent.trim();
    if (!text) continue;
    const el = n.parentElement;
    if (el.closest('pre, script, style')) continue;
    const hebrew = /[֐-׿]/.test(text), latin = /[A-Za-z]/.test(text);
    // English inside a Hebrew run must be isolated, or the sentence can reorder
    if (hebrew && latin) issues.push(`unisolated English in Hebrew: "${text.slice(0, 40)}"`);
    if (latin && !hebrew && !isLtrZone(el)) issues.push(`English outside an LTR isolate: "${text.slice(0, 40)}"`);
    if (!visible(el)) continue;
    const s = getComputedStyle(el);
    if (!isLtrZone(el) && s.direction !== 'rtl') issues.push(`${name(el)} direction is ${s.direction}`);
    const centered = el.closest('button, .num, .fail');
    if (!isLtrZone(el) && !centered && !['start', 'right', '-webkit-right'].includes(s.textAlign))
      issues.push(`${name(el)} text-align is ${s.textAlign}: "${text.slice(0, 30)}"`);
  }

  // Everything stays inside the gutters and above the bottom bar
  const bar = document.querySelector('#bar').getBoundingClientRect();
  for (const el of slide.querySelectorAll('*')) {
    if (!visible(el) || el.closest('pre, svg, canvas') || el.matches('canvas')) continue;
    const r = el.getBoundingClientRect();
    if (r.right > 1512 + 1.5 || r.left < 88 - 1.5) issues.push(`${name(el)} crosses the side gutter (${r.left | 0}..${r.right | 0})`);
    if (r.bottom > bar.top + 1) issues.push(`${name(el)} runs into the bottom bar (${r.bottom | 0} > ${bar.top | 0})`);
    if (el.scrollWidth > el.clientWidth + 2 && getComputedStyle(el).overflow === 'visible' && el.clientWidth > 0 && !el.matches('span, bdi, b, i'))
      issues.push(`${name(el)} text overflows its box`);
  }

  // The header and the main content start from one shared right edge
  const edges = [...slide.querySelectorAll('.kicker, .head h2, .hero h1, .close h2')].filter(visible)
    .map(el => [name(el), el.getBoundingClientRect().right]);
  for (const [n, right] of edges)
    if (Math.abs(right - 1512) > 1.5) issues.push(`${n} right edge is ${right.toFixed(1)}, expected 1512`);
  const main = slide.querySelector('.head')?.nextElementSibling;
  if (main && Math.abs(main.getBoundingClientRect().right - 1512) > 1.5)
    issues.push(`main block right edge is ${main.getBoundingClientRect().right.toFixed(1)}`);

  // Rows read from the right: each child sits to the left of the one before it
  for (const row of slide.querySelectorAll('.ratio, .steps, .ingredients, .misses, .stack, .seg, .legend, .fields, .presets, .lab-grid, .two')) {
    if (!visible(row)) continue;
    const kids = [...row.children].filter(visible);
    for (let i = 1; i < kids.length; i++) {
      const a = kids[i - 1].getBoundingClientRect(), b = kids[i].getBoundingClientRect();
      const sameRow = Math.abs(a.top - b.top) < a.height;
      if (sameRow && b.right > a.left + 1) issues.push(`${name(row)}: child ${i + 1} is not left of child ${i}`);
    }
  }
  return issues;
};

for (let n = 1; n <= slideCount; n++) {
  await page.evaluate(n => { location.hash = '#' + n; }, n);
  await page.reload();
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(500);
  const issues = await page.evaluate(audit);
  check(`Slide ${n} RTL audit`, issues.length === 0, issues.slice(0, 8).join('\n      '));
}

/* Navigation follows reading direction */
await page.goto(URL_ + '#3'); await page.reload();
const bar = await page.evaluate(() => {
  const r = s => document.querySelector(s).getBoundingClientRect();
  const strip = [...document.querySelectorAll('#strip button')].map(b => b.getBoundingClientRect());
  return { next: r('#next'), prev: r('#prev'), first: strip[0], last: strip[9] };
});
check('Next is on the left and previous on the right', bar.next.right <= bar.prev.left);
check('Previous button sits on the content edge', Math.abs(bar.prev.right - GUTTER_EDGE) <= TOLERANCE);
check('Progress strip starts on the right', bar.first.left > bar.last.right);

const at = () => page.evaluate(() => document.documentElement.dataset.slide);
await page.keyboard.press('ArrowLeft');
check('ArrowLeft advances, as reading goes left', await at() === '4');
await page.keyboard.press('ArrowRight');
check('ArrowRight goes back', await at() === '3');
await page.click('#next');
check('Next button agrees with the keyboard', await at() === '4');
await page.click('#prev');
check('Previous button agrees with the keyboard', await at() === '3');
await page.keyboard.press('Home');
check('Previous is disabled on the first slide', await page.isDisabled('#prev'));
await page.keyboard.press('End');
check('Next is disabled on the last slide', await page.isDisabled('#next') && await at() === '10');

/* Sources drawer enters from the left, the inline end in RTL */
await page.click('#open-sources');
await page.waitForTimeout(420);
const drawer = await page.evaluate(() => document.querySelector('#sources').getBoundingClientRect().toJSON());
check('Sources drawer opens on the left edge', Math.abs(drawer.left) <= 1, `left=${drawer.left}`);
await page.keyboard.press('Escape');
await page.waitForTimeout(420);
check('Escape closes the sources drawer', await page.evaluate(() => getComputedStyle(document.querySelector('#sources')).visibility) === 'hidden');

/* Interactions */
await page.goto(URL_ + '#2'); await page.reload();
await page.click('.ing >> nth=1');
check('Ingredient card reveals its role', await page.getAttribute('.ing >> nth=1', 'aria-expanded') === 'true');
await page.goto(URL_ + '#3'); await page.reload();
const before = await page.textContent('#batch-rows');
await page.click('[data-times="10"]');
const after = await page.textContent('#batch-rows');
check('Batch size changes grams, not percentages',
  after.includes('5,000') && before.includes('100%') && after.includes('100%') && after.includes('60%'));
await page.goto(URL_ + '#6'); await page.reload();
await page.click('[data-twin="pie"]');
check('Twin toggle swaps the third ingredient', (await page.textContent('#twin-ratio')).includes('מים'));
await page.goto(URL_ + '#4'); await page.reload();
await page.click('#s4 [data-next-step]'); await page.click('#s4 [data-next-step]');
check('Steps reveal one at a time', await page.isDisabled('#s4 [data-next-step]') &&
  await page.$$eval('#s4 .step.dim', s => s.length) === 0);

/* Same layout at other window sizes */
for (const [w, h] of [[1366, 768], [1920, 1080], [1280, 800]]) {
  await page.setViewportSize({ width: w, height: h });
  await page.waitForTimeout(100);
  const fits = await page.evaluate(() => {
    const r = document.querySelector('#stage').getBoundingClientRect();
    return r.left >= -1 && r.top >= -1 && r.right <= innerWidth + 1 && r.bottom <= innerHeight + 1 &&
      Math.abs((r.left + r.right) / 2 - innerWidth / 2) < 1;
  });
  check(`Stage fits and stays centered at ${w}x${h}`, fits);
}

check('No console errors', errors.length === 0, errors.slice(0, 5).join('\n      '));
await browser.close();
console.log(failed ? `\n${failed} check(s) failed` : '\nAll checks passed');
process.exit(failed ? 1 : 0);
