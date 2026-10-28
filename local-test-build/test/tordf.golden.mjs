import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import assert from 'node:assert/strict';
import { dataRoot } from '../harness.mjs';
import { rdfBaselineDir, rdfCurrentDir } from './paths.mjs';

// Compares the RDF of the working szd-TORDF.xsl with a baseline built from an earlier
// stylesheet (build-rdf.mjs --rev). Changes to reference resolution may only add links from
// an object to a person or corporate body; nothing may disappear.
const baselineDir = rdfBaselineDir;
const currentDir = rdfCurrentDir;
const addedLine = /^<szd:[A-Za-z]+ rdf:resource="https:\/\/gams\.uni-graz\.at\/o:szd\.(organisation#SZDORG|personen#SZDPER)\.\d+[a-z]?"\/>$/;
// Fix of 2026-09-24 in RDF_autograph: an absolute //t:textClass path gave every autograph the
// persons of all entries, and a stray xsl:value-of wrote their names as text. Against a baseline
// from before the fix, the autographs may lose exactly these relation lines and text lines.
const autographRemoval = (line) => /^<szd:relationToPerson rdf:resource="[^"]+"\/>$/.test(line) || !line.trim().startsWith('<');
// Intended corrections of refactoring phase 1 (2026-10-21). A correction pairs a removed baseline
// line with the added line that replaces it (pair), or allows added lines of one exact form (adds).
// Each pairing consumes one removed and one added line, so a correction can neither hide a lost
// line nor admit an unrelated one.
const corrections = [
  { name: 'library relationToWork with one #', files: ['SZDBIB'],
    pair: (removed, added) => removed.includes('o:szd.werkindex##') && added === removed.replace('o:szd.werkindex##', 'o:szd.werkindex#') },
  { name: 'English singular and plural of the correspondence pieces', files: ['SZDKOR'],
    pair: (removed, added) => /^<szd:text xml:lang="en">\d+ Pieces? of Correspondence/.test(removed)
      && added === removed.replace(/^(<szd:text xml:lang="en">\d+ )(Pieces?)( of Correspondence)/, (m, a, piece, b) => a + (piece === 'Piece' ? 'Pieces' : 'Piece') + b) },
  { name: 'English "leaf" instead of "Blatt"', files: ['SZDBIB', 'SZDAUT'],
    pair: (removed, added) => removed.startsWith('<szd:text xml:lang="en">') && removed.includes(' Blatt ')
      && added === removed.replace(' Blatt ', ' leaf ') }
];

const files = readdirSync(baselineDir).filter(name => name.endsWith('.rdf.xml'));
assert.ok(files.length, 'no baseline files in ' + baselineDir);
const multiset = (lines) => lines.reduce((counts, line) => counts.set(line, (counts.get(line) || 0) + 1), new Map());
const difference = (from, to) => {
  const result = [];
  for (const [line, count] of from) {
    const missing = count - (to.get(line) || 0);
    for (let i = 0; i < missing; i++) result.push(line);
  }
  return result;
};
for (const file of files) {
  const name = file.replace('.rdf.xml', '');
  const currentFile = resolve(currentDir, file);
  assert.ok(existsSync(currentFile), file + ': not built with the current stylesheet');
  const baseline = readFileSync(resolve(baselineDir, file), 'utf8');
  const current = readFileSync(currentFile, 'utf8');
  // a baseline from before 8ec067b had no organisation template at all
  if (name === 'SZDORG' && !baseline.includes('<szd:Organisation ')) {
    assert.ok(!baseline.includes('<szd:Organisation '), 'SZDORG baseline already carried organisations');
    assert.ok(baseline.includes('No data source define!'), 'SZDORG baseline was not the unhandled-PID output');
    assert.ok(current.includes('<szd:Organisation '), 'SZDORG current output carries no organisations');
    assert.ok(!current.includes('No data source define!'));
    console.log(`PASS ${file}: baseline had no template, current output has organisations`);
    continue;
  }
  // mixed content can leave text behind an element on the same line; an inserted sibling then
  // moves that text to the next line without changing a triple, so text gets its own line
  const lines = (rdf) => rdf.replace(/(\/>|<\/[^>]+>)(?=[^\s<])/g, '$1\n').split('\n');
  const before = multiset(lines(baseline));
  const after = multiset(lines(current));
  const removed = difference(before, after);
  const added = difference(after, before);
  const active = corrections.filter(c => c.files.includes(name));
  const open = [...added];
  const corrected = [];
  for (const line of removed) {
    const index = open.findIndex(candidate => active.some(c => c.pair && c.pair(line, candidate)));
    if (index === -1) { corrected.push(line); continue; }
    open.splice(index, 1);
  }
  const unexplained = name === 'SZDAUT' ? corrected.filter(line => !autographRemoval(line)) : corrected;
  assert.deepEqual(unexplained, [], file + ': lines disappeared: ' + unexplained.slice(0, 3).join(' | '));
  if (name === 'SZDAUT') {
    // every autograph relates exactly to the persons of its own keywords
    const tei = readFileSync(resolve(dataRoot, 'data/Autograph/SZDAUT.xml'), 'utf8');
    const own = new Map([...tei.matchAll(/<biblFull[^>]*xml:id="([^"]+)"[\s\S]*?<\/biblFull>/g)].map(([entry, id]) =>
      [id, [...entry.matchAll(/<term type="person" ref="#(SZDPER\.\d+[a-z]?)"/g)].map(m => m[1]).sort().join(' ')]));
    for (const [, id, body] of current.matchAll(/<szd:Autograph rdf:about="[^#]+#([^"]+)">([\s\S]*?)<\/szd:Autograph>/g)) {
      const related = [...new Set([...body.matchAll(/relationToPerson rdf:resource="[^#]+#([^"]+)"/g)].map(m => m[1]))].sort().join(' ');
      assert.equal(related, [...new Set(own.get(id).split(' ').filter(Boolean))].sort().join(' '), file + ': ' + id + ' relates to persons of other entries');
    }
  }
  const unexpected = open.filter(line => !addedLine.test(line) && !active.some(c => c.adds && c.adds.test(line)));
  assert.deepEqual(unexpected, [], file + ': unexpected added lines: ' + unexpected.slice(0, 3).join(' | '));
  console.log(`PASS ${file}: ${open.length} lines added, ${removed.length - corrected.length} corrected, 0 removed`);
}
