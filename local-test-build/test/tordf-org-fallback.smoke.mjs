import { readFileSync } from 'node:fs';
import { resolve, dirname, basename } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import assert from 'node:assert/strict';
import { dataRoot } from '../harness.mjs';
import { rdfDir, rdfCurrentDir } from './paths.mjs';

// The GAMS ingest runs szd-TORDF.xsl without an http base URI, so the stylesheet asks
// production for its indexes even on staging, and production lacks o:szd.organisation until
// that object is published. This check builds correspondence and library again with the
// production copy of the organisation index unavailable and demands the RDF of the regular
// build in build-rdf/current. A stylesheet that still loads the index from production aborts
// the build here, because SaxonJS treats the missing copy as fatal where GAMS yields nothing.
const here = dirname(fileURLToPath(import.meta.url));
const buildDir = rdfDir;
const currentDir = rdfCurrentDir;
const label = 'org-fallback';
const sources = ['data/Correspondence/SZDKOR.xml', 'data/Library/SZDBIB.xml'];

const build = spawnSync(process.execPath, [resolve(here, '../build-rdf.mjs'), '--label', label,
  '--unavailable', 'https://gams.uni-graz.at/o:szd.organisation',
  ...sources.map(source => resolve(dataRoot, source))], { stdio: 'inherit' });
assert.equal(build.status, 0, 'build without the production organisation index failed: the index was requested from a host that lacks it');

for (const source of sources) {
  const name = basename(source, '.xml') + '.rdf.xml';
  const expected = readFileSync(resolve(currentDir, name), 'utf8');
  const actual = readFileSync(resolve(buildDir, label, name), 'utf8');
  const orgRefs = expected.match(/rdf:resource="[^"]*o:szd\.organisation#SZDORG\.[0-9]+"/g) || [];
  assert.ok(orgRefs.length, name + ': the regular build has no organisation reference, the comparison would prove nothing');
  if (actual !== expected) {
    const expectedLines = new Set(expected.split('\n'));
    const actualLines = new Set(actual.split('\n'));
    const lost = [...expectedLines].filter(line => !actualLines.has(line));
    const added = [...actualLines].filter(line => !expectedLines.has(line));
    assert.fail(name + ': RDF differs from the regular build, ' + lost.length + ' lines lost, ' + added.length +
      ' added, first lost: ' + lost.slice(0, 5).join(' '));
  }
  console.log(`PASS ${name}: identical to the regular build without the production organisation index, ${orgRefs.length} organisation references`);
}
