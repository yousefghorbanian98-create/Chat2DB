/**
 * Builds resources/icons/icon.ico from resources/icons/icon.png.
 * Pure Node — embeds the PNG as a 256px entry (valid for Windows Vista+).
 * If ImageMagick is available it is used to produce a multi-size .ico instead.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const ICONS = path.join(ROOT, 'resources', 'icons');
const PNG = path.join(ICONS, 'icon.png');
const ICO = path.join(ICONS, 'icon.ico');

function pngHeader(buf) {
  // width/height are big-endian u32 at offsets 16 and 20
  return { w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) };
}

function buildIcoFromPng() {
  const png = fs.readFileSync(PNG);
  const { w, h } = pngHeader(png);
  if (w > 256 || h > 256) throw new Error('icon.png should be ≤256px');
  // ICONDIR + ICONDIRENTRY + PNG payload
  const header = Buffer.alloc(6);
  header.writeUInt16LE(0, 0); // reserved
  header.writeUInt16LE(1, 2); // type: icon
  header.writeUInt16LE(1, 4); // count
  const entry = Buffer.alloc(16);
  entry.writeUInt8(w >= 256 ? 0 : w, 0);
  entry.writeUInt8(h >= 256 ? 0 : h, 1);
  entry.writeUInt8(0, 2); // palette
  entry.writeUInt8(0, 3); // reserved
  entry.writeUInt16LE(1, 4); // planes
  entry.writeUInt16LE(32, 6); // bpp
  entry.writeUInt32LE(png.length, 8);
  entry.writeUInt32LE(22, 12); // offset
  fs.writeFileSync(ICO, Buffer.concat([header, entry, png]));
}

try {
  execFileSync('convert', [PNG, '-define', 'icon:auto-resize=16,24,32,48,64,128,256', ICO]);
  console.log('icon.ico built with ImageMagick (multi-size)');
} catch (_) {
  try {
    buildIcoFromPng();
    console.log('icon.ico built from PNG (single 256px entry)');
  } catch (e) {
    console.error('make-icon failed:', e.message);
    process.exit(1);
  }
}
