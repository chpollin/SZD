import { readFileSync, writeFileSync, readdirSync, mkdirSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { rdfCurrentDir, rdfDir } from './paths.mjs';
import { tripleDiff, checkDiff, readExpectations } from './rdf-triples.mjs';

// Compares the local RDF build with the RDF datastream on staging, triple by triple. It only
// reads from gams-staging.uni-graz.at and is not part of the offline suite, because staging
// changes with every ingest. The object of a local file is the PID of its rdf:about values.
//   node test/rdf-staging.mjs [--expect <expectations.txt>] [<name> ...]   (names as in build-rdf/current)
const HOST = process.env.SZD_STAGING_HOST || 'https://gams-staging.uni-graz.at';
const argv = process.argv.slice(2);
const expectIndex = argv.indexOf('--expect');
const expected = expectIndex === -1 ? undefined : readExpectations(argv.splice(expectIndex, 2)[1]);
const names = argv.length ? argv : readdirSync(rdfCurrentDir).filter((f) => f.endsWith('.raw.xml')).map((f) => f.replace('.raw.xml', ''));
const out = resolve(rdfDir, 'staging');
mkdirSync(out, { recursive: true });
let failed = 0;
for (const name of names) {
  const local = resolve(rdfCurrentDir, name + '.raw.xml');
  if (!existsSync(local)) { console.log(`SKIP ${name}: not built in ${rdfCurrentDir}`); continue; }
  const counts = new Map();
  for (const [, pid] of readFileSync(local, 'utf8').matchAll(/rdf:about="https:\/\/gams\.uni-graz\.at\/(o:szd[^#"]*)/g)) { counts.set(pid, (counts.get(pid) || 0) + 1); }
  const pid = [...counts].sort((a, b) => b[1] - a[1])[0]?.[0];
  if (!pid) { console.log(`SKIP ${name}: no object PID in the local RDF`); continue; }
  const url = `${HOST}/archive/objects/${pid}/datastreams/RDF/content`;
  const response = await fetch(url, { signal: AbortSignal.timeout(60000) });
  if (!response.ok) { failed++; console.log(`FAIL ${name}: ${url} answered HTTP ${response.status}`); continue; }
  const remote = resolve(out, name + '.rdf.xml');
  writeFileSync(remote, await response.text());
  const diff = tripleDiff(remote, local);
  if (!diff) { console.log('NOT CHECKED: python with rdflib is not available'); process.exit(2); }
  const result = checkDiff(diff, expected);
  const open = result.unexpectedRemoved.length + result.unexpectedAdded.length + result.missingRemoved.length + result.missingAdded.length;
  if (open) { failed++; }
  console.log(`${open ? 'DIFF' : 'SAME'} ${name} (${pid}): staging ${diff.triples[0]}, local ${diff.triples[1]} triples, ${diff.onlyFirst.length} only on staging, ${diff.onlySecond.length} only local`);
  for (const [label, list] of [['only on staging', result.unexpectedRemoved], ['only local', result.unexpectedAdded]]) {
    for (const triple of list.slice(0, 5)) { console.log(`  ${label}: ${triple}`); }
  }
}
process.exit(failed ? 1 : 0);
