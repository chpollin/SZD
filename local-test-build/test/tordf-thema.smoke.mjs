import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import assert from 'node:assert/strict';
import { dataRoot } from '../harness.mjs';
import { rdfDir } from './paths.mjs';

// The person search only finds a theme page if its RDF links every tagged person to the
// person index URI. Expectations come from the theme TEI files of the data repo.
const themaDir = process.env.SZD_RDF_THEMA_DIR || resolve(rdfDir, 'thema');
const PER = 'https://gams.uni-graz.at/o:szd.personen#';

const issueDir = resolve(dataRoot, 'data/Issue');
const sources = readdirSync(issueDir, { withFileTypes: true })
  .filter(entry => entry.isDirectory())
  .flatMap(entry => readdirSync(resolve(issueDir, entry.name)).filter(name => /^szd-thema.*\.xml$/.test(name)).map(name => resolve(issueDir, entry.name, name)));
assert.ok(sources.length, 'no theme TEI files in ' + issueDir);

let persons = 0;
for (const source of sources) {
  const name = source.replace(/\\/g, '/').split('/').pop().replace('.xml', '');
  const file = resolve(themaDir, name + '.rdf.xml');
  assert.ok(existsSync(file), 'not built: ' + file);
  const out = readFileSync(file, 'utf8');
  const tagged = new Set([...readFileSync(source, 'utf8').matchAll(/<name\b[^>]*\bref="([^"]*)"/g)]
    .flatMap(match => match[1].trim().split(/\s+/))
    .filter(ref => ref.includes('SZDPER.'))
    .map(ref => ref.replace(/^#/, '')));
  const linked = new Set([...out.matchAll(/<szd:connectedWithPerson rdf:resource="([^"]*)"\/>/g)].map(match => match[1]));
  for (const id of tagged) assert.ok(linked.has(PER + id), name + ': tagged person ' + id + ' missing from the RDF');
  for (const uri of linked) assert.ok(uri.startsWith(PER + 'SZDPER.'), name + ': person resource outside the person index ' + uri);
  persons += tagged.size;
  console.log(`PASS ${name}: ${tagged.size} tagged persons linked to o:szd.personen`);
}
assert.ok(persons, 'no tagged persons in any theme page');
