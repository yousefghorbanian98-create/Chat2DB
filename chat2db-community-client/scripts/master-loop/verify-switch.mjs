#!/usr/bin/env node
/**
 * Visual gate for the Motion Package switcher (G6 of the Master Loop).
 *
 * Runs against the production build served by scripts/master-loop/serve-dist.cjs.
 * Opens Settings → Motion Package, switches Data Cosmos ↔ Hyperreal and asserts:
 *   1. the section renders both package cards,
 *   2. clicking Hyperreal marks it active and writes localStorage,
 *   3. the applied CSS custom property changes on :root,
 *   4. the choice survives a page reload.
 *
 * Usage:
 *   node scripts/master-loop/verify-switch.mjs [--playwright-path <dir>] [--port 8889]
 */
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import fs from 'node:fs';

const require = createRequire(import.meta.url);
const HERE = path.dirname(fileURLToPath(import.meta.url));

const args = process.argv.slice(2);
const getArg = (name, def) => {
  const i = args.indexOf(name);
  return i >= 0 && args[i + 1] ? args[i + 1] : def;
};
const pwDir = getArg(
  '--playwright-path',
  path.resolve(HERE, '../../../master-loop-motions/node_modules/playwright'),
);
const port = Number(getArg('--port', '8889'));

const { chromium } = require(pwDir);

// The sandbox ships a headless Chromium at /tmp/chromium (used by the motion
// demo); fall back to playwright's own browser download when absent.
const CHROMIUM_BIN = process.env.CHROMIUM_BIN || (fs.existsSync('/tmp/chromium') ? '/tmp/chromium' : null);

const BASE = `http://127.0.0.1:${port}`;
const STORAGE_KEY = 'chat2db.motionPackage';

async function clickMotionPackageNav(page) {
  // The settings nav uses antd-style hashed classes; find the leaf text and
  // click its closest button (the nav item).
  return page.evaluate(() => {
    const leaf = Array.from(document.querySelectorAll('*')).find(
      (el) => el.children.length === 0 && el.textContent.trim() === 'Motion Package',
    );
    if (!leaf) return false;
    const btn = leaf.closest('button');
    if (!btn) return false;
    btn.click();
    return true;
  });
}

async function waitForNav(page, timeoutMs) {
  await page.waitForFunction(
    () => document.body && document.body.innerText.includes('Motion Package'),
    { timeout: timeoutMs },
  );
}

async function main() {
  console.log(`[verify-switch] playwright=${pwDir}`);
  const launchOpts = CHROMIUM_BIN
    ? {
        executablePath: CHROMIUM_BIN,
        args: ['--no-sandbox'],
        // The sandbox chromium needs its bundled shared libraries.
        env: { ...process.env, LD_LIBRARY_PATH: '/tmp/chromium-libs/lib' },
      }
    : { args: ['--no-sandbox'] };
  const browser = await chromium.launch(launchOpts);
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

  const results = [];
  const assert = (name, cond, extra = '') => {
    results.push({ name, ok: !!cond, extra });
    console.log(`  ${cond ? '✓' : '✗'} ${name}${extra ? ` — ${extra}` : ''}`);
  };

  try {
    // --- open settings → motion package tab
    const tabUrl = `${BASE}/settings/motionPackage`;
    console.log(`[verify-switch] opening ${tabUrl}`);
    await page.goto(tabUrl, { waitUntil: 'domcontentloaded', timeout: 120000 });
    await waitForNav(page, 300000);

    // The deep-link does not auto-activate the tab in the community layout,
    // so click the Motion Package item in the settings navigation.
    const clicked = await clickMotionPackageNav(page);
    assert('settings nav item clicked', clicked);
    await page.waitForFunction(
      () => document.querySelector('.motion-package-card') !== null,
      { timeout: 30000 },
    ).catch(() => {});

    // Section + cards rendered
    const cards = await page.$$('.motion-package-card');
    assert('two package cards rendered', cards.length === 2, `found ${cards.length}`);

    const activeCard = await page.$('.motion-package-card.active');
    assert('a card is marked active', !!activeCard);

    const cosmosLabel = await page.$eval('.motion-package-card[data-package="cosmos"] b', (el) => el.textContent);
    const hyperLabel = await page.$eval('.motion-package-card[data-package="hyper"] b', (el) => el.textContent);
    assert('labels are Data Cosmos / Hyperreal', /Data Cosmos/.test(cosmosLabel) && /Hyperreal/.test(hyperLabel), `${cosmosLabel} | ${hyperLabel}`);

    const saved = await page.evaluate((k) => localStorage.getItem(k), STORAGE_KEY);
    assert('no stale stored package before switching', saved === null || ['cosmos', 'hyper'].includes(saved), `value=${saved}`);

    const varBefore = await page.evaluate(() => document.documentElement.style.getPropertyValue('--mp-accent').trim());
    const attrBefore = await page.evaluate(() => document.documentElement.getAttribute('data-motion-package'));

    // --- switch to Hyperreal
    await page.click('.motion-package-card[data-package="hyper"]');
    await page.waitForTimeout(1200);

    const activeAfter = await page.$eval('.motion-package-card.active', (el) => el.getAttribute('data-package'));
    assert('Hyperreal card becomes active', activeAfter === 'hyper', `active=${activeAfter}`);

    const storedAfter = await page.evaluate((k) => localStorage.getItem(k), STORAGE_KEY);
    assert('localStorage updated to hyper', storedAfter === 'hyper', `value=${storedAfter}`);

    const varAfter = await page.evaluate(() => document.documentElement.style.getPropertyValue('--mp-accent').trim());
    const attrAfter = await page.evaluate(() => document.documentElement.getAttribute('data-motion-package'));
    assert('CSS var --mp-accent changed', varBefore !== varAfter && varAfter === '#a78bfa', `${varBefore} → ${varAfter}`);
    assert('data-motion-package attribute updated', attrAfter === 'hyper', `attr=${attrAfter}`);

    // --- persistence across reload
    await page.reload({ waitUntil: 'domcontentloaded' });
    await waitForNav(page, 120000);
    await clickMotionPackageNav(page);
    await page.waitForFunction(
      () => document.querySelector('.motion-package-card') !== null,
      { timeout: 30000 },
    ).catch(() => {});
    const activeAfterReload = await page.$eval('.motion-package-card.active', (el) => el.getAttribute('data-package'));
    assert('choice persisted after reload', activeAfterReload === 'hyper', `active=${activeAfterReload}`);

    // --- switch back to Data Cosmos
    await page.click('.motion-package-card[data-package="cosmos"]');
    await page.waitForTimeout(800);
    const storedBack = await page.evaluate((k) => localStorage.getItem(k), STORAGE_KEY);
    assert('switch back to cosmos persisted', storedBack === 'cosmos', `value=${storedBack}`);
  } catch (err) {
    results.push({ name: `run error: ${err.message}`, ok: false, extra: '' });
    console.error(err);
  } finally {
    await browser.close();
  }

  const passed = results.filter((r) => r.ok).length;
  const failed = results.length - passed;
  console.log(`\n[verify-switch] ${passed} passed, ${failed} failed`);
  process.exit(failed === 0 ? 0 : 1);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
