import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync, copyFileSync, rmSync } from 'node:fs';
import { resolve, isAbsolute } from 'node:path';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { cpus } from 'node:os';
import { here, root, dataRoot, fixtureDir, materialize, readStylesheets, render, revLabel, outputName, pool } from './harness.mjs';

// Snapshot driver. Renders every page of snapshot.manifest.json in both languages from a
// git revision (the szd-*.xsl of that commit) or from the working tree into
// build-snap/<label>/, and compares two snapshots byte for byte. Rendered pages are never
// versioned; what makes a snapshot reproducible is the revision, the data repository
// commit and the input hashes recorded in meta.json.
//
//   node snapshot.mjs [--rev <commit>|worktree] [--only name,...] [--out <dir>] [--force]
//   node snapshot.mjs --rev <commit> --compare <commit>|worktree [--only name,...]
//   node snapshot.mjs --diff <dirA> <dirB>
const usage = 'Usage: node snapshot.mjs [--rev <commit>|worktree] [--compare <commit>|worktree] [--only name,...] [--out <dir>] [--force] | --diff <dirA> <dirB>';
const argv = process.argv.slice(2);
const flag = (name) => { const i = argv.indexOf(name); return i === -1 ? false : (argv.splice(i, 1), true); };
const option = (name) => { const i = argv.indexOf(name); return i === -1 ? '' : argv.splice(i, 2)[1]; };

export const manifest = JSON.parse(readFileSync(resolve(here, 'snapshot.manifest.json'), 'utf8'));
export const snapRoot = resolve(here, 'build-snap');
const jobs = Number(process.env.SZD_JOBS) || Math.max(2, Math.min(6, cpus().length - 2));
const sha256 = (path) => createHash('sha256').update(readFileSync(path)).digest('hex');

export const inputPath = (input) => {
  const [kind, path] = input.split(/:(.*)/s);
  if (kind === 'data') { return resolve(dataRoot, path); }
  if (kind === 'fixture') { return resolve(fixtureDir, path); }
  throw new Error('Unknown input kind: ' + input);
};

function dataState() {
  const run = (args) => { try { return execFileSync('git', ['-C', dataRoot, ...args], { encoding: 'utf8' }).trim(); } catch { return null; } };
  return { root: dataRoot, commit: run(['rev-parse', 'HEAD']), dirty: run(['status', '--porcelain', '--', 'data']) ? true : false };
}

const selected = (only) => {
  const names = only ? only.split(',') : null;
  const pages = manifest.pages.filter((entry) => !names || names.includes(entry.name));
  if (names && pages.length !== names.length) { throw new Error('Unknown manifest name in --only: ' + only); }
  return pages;
};

// Builds a snapshot and returns its directory. A snapshot of a commit is reused when
// manifest entries, inputs and fixtures are unchanged; the working tree is always rebuilt.
export async function buildSnapshot({ rev = 'worktree', only = '', out = '', force = false, quiet = false } = {}) {
  const label = revLabel(rev);
  // a partial snapshot gets a folder of its own, so it never replaces a complete one
  const dir = out ? resolve(out) : resolve(snapRoot, only ? label + '.' + createHash('sha1').update(only).digest('hex').slice(0, 8) : label);
  if (dir.includes('--')) { throw new Error('Snapshot directory must not contain "--" (the path reaches XML comments): ' + dir); }
  const pages = selected(only);
  const inputs = Object.fromEntries(pages.map((entry) => [entry.name, sha256(inputPath(entry.input))]));
  const fixtures = Object.fromEntries(readdirSync(fixtureDir).filter((f) => f.endsWith('.xml')).map((f) => [f, sha256(resolve(fixtureDir, f))]));
  const metaFile = resolve(dir, 'meta.json');
  // a commit snapshot is reused when it holds every requested page from the same inputs
  const reusable = (candidate) => {
    if (label === 'worktree' || force || !existsSync(resolve(candidate, 'meta.json'))) { return false; }
    const meta = JSON.parse(readFileSync(resolve(candidate, 'meta.json'), 'utf8'));
    return JSON.stringify(meta.fixtures) === JSON.stringify(fixtures) && pages.every((entry) =>
      JSON.stringify(meta.pages.find((p) => p.name === entry.name)) === JSON.stringify(entry)
      && meta.inputs[entry.name] === inputs[entry.name] && !meta.failed.some((f) => f.startsWith(entry.name + '.')));
  };
  for (const candidate of out ? [dir] : [resolve(snapRoot, label), dir]) {
    if (reusable(candidate)) { if (!quiet) { console.log('reuse ' + candidate); } return candidate; }
  }
  rmSync(dir, { recursive: true, force: true });
  const xslDir = resolve(dir, 'xsl');
  materialize(xslDir, readStylesheets(rev));
  const tasks = [];
  for (const entry of pages) {
    const input = resolve(dir, entry.name + '.input.xml');
    copyFileSync(inputPath(entry.input), input);
    for (const mode of entry.modes || ['']) {
      for (const locale of entry.locales || ['de', 'en']) {
        tasks.push(Object.assign(async () => {
          const started = Date.now();
          try {
            await render({ xslDir, page: entry.page, input, out: dir, name: entry.name, locale, mode });
          } catch (error) {
            error.page = outputName(entry.name, locale, mode);
            throw error;
          }
          if (!quiet) { console.log(`built ${outputName(entry.name, locale, mode)} (${Math.round((Date.now() - started) / 1000)} s)`); }
        }, { slow: entry.page === 'szd-Facsimiles' }));
      }
    }
  }
  // the gallery takes minutes, started first it runs alongside the rest
  tasks.sort((a, b) => b.slow - a.slow);
  const failures = await pool(tasks, jobs);
  const meta = {
    rev: label === 'worktree' ? 'worktree' : execFileSync('git', ['rev-parse', rev + '^{commit}'], { cwd: root, encoding: 'utf8' }).trim(),
    label,
    head: execFileSync('git', ['rev-parse', 'HEAD'], { cwd: root, encoding: 'utf8' }).trim(),
    created: new Date().toISOString(),
    data: dataState(),
    processor: 'xslt3 ' + JSON.parse(readFileSync(resolve(here, 'node_modules/xslt3/package.json'), 'utf8')).version + ', node ' + process.version,
    pages,
    inputs,
    fixtures,
    failed: failures.map((error) => error.page)
  };
  writeFileSync(metaFile, JSON.stringify(meta, null, 2) + '\n');
  for (const error of failures) { console.error('FAIL ' + error.message); }
  if (failures.length) { throw new Error(failures.length + ' page(s) failed to render in ' + dir); }
  return dir;
}

