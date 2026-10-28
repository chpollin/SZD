import { readFileSync, existsSync } from 'node:fs';
import { resolve, basename } from 'node:path';
import { spawnSync, execFileSync } from 'node:child_process';
import { here, root, dataRoot } from '../harness.mjs';
import { rdfDir } from './paths.mjs';

// Strict RDF comparison for refactorings of szd-TORDF.xsl that must not change the output:
// the serialisation of every file built with the working-tree stylesheet must equal, byte
// for byte, the one built with the stylesheet of SZD_RDF_STRICT_REV (default HEAD).
// tordf.golden.mjs stays the tolerant check that allows added reference lines.
//   node test/tordf.strict.mjs [<tei.xml> ...]   (default: the golden set without the autographs)
const rev = process.env.SZD_RDF_STRICT_REV || 'HEAD';
const hash = execFileSync('git', ['rev-parse', '--short', rev + '^{commit}'], { cwd: root, encoding: 'utf8' }).trim();
export const strictSources = [
  'data/Index/Location/SZDSTA.xml', 'data/Index/Organisation/SZDORG.xml', 'data/Correspondence/SZDKOR.xml',
  'data/Library/SZDBIB.xml', 'data/PersonalDocument/SZDLEB.xml',
  'data/Correspondence/konvolute/szd.korrespondenzen.meiler-friedrich.xml'
];
const sources = process.argv.slice(2).length ? process.argv.slice(2).map((f) => resolve(f)) : strictSources.map((f) => resolve(dataRoot, f));
const build = (args) => {
  const run = spawnSync(process.execPath, [resolve(here, 'build-rdf.mjs'), ...args, ...sources], { encoding: 'utf8' });
  if (run.status !== 0) { throw new Error('build-rdf.mjs ' + args.join(' ') + ' failed:\n' + run.stdout + run.stderr); }
};
build(['--rev', hash, '--label', 'strict-' + hash]);
build(['--label', 'strict-worktree']);
let failures = 0;
for (const source of sources) {
  const file = basename(source).replace(/\.xml$/, '') + '.raw.xml';
  const [a, b] = ['strict-' + hash, 'strict-worktree'].map((label) => resolve(rdfDir, label, file));
  if (!existsSync(a) || !existsSync(b)) { failures++; console.log('FAIL ' + file + ': not built'); continue; }
  const x = readFileSync(a), y = readFileSync(b);
  if (x.equals(y)) { console.log(`PASS ${file}: byte-identical to ${hash}`); continue; }
  failures++;
  let i = 0;
  while (i < x.length && i < y.length && x[i] === y[i]) { i++; }
  const context = (buffer) => JSON.stringify(buffer.subarray(Math.max(0, i - 80), i + 120).toString('utf8'));
  console.log(`FAIL ${file}: differs from ${hash} at byte ${i}\n  ${hash}: ${context(x)}\n  worktree: ${context(y)}`);
}
console.log(`${sources.length} RDF files compared with ${hash}: ${failures ? failures + ' differ' : 'byte-identical'}`);
process.exit(failures ? 1 : 0);
