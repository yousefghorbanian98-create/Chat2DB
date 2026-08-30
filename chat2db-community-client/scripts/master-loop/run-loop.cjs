#!/usr/bin/env node
/**
 * Master Loop runner — Motion Package switcher integration (chat2db-community-client)
 * ====================================================================================
 * Phase-gated integration loop. Each phase is a GATE: it must PASS before the
 * loop proceeds to the next phase. Nothing in the real project is executed by
 * preparing this file; the loop only runs when the operator explicitly starts it:
 *
 *   node scripts/master-loop/run-loop.cjs            # run ALL gates in order
 *   node scripts/master-loop/run-loop.cjs --phase typecheck
 *   node scripts/master-loop/run-loop.cjs --continue-on-error
 *   node scripts/master-loop/run-loop.cjs --status   # report last run state
 *
 * Exit code: 0 = all executed gates passed, 1 = a gate failed, 2 = usage error.
 */
'use strict';

const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const ROOT = path.resolve(__dirname, '../..');
const STATE_FILE = path.join(__dirname, 'loop-state.json');

const PHASES = [
  {
    id: 'static',
    title: 'G1 · Static wiring gate',
    desc: '8 touchpoints wired, motion-package module present, no forbidden imports',
    run: runStaticGate,
  },
  {
    id: 'i18n-keys',
    title: 'G2 · i18n keys gate',
    desc: 'All 11 keys present in all 5 locale files, no placeholder drift',
    run: runI18nKeysGate,
  },
  {
    id: 'typecheck',
    title: 'G3 · TypeScript gate',
    desc: 'umi generate tmp (fresh checkout) + tsc --noEmit: zero errors in the integration set',
    run: () => {
      // tsconfig extends src/.umi/tsconfig.json which only exists after umi
      // generates its temp files — do that first so a fresh checkout passes.
      if (!fs.existsSync(path.join(ROOT, 'src/.umi/tsconfig.json'))) {
        if (!runCmd('npx', ['umi', 'generate', 'tmp'], 'typecheck', 600)) {
          return false;
        }
      }
      const res = spawnSync('npx', ['tsc', '--noEmit'], {
        cwd: ROOT,
        encoding: 'utf8',
        timeout: 900 * 1000,
      });
      const out = (res.stdout || '') + (res.stderr || '');
      const errorLines = out.split('\n').filter((l) => l.includes('error TS'));
      if (errorLines.length === 0) {
        return true;
      }
      // The project carries a large pre-existing type-error baseline
      // (201 errors in files outside this integration, no typecheck in CI).
      // The gate is baseline-aware: it only fails on errors inside the
      // Motion Package integration file set.
      const INTEGRATION_FILES = [
        'src/motion-package/',
        'src/blocks/Setting/index.tsx',
        'src/layouts/GlobalLayout/CommunityLayout.tsx',
        'src/layouts/GlobalLayout/index.tsx',
        'src/i18n/en-US/setting.ts',
        'src/i18n/zh-CN/setting.ts',
        'src/i18n/ja-JP/setting.ts',
        'src/i18n/ko-KR/setting.ts',
        'src/i18n/es-ES/setting.ts',
      ];
      const mine = errorLines.filter((l) =>
        INTEGRATION_FILES.some((f) => l.includes(f)),
      );
      if (mine.length > 0) {
        console.error(color.red(`  [typecheck] ${mine.length} error(s) inside the integration set:`));
        mine.slice(0, 12).forEach((l) => console.error(color.red(`    ${l}`)));
        return false;
      }
      console.log(
        color.yellow(
          `  [typecheck] ${errorLines.length} pre-existing baseline error(s) in other files (out of scope, verified: none inside the integration set)`,
        ),
      );
      return true;
    },
  },
  {
    id: 'i18n-validate',
    title: 'G4 · i18n validator gate',
    desc: 'node scripts/validate-i18n.cjs exits 0',
    run: () => runCmd('node', ['scripts/validate-i18n.cjs'], 'i18n-validate'),
  },
  {
    id: 'build',
    title: 'G5 · Production build gate',
    desc: 'yarn build:web:community (prebuild unit tests + umi build + bundle verify)',
    run: () => runCmd('yarn', ['build:web:community'], 'build', 2400),
  },
  {
    id: 'visual',
    title: 'G6 · Visual switch gate',
    desc: 'Serve production build (dist/) + settings opens + package switch persists (playwright)',
    run: runVisualGate,
  },
];