// First differing position of two buffers, with line, column and some context.
function firstDifference(a, b) {
  let i = 0;
  while (i < a.length && i < b.length && a[i] === b[i]) { i++; }
  const text = a.subarray(0, i).toString('utf8');
  const line = text.split('\n').length;
  const column = i - (text.lastIndexOf('\n') + 1) + 1;
  const context = (buffer) => JSON.stringify(buffer.subarray(Math.max(0, i - 60), i + 100).toString('utf8'));
  return `byte ${i}, line ${line}, column ${column}\n    a: ${context(a)}\n    b: ${context(b)}`;
}

// Compares every page of two snapshot directories. Returns the list of differences.
export function compareSnapshots(dirA, dirB, { names = null } = {}) {
  const pages = (dir) => readdirSync(dir).filter((f) => f.endsWith('.html') && (!names || names.some((n) => f.startsWith(n + '.'))));
  const a = new Set(pages(dirA));
  const b = new Set(pages(dirB));
  const differences = [];
  for (const file of [...new Set([...a, ...b])].sort()) {
    if (!a.has(file) || !b.has(file)) { differences.push(`${file}: only in ${a.has(file) ? dirA : dirB}`); continue; }
    const x = readFileSync(resolve(dirA, file));
    const y = readFileSync(resolve(dirB, file));
    if (!x.equals(y)) { differences.push(`${file}: differs at ${firstDifference(x, y)}`); }
  }
  const meta = (dir) => existsSync(resolve(dir, 'meta.json')) ? JSON.parse(readFileSync(resolve(dir, 'meta.json'), 'utf8')) : null;
  const [ma, mb] = [meta(dirA), meta(dirB)];
  const notes = [];
  if (ma && mb) {
    if (ma.data.commit !== mb.data.commit || ma.data.dirty || mb.data.dirty) {
      notes.push(`data repository ${ma.data.commit}${ma.data.dirty ? ' (dirty)' : ''} against ${mb.data.commit}${mb.data.dirty ? ' (dirty)' : ''}`);
    }
    const changed = Object.keys(ma.inputs).filter((name) => name in mb.inputs && ma.inputs[name] !== mb.inputs[name]);
    if (changed.length) { notes.push('inputs differ, differences may come from the data: ' + changed.join(', ')); }
  }
  return { compared: new Set([...a, ...b]).size, differences, notes };
}

export function report({ compared, differences, notes }, dirA, dirB) {
  for (const note of notes) { console.log('note: ' + note); }
  for (const difference of differences) { console.log('DIFF ' + difference); }
  console.log(`${compared} pages compared between ${dirA} and ${dirB}: ${differences.length ? differences.length + ' differ' : 'byte-identical'}`);
}

const main = async () => {
  const diff = argv.indexOf('--diff');
  if (diff !== -1) {
    const [a, b] = argv.slice(diff + 1, diff + 3).map((d) => isAbsolute(d) || existsSync(d) ? resolve(d) : resolve(snapRoot, d));
    if (!a || !b) { throw new Error(usage); }
    const result = compareSnapshots(a, b);
    report(result, a, b);
    process.exit(result.differences.length ? 1 : 0);
  }
  const rev = option('--rev') || 'worktree';
  const compare = option('--compare');
  const only = option('--only');
  const out = option('--out');
  const force = flag('--force');
  if (argv.length) { throw new Error(usage); }
  const dirA = await buildSnapshot({ rev, only, out, force });
  console.log('snapshot ' + dirA);
  if (compare) {
    const dirB = await buildSnapshot({ rev: compare, only, force });
    const result = compareSnapshots(dirA, dirB, { names: only ? only.split(',') : null });
    report(result, dirA, dirB);
    process.exit(result.differences.length ? 1 : 0);
  }
};

if (process.argv[1] && resolve(process.argv[1]) === resolve(here, 'snapshot.mjs')) {
  main().catch((error) => { console.error(error.message); process.exit(1); });
}
