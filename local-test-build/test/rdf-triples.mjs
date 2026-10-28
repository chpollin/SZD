import { readFileSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

// Triple diff of two RDF/XML outputs against a named expectation list. The list holds one
// expected change per line, "+ <triple>" for a triple that only the second file may have,
// "- <triple>" for one that only the first may have, both in N-Triples; "#" starts a comment.
// Every difference must be listed and every listed change must occur.
//   node test/rdf-triples.mjs <first.rdf.xml> <second.rdf.xml> [<expectations.txt>]
const here = dirname(fileURLToPath(import.meta.url));

// Returns { triples, onlyFirst, onlySecond } or null when python with rdflib is missing.
export function tripleDiff(first, second) {
  const run = spawnSync('python', [resolve(here, 'rdf_triples.py'), first, second], { encoding: 'utf8', maxBuffer: 512 * 1024 * 1024 });
  if (run.error || (run.status !== 0 && /No module named 'rdflib'/.test(run.stderr))) { return null; }
  if (run.status !== 0) { throw new Error('rdflib failed on ' + first + ' / ' + second + ':\n' + run.stderr); }
  return JSON.parse(run.stdout);
}

export function readExpectations(file) {
  const expected = { onlyFirst: new Set(), onlySecond: new Set() };
  for (const raw of readFileSync(file, 'utf8').split('\n')) {
    const line = raw.trim();
    if (!line || line.startsWith('#')) { continue; }
    const sign = line[0];
    const triple = line.slice(1).trim();
    if (sign === '+') { expected.onlySecond.add(triple); } else if (sign === '-') { expected.onlyFirst.add(triple); } else { throw new Error('Expectation line without + or -: ' + line); }
  }
  return expected;
}

// Unexplained and missing changes of a diff against expectations.
export function checkDiff(diff, expected = { onlyFirst: new Set(), onlySecond: new Set() }) {
  return {
    unexpectedRemoved: diff.onlyFirst.filter((t) => !expected.onlyFirst.has(t)),
    unexpectedAdded: diff.onlySecond.filter((t) => !expected.onlySecond.has(t)),
    missingRemoved: [...expected.onlyFirst].filter((t) => !diff.onlyFirst.includes(t)),
    missingAdded: [...expected.onlySecond].filter((t) => !diff.onlySecond.includes(t))
  };
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const [first, second, expectations] = process.argv.slice(2);
  if (!first || !second) { throw new Error('Usage: node test/rdf-triples.mjs <first.rdf.xml> <second.rdf.xml> [<expectations.txt>]'); }
  for (const file of [first, second]) { if (!existsSync(file)) { throw new Error('Missing ' + file); } }
  const diff = tripleDiff(resolve(first), resolve(second));
  if (!diff) { console.log('NOT CHECKED: python with rdflib is not available'); process.exit(2); }
  const result = checkDiff(diff, expectations ? readExpectations(expectations) : undefined);
  const show = (label, list) => { if (list.length) { console.log(`${label} (${list.length}):\n  ` + list.slice(0, 20).join('\n  ') + (list.length > 20 ? '\n  …' : '')); } };
  show('removed, not expected', result.unexpectedRemoved);
  show('added, not expected', result.unexpectedAdded);
  show('expected removal missing', result.missingRemoved);
  show('expected addition missing', result.missingAdded);
  const failed = Object.values(result).some((list) => list.length);
  console.log(`${failed ? 'FAIL' : 'PASS'} ${first} -> ${second}: ${diff.triples[0]} / ${diff.triples[1]} triples, ${diff.onlyFirst.length} removed, ${diff.onlySecond.length} added`);
  process.exit(failed ? 1 : 0);
}