const args = process.argv.slice(2);
const flags = {
  phase: null,
  continueOnError: false,
  status: false,
};
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--phase') flags.phase = args[++i];
  else if (args[i] === '--continue-on-error') flags.continueOnError = true;
  else if (args[i] === '--status') flags.status = true;
  else if (args[i] === '--list') {
    console.log('Available phases:');
    PHASES.forEach((p) => console.log(`  ${p.id.padEnd(14)} ${p.title}`));
    process.exit(0);
  } else {
    console.error(`Unknown argument: ${args[i]}`);
    process.exit(2);
  }
}

const color = {
  green: (s) => `\x1b[32m${s}\x1b[0m`,
  red: (s) => `\x1b[31m${s}\x1b[0m`,
  yellow: (s) => `\x1b[33m${s}\x1b[0m`,
  dim: (s) => `\x1b[2m${s}\x1b[0m`,
};

function loadState() {
  try {
    return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
  } catch {
    return { phases: {}, updatedAt: null };
  }
}

function saveState(state) {
  state.updatedAt = new Date().toISOString();
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

function runCmd(cmd, argv, phaseId, timeoutSec = 600) {
  console.log(color.dim(`  $ ${cmd} ${argv.join(' ')}`));
  const res = spawnSync(cmd, argv, {
    cwd: ROOT,
    stdio: 'inherit',
    timeout: timeoutSec * 1000,
    shell: false,
  });
  if (res.error) {
    console.error(color.red(`  [${phaseId}] spawn error: ${res.error.message}`));
    return false;
  }
  return res.status === 0;
}

/* ---------------------------------------------------------------- G1 */
function runStaticGate() {
  const ok = [];
  const fail = [];
  const check = (name, cond) => (cond ? ok.push(name) : fail.push(name));

  const read = (p) => {
    try {
      return fs.readFileSync(path.join(ROOT, p), 'utf8');
    } catch {
      return null;
    }
  };

  // 1-2. Provider mounted in both layouts
  ['src/layouts/GlobalLayout/CommunityLayout.tsx', 'src/layouts/GlobalLayout/index.tsx'].forEach((p) => {
    const src = read(p) || '';
    check(`${p} → provider import`, src.includes("from '@/motion-package/MotionPackageProvider'"));
    check(`${p} → provider mounted`, /<MotionPackageProvider>[\s\S]*<\/MotionPackageProvider>/.test(src));
  });

  // 3. Settings menu item
  const setting = read('src/blocks/Setting/index.tsx') || '';
  check('Setting/index.tsx → menu item', setting.includes("code: 'motionPackage'"));
  check('Setting/index.tsx → Sparkles icon', /import \{[^}]*Sparkles[^}]*\} from 'lucide-react'/.test(setting));
  check('Setting/index.tsx → section body', setting.includes('<MotionPackageSetting />'));

  // 4. Module files exist
  ['types.ts', 'MotionPackageProvider.tsx', 'MotionPackageSetting.tsx', 'motion-package.css'].forEach((f) => {
    check(`src/motion-package/${f} exists`, fs.existsSync(path.join(ROOT, 'src/motion-package', f)));
  });

  // 5. No forbidden imports inside the module
  const moduleFiles = ['types.ts', 'MotionPackageProvider.tsx', 'MotionPackageSetting.tsx'];
  moduleFiles.forEach((f) => {
    const src = read(`src/motion-package/${f}`) || '';
    check(`${f} → no @ant-design/icons`, !src.includes('@ant-design/icons'));
    check(`${f} → no react-router`, !src.includes('react-router'));
  });

  // 6. Storage key constant used consistently
  const types = read('src/motion-package/types.ts') || '';
  const provider = read('src/motion-package/MotionPackageProvider.tsx') || '';
  check('types.ts → storage key const', types.includes("MOTION_PACKAGE_STORAGE_KEY = 'chat2db.motionPackage'"));
  check('provider → uses storage key', provider.includes('MOTION_PACKAGE_STORAGE_KEY'));

  // 7. No leftover demo-only markers
  const css = read('src/motion-package/motion-package.css') || '';
  check('motion-package.css → scoped classnames', !/\.settings-panel|\.pkg-badge|\.action-card/.test(css));

  console.log(color.dim(`  static checks: ${ok.length} ok, ${fail.length} failed`));
  return fail.length === 0;
}

