// Records the demo video and README screenshots from the real deck.
// Run: cd tests && node record_demo.mjs <output-folder>
import { chromium } from 'playwright';
import { fileURLToPath } from 'node:url';

const out = process.argv[2];
const url = `file://${fileURLToPath(new URL('../index.html', import.meta.url))}`;
const browser = await chromium.launch({ channel: 'chrome', headless: true });
const context = await browser.newContext({
  viewport: { width: 1600, height: 900 },
  recordVideo: { dir: out, size: { width: 1600, height: 900 } },
});
const page = await context.newPage();
const started = Date.now();
const mark = label => console.log(`${label} ${((Date.now() - started) / 1000).toFixed(1)}`);
const pause = ms => page.waitForTimeout(ms);
const shot = name => page.screenshot({ path: `${out}/${name}.png` });
const next = async (wait = 1100) => { await page.click('#next'); await pause(wait); };

await page.goto(url);
await page.evaluate(() => document.fonts.ready);
await page.waitForFunction(() => window.bakery, null, { timeout: 60000 });
await pause(1800);
await shot('slide-01');

await next();                                        // 2
for (let i = 0; i < 5; i++) { await page.click(`.ing >> nth=${i}`); await pause(420); }
await pause(700);
await shot('slide-02');

await next();                                        // 3
await page.click('[data-times="2"]'); await pause(800);
await page.click('[data-times="10"]'); await pause(1200);
await shot('slide-03');

await next();                                        // 4
for (let i = 0; i < 2; i++) { await page.click('#s4 [data-next-step]'); await pause(800); }
await next();                                        // 5
for (let i = 0; i < 2; i++) { await page.click('#s5 [data-next-step]'); await pause(800); }
await next();                                        // 6
await page.click('[data-twin="pie"]'); await pause(1200);
await page.click('[data-twin="cookie"]'); await pause(900);
await page.click('[data-twin="pie"]'); await pause(800);

mark('oven');
await next(300);                                     // 7
await page.waitForFunction(() => bakery.stats.bakes > 0 && !bakery.stats.running, null, { timeout: 20000 });
await pause(500);
await page.click('#bake-family [data-family="pie"]');
await page.waitForFunction(() => !bakery.stats.running, null, { timeout: 20000 });
const view = await page.locator('[data-viewport="oven"]').boundingBox();
await page.mouse.move(view.x + view.width * .6, view.y + view.height * .55);
await page.mouse.down();
await page.mouse.move(view.x + view.width * .3, view.y + view.height * .5, { steps: 24 });
await page.mouse.up();
await pause(500);
await shot('slide-07');

mark('lab');
await next(900);                                     // 8
await page.waitForSelector('#py-status[data-state="ready"]', { state: 'attached', timeout: 90000 });
await page.click('[data-preset="genoise"]'); await pause(1300);
await page.click('[data-preset="shortbread"]'); await pause(1300);
await page.click('[data-preset="all_butter_crust"]'); await pause(1300);
await page.click('[data-preset="brioche"]'); await pause(1500);
await shot('slide-08');
await page.click('[data-preset="baguette"]'); await pause(1100);
const fat = await page.locator('#sliders input[data-ing="fat"]').boundingBox();
await page.mouse.move(fat.x + fat.width - 6, fat.y + fat.height / 2);
await page.mouse.down();
await page.mouse.move(fat.x + fat.width * .55, fat.y + fat.height / 2, { steps: 40 });
await page.mouse.up();
await pause(1200);
await page.click('#lab-reset'); await pause(800);
await page.click('#lab-double'); await pause(1200);
await page.click('#lab-code-toggle'); await pause(1800);
await page.click('#lab-code-toggle'); await pause(500);
mark('labEnd');

await next(2600);                                    // 9
await shot('slide-09');
await next(800);                                     // 10
for (const [ingredient, grams] of [['flour', '300'], ['fat', '200'], ['sugar', '150'], ['egg', '100']]) {
  await page.fill(`#yours input[data-ing="${ingredient}"]`, grams);
  await pause(300);
}
await page.click('#yours button[type="submit"]');
await pause(1500);
await page.click('#yours-challah');
await pause(2600);
await shot('slide-10');
mark('end');

await context.close();
await browser.close();
