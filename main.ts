// The World — Monday 23 November 2026.
// Entry program for the MakeFun news-image bounty.
// The front page is drawn ahead of time by build_entry.py (same folder) and
// stored as entry.png; this program publishes that file. It holds 34 stories
// from Monday 23 November 2026 across 7 regions, drawn at 1024x1024.
// No network, no clock, no randomness, so every run writes the same bytes.
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const page = readFileSync(join(here, 'entry.png'));

// Refuse to publish anything that is not a PNG within the bounty's 1 MiB limit.
// The gate also requires the two runs to write identical bytes; a fixed file
// copied verbatim satisfies that by construction.
const PNG_SIGNATURE = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
const isPng = PNG_SIGNATURE.every((byte, i) => page[i] === byte);
if (!isPng) throw new Error('entry.png is not a PNG file');
if (page.length > 1_048_576) throw new Error(`entry.png is too large: ${page.length} bytes`);
// Width and height sit in the IHDR chunk, big-endian, at bytes 16 and 20.
const width = page.readUInt32BE(16);
const height = page.readUInt32BE(20);
if (width !== 1024 || height !== 1024) throw new Error(`entry.png is ${width}x${height}, expected 1024x1024`);

mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, 'entry.png'), page);
console.log(`wrote entry.png (${page.length} bytes)`);