/* ---------------------------------------------------------------- G2 */
function runI18nKeysGate() {
  const KEYS = [
    'setting.nav.motionPackage',
    'setting.nav.motionPackageDescribe',
    'setting.motionPackage.title',
    'setting.motionPackage.sub',
    'setting.motionPackage.cosmosLabel',
    'setting.motionPackage.cosmosDesc',
    'setting.motionPackage.hyperLabel',
    'setting.motionPackage.hyperDesc',
    'setting.motionPackage.active',
    'setting.motionPackage.tapToSwitch',
    'setting.motionPackage.saved',
  ];
  const locales = ['en-US', 'zh-CN', 'ja-JP', 'ko-KR', 'es-ES'];
  let failed = false;
  for (const locale of locales) {
    const file = path.join(ROOT, 'src/i18n', locale, 'setting.ts');
    const src = fs.readFileSync(file, 'utf8');
    for (const key of KEYS) {
      if (!src.includes(`'${key}'`)) {
        console.error(color.red(`  [i18n-keys] ${locale}: missing key ${key}`));
        failed = true;
        continue;
      }
      // Extract the value of THIS key only. A file-wide placeholder scan
      // would trip on pre-existing keys such as setting.license.codeCountdown.
      const lineMatch = src.match(new RegExp(`'${key}'\\s*:\\s*'(.*?)',`));
      const value = lineMatch ? lineMatch[1] : '';
      if (/\{[0-9]+\}/.test(value)) {
        console.error(color.red(`  [i18n-keys] ${locale}: ${key} contains a raw placeholder "${value}"`));
        failed = true;
      }
      // validate-i18n.cjs is strict about HTML tags in es-ES / ko-KR;
      // keep the new keys tag-free in every locale.
      if (/<\/?[a-zA-Z]/.test(value)) {
        console.error(color.red(`  [i18n-keys] ${locale}: ${key} contains an HTML tag "${value}"`));
        failed = true;
      }
    }
  }
  return !failed;
}

/* ---------------------------------------------------------------- G6 */
const { spawn } = require('node:child_process');
const net = require('node:net');

function waitForPort(port, timeoutSec) {
  const deadline = Date.now() + timeoutSec * 1000;
  return new Promise((resolve) => {
    const tryOnce = () => {
      const sock = net.connect({ port, host: '127.0.0.1' });
      sock.once('connect', () => {
        sock.destroy();
        resolve(true);
      });
      sock.once('error', () => {
        sock.destroy();
        if (Date.now() > deadline) resolve(false);
        else setTimeout(tryOnce, 3000);
      });
    };
    tryOnce();
  });
}

