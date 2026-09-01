/**
 * Runs `electron-builder --win nsis`, capturing output. On failure it re-emits
 * the tail of the captured output as GitHub workflow `::error::` commands so the
 * real error becomes visible in the check-run annotations (and in the log).
 */
import { spawn } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const CLI = path.join(ROOT, 'node_modules', 'electron-builder', 'out', 'cli', 'cli.js');

const args = ['--win', 'nsis', '--publish', 'never'];

// Strip any GitHub token so electron-builder never enters publish mode
// (the workflow may set GH_TOKEN; a token in the env triggers auto-publish
// detection and electron-builder then fails when it can't resolve the repo).
const env = { ...process.env, CSC_IDENTITY_AUTO_DISCOVERY: 'false' };
delete env.GH_TOKEN;
delete env.GITHUB_TOKEN;

const child = spawn(process.execPath, [CLI, ...args], {
  cwd: ROOT,
  env,
  stdio: ['ignore', 'pipe', 'pipe']
});

const ring = [];
const MAX = 120;
function pushLine(line) {
  ring.push(line);
  if (ring.length > MAX) ring.shift();
}

child.stdout.on('data', (d) => {
  const s = d.toString();
  process.stdout.write(s);
  for (const l of s.split(/\r?\n/)) if (l.trim()) pushLine(l);
});
child.stderr.on('data', (d) => {
  const s = d.toString();
  process.stderr.write(s);
  for (const l of s.split(/\r?\n/)) if (l.trim()) pushLine(l);
});

child.on('close', (code) => {
  if (code !== 0) {
    const tail = ring.slice(-60);
    console.error('\n===== electron-builder failed — last 60 lines =====');
    for (const l of tail) console.error(l);
    console.error('===== end =====\n');
    // Surface as annotations (readable via the check-runs API).
    for (const l of tail.slice(-20)) {
      console.log(`::error::${l.replace(/%/g, '%25').replace(/\r/g, '%0D').replace(/\n/g, '%0A')}`);
    }
    process.exit(code || 1);
  }
  process.exit(0);
});