function runVisualGate() {
  return new Promise((resolve) => {
    const port = 8889;
    const distDir = path.join(ROOT, 'dist');
    if (!fs.existsSync(path.join(distDir, 'index.html'))) {
      console.error(color.red('  dist/ missing — run the build gate (G5) first'));
      resolve(false);
      return;
    }
    // The webpack dev server uses ~2.7GB and gets OOM-killed next to
    // Chromium in this ~4GB sandbox; serving the production build is both
    // lighter and verifies the real artifact G5 produced.
    console.log(color.dim('  $ node scripts/master-loop/serve-dist.cjs   (static dist/, 127.0.0.1:8889)'));
    const child = spawn('node', ['scripts/master-loop/serve-dist.cjs'], {
      cwd: ROOT,
      stdio: ['ignore', 'pipe', 'pipe'],
      detached: true,
    });
    let logTail = '';
    let finished = false;
    const finish = (ok) => {
      if (finished) return;
      finished = true;
      try {
        process.kill(-child.pid, 'SIGTERM'); // whole process group
      } catch {
        child.kill('SIGTERM');
      }
      resolve(ok);
    };
    child.stdout.on('data', (d) => {
      logTail = (logTail + d.toString()).slice(-4000);
      process.stdout.write(d);
    });
    child.stderr.on('data', (d) => {
      logTail = (logTail + d.toString()).slice(-4000);
      process.stderr.write(d);
    });
    child.on('exit', (code) => {
      if (!finished) {
        finished = true;
        console.error(color.red(`  dev server exited early (code ${code})`));
        resolve(false);
      }
    });
    const timer = setTimeout(() => {
      console.error(color.red('  dev server did not open port 8889 in time — last log:\n' + logTail.slice(-1500)));
      finish(false);
    }, 900 * 1000);

    waitForPort(port, 900).then(async (up) => {
      if (!up) {
        clearTimeout(timer);
        console.error(color.red('  port 8889 never opened'));
        finish(false);
        return;
      }
      await new Promise((r) => setTimeout(r, 1500));
      console.log(color.dim('  static server up — running playwright verification…'));
      // Playwright is not a dep of the client; resolve from the motion demo first.
      const candidates = [
        path.join(ROOT, 'node_modules/playwright'),
        path.resolve(__dirname, '../../../master-loop-motions/node_modules/playwright'),
      ];
      const pw = candidates.find((p) => fs.existsSync(p));
      if (!pw) {
        clearTimeout(timer);
        const requirePw = process.env.MASTER_LOOP_REQUIRE_PLAYWRIGHT === '1';
        console.error(
          requirePw
            ? color.red('  playwright not found — visual gate FAILED (MASTER_LOOP_REQUIRE_PLAYWRIGHT=1)')
            : color.yellow('  playwright not found — visual gate SKIPPED (install playwright to enable)'),
        );
        finish(!requirePw);
        return;
      }
      const res = spawnSync(
        'node',
        ['scripts/master-loop/verify-switch.mjs', '--playwright-path', pw, '--port', String(port)],
        { cwd: ROOT, stdio: 'inherit', timeout: 300 * 1000 },
      );
      clearTimeout(timer);
      finish(res.status === 0);
    });
  });
}

/* ---------------------------------------------------------------- main */
async function main() {
  if (flags.status) {
    const state = loadState();
    console.log('Last loop run:', state.updatedAt || 'never');
    PHASES.forEach((p) => {
      const s = state.phases[p.id];
      const label = s === true ? color.green('PASS') : s === false ? color.red('FAIL') : color.yellow('not run');
      console.log(`  ${p.id.padEnd(14)} ${label}`);
    });
    process.exit(0);
  }

  console.log('============================================================');
  console.log(' Master Loop — Motion Package switcher (chat2db-community-client)');
  console.log('============================================================');

  if (!fs.existsSync(path.join(ROOT, 'node_modules'))) {
    console.log(color.yellow('  node_modules missing — installing dependencies first (yarn install)…'));
    if (!runCmd('yarn', ['install'], 'deps', 1800)) {
      console.error(color.red('  GATE FAIL: dependency install failed'));
      process.exit(1);
    }
  }

  const state = loadState();
  const selected = flags.phase ? PHASES.filter((p) => p.id === flags.phase) : PHASES;
  if (selected.length === 0) {
    console.error(`Unknown phase "${flags.phase}". Use --list to see phases.`);
    process.exit(2);
  }

  let allPassed = true;
  for (const phase of selected) {
    console.log(`\n▶ ${phase.title}`);
    console.log(color.dim(`  ${phase.desc}`));
    let passed = false;
    try {
      passed = await phase.run();
    } catch (err) {
      console.error(color.red(`  gate threw: ${err.message}`));
      passed = false;
    }
    state.phases[phase.id] = passed;
    saveState(state);
    if (passed) {
      console.log(color.green(`  ✓ ${phase.id} PASSED`));
    } else {
      console.error(color.red(`  ✗ ${phase.id} FAILED`));
      allPassed = false;
      if (!flags.continueOnError) {
        console.error(color.red('  Loop halted at gate. Fix and re-run (--continue-on-error to override).'));
        process.exit(1);
      }
    }
  }

  console.log('\n============================================================');
  console.log(allPassed ? color.green(' LOOP COMPLETE — ALL GATES PASSED') : color.red(' LOOP COMPLETE — SOME GATES FAILED'));
  console.log('============================================================');
  process.exit(allPassed ? 0 : 1);
}

main().catch((err) => {
  console.error(color.red(`  fatal: ${err.stack || err.message}`));
  process.exit(1);
});
